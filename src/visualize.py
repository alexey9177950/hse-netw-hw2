import matplotlib.pyplot as plt


def draw_node(node, very=False, node_type=None):
    if node_type == "source_dest":
        plt.scatter(node.x, node.y, color='black', label=node.label)
        plt.annotate(node.label, (node.x, node.y))
    elif node_type == "on_path":
        plt.scatter(node.x, node.y, color='r')
    elif node_type == "usual":
        plt.scatter(node.x, node.y, color='b')
    else:
        raise Exception("unknown node type")


def draw_line(node1, node2, special):
    if special:
        plt.plot([node1.x, node2.x], [node1.y, node2.y], 'r')
    else:
        plt.plot([node1.x, node2.x], [node1.y, node2.y], 'g')


def visualize(nodes, edges, route):
    plt.axis('equal')
    for e in edges:
        try: draw_line(nodes[e.n1], nodes[e.n2], special=False)
        except: pass
    for i in range(len(route) - 1):
        n1, n2 = route[i], route[i + 1]
        try:
            draw_line(nodes[n1], nodes[n2], special=True)
        except: pass
    for node in nodes:
        draw_node(node, node_type='usual')
    for ind in route[1:-1]:
        draw_node(nodes[ind], node_type='on_path')
    draw_node(nodes[route[0]], node_type='source_dest')
    draw_node(nodes[route[-1]], node_type='source_dest')
    plt.show()
