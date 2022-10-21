import numpy as np
import pandas as pd
from gsdmm import MovieGroupProcess
from tqdm import tqdm
import pickle
import re

import cluster_output


def exeCluster():
    # load dataset
    tweets_df = pd.read_csv(r'cleaned_data.csv')
    # strip string(token) into individual
    tweets_df['tokens'] = tweets_df.tokens.apply(lambda x: re.split('\\s', str(x)))
    # create list of  token lists
    docs = tweets_df['tokens'].tolist()

    # train short text topic modelling
    mgp = MovieGroupProcess(K=10, alpha=0.1, beta=0.1, n_iters=30)
    vocab = set(x for doc in docs for x in doc)
    n_terms = len(vocab)
    y = mgp.fit(docs, n_terms)
    # save model
    with open('10clusters.model', 'wb') as f:
        pickle.dump(mgp, f)
        f.close()

    # load in trained model
    filehandler = open('10clusters.model', 'rb')
    mgp = pickle.load(filehandler)

    # helper functions
    def top_words(cluster_word_distribution, top_cluster, values):
        """prints the top words in each cluster"""
        for cluster in top_cluster:
            sort_dicts = sorted(mgp.cluster_word_distribution[cluster].items(), key=lambda k: k[1], reverse=True)[
                         :values]
            print('Cluster %s : %s' % (cluster, sort_dicts))
            print(' — — — — — — — — —')

    def topic_allocation(df, docs, mgp, topic_dict):
        """allocates all topics to each document in original dataframe,
        adding two columns for cluster number and cluster description"""
        topic_allocations = []
        for doc in tqdm(docs):
            topic_label, score = mgp.choose_best_label(doc)
            topic_allocations.append(topic_label)

        df['cluster'] = topic_allocations

        df['topic_name'] = df.cluster.apply(lambda x: get_topic_name(x, topic_dict))
        print('Complete. Number of documents with topic allocated: {}'.format(len(df)))

    def get_topic_name(doc, topic_dict):
        """returns the topic name string value from a dictionary of topics"""
        topic_desc = topic_dict[doc]
        return topic_desc

    doc_count = np.array(mgp.cluster_doc_count)
    print('Number of documents per topic :', doc_count)
    print('*' * 20)
    # topics sorted by the number of documents they are allocated to
    top_index = doc_count.argsort()[-10:][::-1]
    print('Most important clusters (by number of docs inside):',
          top_index)
    print('*' * 20)

    # show the top 5 words in term frequency for each cluster
    topic_indices = np.arange(start=0, stop=len(doc_count), step=1)
    top_words(mgp.cluster_word_distribution, topic_indices, 5)

    topic_dict = {}
    topic_names = ['healthcare & policy',
                   'virus/outbreaks',
                   'cancer studies affecting woman/babies',
                   'covid cases',
                   'cancer & heart disease',
                   'diet & exercise',
                   'health & medical workers',
                   'circuit breaker',
                   'front liner',
                   'public reaction']
    for i, topic_num in enumerate(topic_indices):
        topic_dict[topic_num] = topic_names[i]
    topic_allocation(tweets_df, docs, mgp, topic_dict)
    tweets_df.to_csv(r'10cluster.csv', index=False, header=True)

    cluster_output.topicModelling()

