from rdflib import Namespace, Graph, URIRef
from rdflib.namespace import Namespace

def bind_namespace_prefixes(g):
    # Add usual prefixes for prettier serialization...
    g.bind("bf", Namespace("http://id.loc.gov/ontologies/bibframe/"))
    g.bind("bflc", Namespace("http://id.loc.gov/ontologies/bflc/"))
    g.bind("lclocal", Namespace("http://id.loc.gov/ontologies/lclocal/"))

for ttl in (
    """
    # Graph of one triple
    @prefix ex: <http://example.org/> .
    ex:r1 ex:p1 ex:r2 .
    """,
    """
    # Graph of two triples with middle bnode
    @prefix ex: <http://example.org/> .
    ex:r1 ex:p1 [ ex:p2 ex:r2 ] .
    """,
    """
    # Graph of three triples with middle bnode
    @prefix ex: <http://example.org/> .
    ex:r1 ex:p1 [ ex:p2 ex:r2; ex:p3 ex:r3 ] .
    """,
    """
    # Graph of two triples with shared bnode object
    @prefix ex: <http://example.org/> .
    ex:r1 ex:p1 _:bnode1 .
    ex:r2 ex:p2 _:bnode1 .
    """,
    """
    # Graph of two triples with shared bnode subject
    @prefix ex: <http://example.org/> .
    _:bnode1 ex:p1 ex:r1 .
    _:bnode1 ex:p2 ex:r2 .
    """,

):
    g = Graph()
    print("---o-> " + ttl)
    g.parse(data=ttl, format="n3")
    for format in ('n3', 'xml', 'nt'):
        print(g.serialize(format=format))
