#!/usr/bin/env python3

import json
import sys
import time 

from sklearn.feature_extraction.text import TfidfVectorizer


def convert_single(doc):
    NUM_KEYWORDS = 5
    entities = [e['text'] for e in doc['enriched_text']["entities"][:NUM_KEYWORDS]]
    concepts = [e['text'] for e in doc['enriched_text']["concepts"][:NUM_KEYWORDS]]
    keywords = doc['metadata']["keywords"][:NUM_KEYWORDS]
    categories = [e['label'] for e in doc['enriched_text']["categories"][:NUM_KEYWORDS]]
    lst = entities + concepts + keywords + categories
    lst = [x.replace(' ', '_') for x in lst]
    lst = ' '.join(lst)
    return lst


def convert_results(doc):
    results = doc.result['results']
    return [convert_single(result) for result in results]


def cluster(X, num=3):
    from sklearn.cluster import KMeans
    kmeans = KMeans(n_clusters=num)
    kmeans.fit(X)
    return kmeans


def fit(vectorizer, kmeans, doc):
    title = doc['metadata']['title'] # filename -> TITLE
    converted = convert_single(doc)
    vec = vectorizer.transform([converted])
    y = kmeans.predict(vec)
    return y[0], title #, score_str


def query(query_string, disc, n_results=50, n_clusters=3):
    total_start_time = time.time()
    query_start_time = time.time()
    discovery = disc['discovery']
    env_id = disc['env_id']
    coll_id = disc['coll_id']
    response = discovery.discovery.query(env_id, coll_id, query=query_string, count=n_results)
    query_end_time = time.time()
    # print(f'Query: {query_end_time-query_start_time}')
    cluster_start_time = time.time()
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
    title2y = {}
    for doc in docs.result['results']:
        y, title = fit(vectorizer, kmeans, doc)
        clusters[y].append(title)
        title2y[title] = y
    for result in response.result['results']:
        metadata = result['metadata']
        title = metadata['title']
        metadata['cluster_id'] = int(title2y[title])
    cluster_end_time = time.time()
    total_end_time = time.time()
    #print(f'Total: {total_end_time-total_start_time}')
    timings = {
        'total_time': int((total_end_time-total_start_time)*1000),
        'query_time': int((query_end_time-query_start_time)*1000),
        'cluster_time': int((cluster_end_time-cluster_start_time)*1000),
        }
    response.result['timings'] = timings
    return response.result


def print_response(response, number_of_clusters):
    results = response['results']
    #print('\nResults by cluster:')
    url2id = {}
    print('Results:')
    for i, result in enumerate(results):
        #url = result['metadata']['url']
        title = result['metadata']['title']
        url = title
        cluster_id = result['metadata']['cluster_id']
        print(f'[{i}] {title}')
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
    from verdens_klogeste.insert import setup, DICOVERY_ENV_NAME, DICOVERY_COLL_NAME
    args = cli()
    _, discovery = setup()
    env_id = discovery.find_env_id(DICOVERY_ENV_NAME)
    coll_id = discovery.find_coll_id(env_id, DICOVERY_COLL_NAME)
    disc = {'discovery': discovery, 'env_id': env_id, 'coll_id': coll_id}
    response = query(args.q, disc, args.results_count, args.number_of_clusters)
    print(type(response))
    if 'timings' in response:
        print(response['timings'])
    print_response(response, args.number_of_clusters)


if __name__ == '__main__':
    main()
