# Code by Adam Gluck https://github.com/AdamGluck/dispersion-tie

import networkx as nx

''' This metric is taken from the article
    put out by Facebook on the dispersion tie
    metric. It is generally used to find romantic
    partners. The idea is that the more ties that
    two people share between different parts of one
    users graph, the more they have been introduced around
    thus the more likely they are to be dating.
    It's actually fairly accurate.
    The complete text can be found here: http://arxiv.org/pdf/1310.6753v1.pdf?
    '''
# def disp(G, node, partner):
def disp(G, ego):
    nbunch = G.neighbors(ego)
    sub = G.subgraph(nbunch)

    disperse = 0
    graph_size = len(sub)
    did_calculate = nx.Graph()

    shortest_paths = dict(nx.shortest_path_length(sub))
    count = 0
    for source in shortest_paths:
        disperse += graph_size - len(shortest_paths[source])
        for target in shortest_paths[source]:
            length = shortest_paths[source][target]
            if length > 1 and not did_calculate.has_edge(source, target):
                disperse += 1
            did_calculate.add_edge(source, target)

    return disperse

def norm(G, ego):
    dispv = disp(G, ego)
    mutv = len(list(G.neighbors(ego)))
    return dispv / mutv

def ordered_friends(G):
    ordered = {}
    # for node in G.nodes_iter():
    for node in G.nodes():
        strength = norm(G, node)
        ordered[node] = strength
    return sorted(ordered, key=ordered.get, reverse = True)
