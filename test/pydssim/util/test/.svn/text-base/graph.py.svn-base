'''graph.py

The naming graph for each device -- nodes are devices, edges are names
'''

class NameGraph:
  root = None
  nodes = []
  rootnodes = []

  def __init__(self):
    pass

  def lookup(self, name, node=None, visited=None):
    if visited is None:
      visited = []
    if node is None:
      node=self.root
    ret = []
    visited.append(node)
    for e in node.edges:
      if e.name == name:
        ret.append(e.dst)
      if e.importlink and e.dst not in visited:
        ret.append(lookup(name, e.dst, visited))
    return ret

  def buildroot(self, id):
    self.root = GraphNode(id)
    self.nodes.append(self.root)
    self.rootnodes.append(self.root)
    return self.root

  def addrootnode(self, id):
    '''add a node without a link pointing to it (nameless node)'''
    n = GraphNode(id)
    self.nodes.append(n)
    self.rootnodes.append(n)

  def addnode(self, id, name, where=None):
    if where is None:
      where = self.root
    n = GraphNode(id)
    self.nodes.append(n)
    where.addedge(name, n)
    return n


class GraphNode:
  def __init__(self, id):
    self.edges = []
    self.id = id

  def addedge(self, name, node):
    self.edges.append(GraphEdge(name, self, node))

class GraphEdge:
  def __init__(self, name, src, dst):
    self.src = src
    self.dst = dst
    self.name = name
    self.importlink = False

