from math import sin, cos, asin, sqrt
import math
from graphml import Edge


def hav(x):
    return (1 - math.cos(x)) / 2


def dist_delay(node1, node2):
    # https://en.wikipedia.org/wiki/Haversine_formula

    # longtitudes and latitudes in radians
    phi1 = math.pi * node1.y / 360
    phi2 = math.pi * node2.y / 360
    lambda1 = math.pi * node1.x / 360
    lambda2 = math.pi * node2.x / 360
    
    # distance in km, delay in mks
    EARTH_R = 6371
    dist = 2 * EARTH_R * asin(sqrt(hav(phi2 - phi1) + cos(phi1) * cos(phi2) * hav(lambda2 - lambda1)))
    delay = 4.83 * dist
    return dist, delay


def print_distances(nodes, edges, fname):
    id_to_ind = dict((j.num, i) for i, j in enumerate(nodes))

    f_out = open(fname, "w")
    print("Node 1 (id), Node 1 (label), Node 1 (longtitude), Node 1 (latitude)," + \
          "Node 2 (id), Node 2 (label), Node 2 (longtitude), Node 2 (latitude)," + \
          "Distance (km), Delay (mks)", file=f_out)
    w_edges = []
    for id1, id2 in sorted(edges):
        ind1, ind2 = id_to_ind[id1], id_to_ind[id2]
        node1, node2 = nodes[ind1], nodes[ind2]
        dist, delay = dist_delay(node1, node2)
        print(id1, node1.label, node1.x, node1.y,
              id2, node2.label, node2.x, node2.y,
              *dist_delay(node1, node2),
              sep=',', file=f_out)
        w_edges.append(Edge(ind1, ind2, dist))

    return nodes, w_edges

