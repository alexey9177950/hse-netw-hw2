import xml.etree.ElementTree as ET

class Edge:
    def __init__(self, n1, n2, w):
        self.n1 = n1
        self.n2 = n2
        self.w = w

class Node:
    def __init__(self, num, x, y, label):
        self.num = num
        self.x = x
        self.y = y
        self.label = label

    def __str__(self):
        return "Node(" + str(self.num) + ";" + \
                str(self.x) + "," + str(self.y) + ")"

    def __repr__(self):
        return str(self)


def filter_bad_nodes(nodes, edges):
    bad_ids = set(i.num for i in nodes if not (i.x and i.y))
    nodes = [i for i in nodes if i.num not in bad_ids]
    good_ids = set(i.num for i in nodes)

    good_edges = []
    for edge in edges:
        n1, n2 = edge
        if (n1 not in bad_ids) and (n2 not in bad_ids):
            assert (n1 in good_ids) and (n2 in good_ids), "Edge contains invalid node id"
            good_edges.append(edge)
    print("Dropped", len(bad_ids), "/", len(nodes), "nodes")
    print("Dropped", len(edges) - len(good_edges), "/", len(edges), "edges")
    return nodes, good_edges


def parse_graph(filename):
    ns = {'xmlns' : "http://graphml.graphdrawing.org/xmlns"}
    tree = ET.parse(filename)
    root = tree.getroot()

    x_key, y_key, label_key = None, None, None
    for key in root.findall('xmlns:key', ns):
        if key.attrib['attr.name'] == 'Longitude':
            x_key = key.attrib['id']
        if key.attrib['attr.name'] == 'Latitude':
            y_key = key.attrib['id']
        if key.attrib['attr.name'] == 'label' and key.attrib['for'] == 'node':
            label_key = key.attrib['id']
    assert x_key and y_key and label_key, "provide keys for latitude, longtitude and label"

    graphroot = root.find('xmlns:graph', ns)
    undirected = ('edgedefault' in graphroot.attrib) and (graphroot.attrib['edgedefault'] == 'undirected')

    nodes = []
    for i in graphroot.findall('xmlns:node', ns):
        x, y, label = None, None, None
        for j in i.findall('xmlns:data', ns):
            if x_key in j.attrib.values():
                x = float(j.text)
            if y_key in j.attrib.values():
                y = float(j.text)
            if label_key in j.attrib.values():
                label = j.text
        nodes.append(Node(int(i.attrib['id']), x, y, label))

    edges = []
    for edge in graphroot.findall('xmlns:edge', ns):
        new_edge = (int(edge.attrib['source']), int(edge.attrib['target']))
        edges.append(new_edge)
        if undirected:
            edges.append((new_edge[1], new_edge[0]))

    return filter_bad_nodes(nodes, edges)

