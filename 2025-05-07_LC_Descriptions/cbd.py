from rdflib import Namespace, Graph, URIRef
from rdflib.namespace import Namespace

def bind_namespace_prefixes(g):
    # Add usual prefixes for prettier serialization...
    g.bind("bf", Namespace("http://id.loc.gov/ontologies/bibframe/"))
    g.bind("bflc", Namespace("http://id.loc.gov/ontologies/bflc/"))
    g.bind("lclocal", Namespace("http://id.loc.gov/ontologies/lclocal/"))

#g_uri = "https://id.loc.gov/resources/instances/1006621.cbd.json"
g_uri = "1006621.cbd.json"
g = Graph()
g.parse(g_uri)
print("\nNumber of statements in graph from %s is %d" % (g_uri, len(g)))
#bind_namespace_prefixes(g)
#print(g.serialize(format='n3'))

# https://rdflib.readthedocs.io/en/stable/apidocs/rdflib.html#rdflib.graph.Graph.cbd
w_uri = "http://id.loc.gov/resources/instances/1006621"
cbd = g.cbd(URIRef(w_uri))
print("\nNumber of statements in CBD sub-graph for node %s is %d" % (w_uri, len(cbd)))
bind_namespace_prefixes(cbd)
print(cbd.serialize(format='n3'))
