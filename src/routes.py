INF = 10**18

def get_routes(n, edges):
    dists = [[INF for i in range(n)] for j in range(n)]
    paths = [[[] for i in range(n)] for j in range(n)]
    for i in range(n):
        dists[i][i] = 0
        paths[i][i] = [i]
    for e in edges:
        dists[e.n1][e.n2] = min(dists[e.n1][e.n2], e.w)
        dists[e.n2][e.n1] = min(dists[e.n2][e.n1], e.w)
        paths[e.n1][e.n2] = [e.n1, e.n2]
        paths[e.n2][e.n1] = [e.n2, e.n1]

    for mid_n in range(n):
        for first_n in range(n):
            for last_n  in range(n):
                new_dist = dists[first_n][mid_n] + dists[mid_n][last_n]
                if new_dist < dists[first_n][last_n]:
                    dists[first_n][last_n] = new_dist
                    path_f = paths[first_n][mid_n]
                    path_l = paths[mid_n][last_n]
                    paths[first_n][last_n] = path_f + path_l[1:]

    return dists, paths


def print_routes(nodes, edges, fname, reserve_paths=False):
    n = len(nodes)
    dists, routes = get_routes(len(nodes), edges)
    
    f_out = open(fname, "w")
    print("Node 1 (id), Node 2 (id), Path type, Path, Delay (mks)", file=f_out)
    
    for i in range(n):
        for j in range(i + 1, n):
            dist = dists[i][j]
            path = [nodes[ind].num for ind in routes[i][j]] if dist != INF else "no"
            delay = dist if dist != INF else ""
            print(nodes[i].num, nodes[j].num, "main", path, delay, sep=",", file=f_out)
    
    return dists, routes

