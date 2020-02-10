
import networkx as nx



class Analyzer(object):
    def __init__(self):
        self.predicate = {}
    def predicate(self):
        raise Exception("Analyzers must implement a predicate method!")
    def analyze(self,graph):
        raise Exception("Analyzers must implement an analyze method!")

class Evidence(object):
    def __init__(self):
        self.symptom = False
    def mark_suspect(self):
        self.symptom = True
    def __hash__(self):
        raise Exception("Evidence must implement a __hash__ method!")

class Query(object):
    def __init__(self, matcher):
        self.matcher = matcher
    def match(self, evidence):
        return self.matcher(evidence)

class Results(object):
    def __init__(self, queries, mapping, subgraph):
        self.graph = subgraph
        self.evidence = {}
        for query in queries:
            self.evidence[query.field_name] = mapping[query]
    def add(self, evidence, parent):
        self.graph.add_node(evidence)
        self.graph.add_edge(evidence,parent)
    def lookup(self, name):
        return self.evidence[name]
