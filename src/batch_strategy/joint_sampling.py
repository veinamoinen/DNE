import sys
import os
import re
import networkx as nx
import random
import numpy as np

from alias_table_sampling import AliasTable as at

class BatchStrategy(object):
    # G is a DiGraph with edge weights
    def __init__(self, G, num_new, modify_list, params = None):
        self.edges = []
        probs_in = []
        probs_out = []
        n = G.number_of_nodes()
        for u in modify_list:
            for v in G[u]:
                probs_in.append(G[u][v]['weight'])
                probs_out.append(G[v][u]['weight'])
                self.edges.append((u, v))

        for u in xrange(n - num_new, n):
            for v in G[u]:
                probs_in.append(G[u][v]['weight'])
                probs_out.append(G[v][u]['weight'])
                self.edges.append((u, v))
        self.sampling_handler_in = at(probs_in)
        self.sampling_handler_out = at(probs_out)

    def get_batch(self, batch_size):
        batch_labels_in = []
        batch_labels_out = []
        batch_x_in = []
        batch_x_out = []
        for _ in xrange(batch_size):
            idx = self.sampling_handler_in.sample()
            batch_x_in.append(self.edges[idx][0])
            batch_labels_in.append([self.edges[idx][1]])
            idx = self.sampling_handler_out.sample()
            batch_x_out.append(self.edges[idx][1])
            batch_labels_out.append([self.edges[idx][0]])
        return batch_x_in, batch_x_out, batch_labels_in, batch_labels_out
