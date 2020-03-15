import sys, os, argparse
from graphml import parse_graph, Node
from distances import print_distances
from routes import INF, print_routes
from visualize import visualize


def get_name_from_path(path):
    name_with_ext = os.path.basename(path)
    if '.' in name_with_ext:
        return ".".join(list(name_with_ext.split('.'))[:-1])
    else:
        return name_with_ext


if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument('-t', '--topology', help='file with network topology')
    argparser.add_argument('-r', '--reserve_flag', help="flag if build reserve paths", action="store_true")
    argparser.add_argument('-s', '--source_node', help="source node id", type=int)
    argparser.add_argument('-d', '--dest_node', help="destination node id", type=int)
    argparser.add_argument('-v', '--vis_flag', help="flag if build visualisation", action="store_true")
    args, unknown = argparser.parse_known_args(sys.argv)
    assert not args.reserve_flag, "Reserve paths are not supported"
    
    nodes, edges = parse_graph(args.topology)

    fname = get_name_from_path(args.topology)
    dist_path = os.path.join("results", fname + "_dist.csv")
    nodes, edges = print_distances(nodes, edges, dist_path)
    print("Distances were written to", dist_path)

    routes_path = os.path.join("results", fname + "_routes.csv")
    dists, routes = print_routes(nodes, edges, routes_path, args.reserve_flag)
    print("Routes were written to", routes_path)

    if args.vis_flag:
        visualize(nodes, edges, routes[args.source_node][args.dest_node])
