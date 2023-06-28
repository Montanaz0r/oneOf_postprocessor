from collections import defaultdict
import rdflib
from rdflib.collection import Collection
from rdflib.term import BNode, URIRef
import sys

input_rdf = sys.argv[1]
output_rdf = sys.argv[2]


g = rdflib.Graph()
g2 = rdflib.Graph()
g.parse(input_rdf, format="turtle")

for ns in g.namespaces():
    g2.namespace_manager.bind(ns[0], ns[1])

concepts = defaultdict(list)

for s, p, o in g:
    if p == URIRef("http://www.w3.org/2002/07/owl#oneOf"):
        concepts[s].append(o)
    else:
        g2.add((s, p, o))

for concept in concepts:
    bn = BNode()
    g2.add((concept, URIRef("http://www.w3.org/2002/07/owl#oneOf"), bn))
    Collection(g2, bn, concepts[concept])

g2.serialize(destination=output_rdf, format="turtle")
