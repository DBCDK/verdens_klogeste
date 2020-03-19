#!/usr/bin/env python3

import json
import sys

from sklearn.feature_extraction.text import TfidfVectorizer


def convert_single(doc):
    NUM_KEYWORDS = 5
    # print(doc['extracted_metadata']['filename'])
    entities = [e['text'] for e in doc['enriched_text']["entities"][:NUM_KEYWORDS]]
    concepts = [e['text'] for e in doc['enriched_text']["concepts"][:NUM_KEYWORDS]]
    #keywords = [e['text'] for e in doc['metadata']["keywords"][:NUM_KEYWORDS]]
    keywords = doc['metadata']["keywords"][:NUM_KEYWORDS]
    categories = [e['label'] for e in doc['enriched_text']["categories"][:NUM_KEYWORDS]]
    # print(f'E : {entities}')
    # print(f'C1: {concepts}')
    # print(f'K : {keywords}')
    # print(f'C2: {categories}')
    lst = entities + concepts + keywords + categories
    lst = [x.replace(' ', '_') for x in lst]
    lst = ' '.join(lst)
    return lst


def convert_results(doc):
    results = doc.result['results']
    #results = doc['result']['results']
    return [convert_single(result) for result in results]


def cluster(X, num=3): #vectorizer, docs):
    from sklearn.cluster import KMeans
    kmeans = KMeans(n_clusters=num)
    kmeans.fit(X)
    #y_kmeans = kmeans.predict(X)
    #print(y_kmeans)
    return kmeans


def fit(vectorizer, kmeans, doc):
    filename = doc['metadata']['url']
    confidence = doc['result_metadata']['confidence']
    score = doc['result_metadata']['score']
    filename = f'{filename}  ({score:.2f}/{confidence:.2f})'
    converted = convert_single(doc)
    vec = vectorizer.transform([converted])
    y = kmeans.predict(vec)
    return y[0], filename


# def main_old():
#     s = sys.stdin.read()
#     doc = json.loads(s)
#     converted = convert_results(doc)
#     # print(converted)
#     vectorizer = TfidfVectorizer()
#     X = vectorizer.fit_transform(converted)
#     print(vectorizer.get_feature_names())
#     print(X.shape)
#     vec = vectorizer.transform([converted[0]])
#     print(vec)
#     print('---')
#     print(X[0])
#     cluster(X)


def main():
    NUM_CLUSTERS = 3
    s = sys.stdin.read()
    docs = json.loads(s)
    converted = convert_results(docs)
    vectorizer = TfidfVectorizer()
    vectorizer.fit(converted)
    vec = vectorizer.transform(converted)
    kmeans = cluster(vec, num=NUM_CLUSTERS)
    clusters = [[] for i in range(NUM_CLUSTERS)]
    print('\ncluster_id : filename  (discovery-score/discovery-confidence)')
    for doc in docs['result']['results']:
        y, filename = fit(vectorizer, kmeans, doc)
        print(f'{y}: {filename}')
        clusters[y].append(filename)
    print('\n\nResults by cluster:')
    for i, clster in enumerate(clusters):
        print(f'#{i}')
        for filename in clster:
            print(f'  {filename}')


def query():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-q')
    args = parser.parse_args()

    from verdens_klogeste.insert import setup, DICOVERY_ENV_NAME, DICOVERY_COLL_NAME

    _, disc = setup()
    env_id = disc.find_env_id(DICOVERY_ENV_NAME)
    coll_id = disc.find_coll_id(env_id, DICOVERY_COLL_NAME)
    response = disc.discovery.query(env_id, coll_id, query=args.q, count=50)
    #print(response)
    for i, result in enumerate(response.result['results']):
        print(f'[{i}]: {result["metadata"]["url"]}')

    NUM_CLUSTERS = 3
    docs = response
    converted = convert_results(docs)
    vectorizer = TfidfVectorizer()
    vectorizer.fit(converted)
    vec = vectorizer.transform(converted)
    kmeans = cluster(vec, num=NUM_CLUSTERS)
    clusters = [[] for i in range(NUM_CLUSTERS)]
    print('\ncluster_id : filename  (discovery-score/discovery-confidence)')
    for doc in docs.result['results']:
        y, filename = fit(vectorizer, kmeans, doc)
        #print(f'{y}: {filename}')
        clusters[y].append(filename)
    print('\nResults by cluster:')
    for i, clster in enumerate(clusters):
        print(f'#{i}')
        for filename in clster:
            print(f'  {filename}')

        
def clustering(discovery_result, num_clusters=3):
    None
    
            
if __name__ == '__main__':
    #main()
    query()
