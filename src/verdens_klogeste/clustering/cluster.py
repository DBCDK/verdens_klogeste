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
    # confidence = doc['result_metadata']['confidence']
    # score = doc['result_metadata']['score']
    # score_str = f'({score:.2f}/{confidence:.2f})'
    converted = convert_single(doc)
    vec = vectorizer.transform([converted])
    y = kmeans.predict(vec)
    return y[0], filename #, score_str


def query(query_string, n_results=50, n_clusters=3):
    #print(f'{query_string}  {n_results}  {n_clusters}')
    #print(f'{type(n_results)}  {type(n_clusters)}')
    from verdens_klogeste.insert import setup, DICOVERY_ENV_NAME, DICOVERY_COLL_NAME

    _, disc = setup()
    env_id = disc.find_env_id(DICOVERY_ENV_NAME)
    coll_id = disc.find_coll_id(env_id, DICOVERY_COLL_NAME)
    response = disc.discovery.query(env_id, coll_id, query=query_string, count=n_results)
    matching_results = response.result['matching_results']    
    if matching_results == 0:
        return response.result

    if len(response.result['results']) < n_clusters:
        # There are requested more results than there are clusters.
        # We will give all results cluster_id=0
        for result in response.result['results']:
            metadata = result['metadata']
            metadata['cluster_id'] = 0
        return response.result

    docs = response
    converted = convert_results(docs)
    vectorizer = TfidfVectorizer()
    vectorizer.fit(converted)
    vec = vectorizer.transform(converted)
    kmeans = cluster(vec, num=n_clusters)
    clusters = [[] for i in range(n_clusters)]
    #print('\ncluster_id : filename  (discovery-score/discovery-confidence)')
    filename2y = {}
    for doc in docs.result['results']:
        y, filename = fit(vectorizer, kmeans, doc)
        clusters[y].append(filename)
        filename2y[filename] = y
    for result in response.result['results']:
        metadata = result['metadata']
        url = metadata['url']
        metadata['cluster_id'] = int(filename2y[url])
        # print(metadata)
    return response.result


def print_response(response, number_of_clusters):
    results = response['results']
    #print('\nResults by cluster:')
    url2id = {}
    print('Results:')
    for i, result in enumerate(results):
        url = result['metadata']['url']
        cluster_id = result['metadata']['cluster_id']
        print(f'[{i}] {url}')
        url2id[url] = cluster_id       
    clusters = [[] for _ in range(number_of_clusters)]
    for url, cluster_id in url2id.items():
        clusters[cluster_id].append(url)
    for i, clstrs in enumerate(clusters):
        print(f'\n#{i}')
        for url in clstrs:
            print(url)


def cli():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-q')
    parser.add_argument("-n", "--results-count", default=50, type=int)
    parser.add_argument("-c", "--number-of-clusters", default=3, type=int)
    args = parser.parse_args()
    return args


def main():
    args = cli()
    response = query(args.q, args.results_count, args.number_of_clusters)
    print(type(response))
    print_response(response, args.number_of_clusters)


if __name__ == '__main__':
    main()