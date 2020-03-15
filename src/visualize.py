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
    # in case of crossing map's edge
    if node1.x > node2.x:
        node1, node2 = node2, node1
    left_marg = node1.x - (-180)
    right_marg = 180 - node2.x
    if left_marg + right_marg < node2.x - node1.x:
        bord_height = (node1.y * left_margin + node2.y * right_margin) / (left_margin + right_margin)
        left_node = Node(-180, bord_height)
        right_node = Node(180, bord_height)
        draw_line(left_node, node1, special)
        draw_line(node2, right_node, special)
        return

    if special:
        plt.plot([node1.x, node2.x], [node1.y, node2.y], 'r')
    else:
        plt.plot([node1.x, node2.x], [node1.y, node2.y], 'g')


def visualize(nodes, edges, route):
    plt.title("Route")
    plt.axis('equal')
    plt.xlabel('Longtitude')
    plt.ylabel('Latitude')
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
