import pidge
import networkx as nx

class HardFaultAnalyzer(pidge.core.types.Analyzer):
    def __init__(self):
        pass
    def predicate(self):
        def query(evidence):
            if evidence.is_a(pidge.types.evidence.StackTrace):
                return evidence.frame.is_bottom()
            return false
        #FIXME: Query could provide a chainable API to build
        # query objects.
        return nx.digraph().add_node(pidge.types.Query("stack_trace",query))
    def analyze(self, debugger, results):
        stack_trace = results.lookup("stack_trace")
        for reg in stack_trace.registers:
            results.add(pidge.bag_evidence(reg), stack_trace)
        # Get the values in the fault registers.
        for reg in debugger.get_fault_registers():
            results.add(pidge.bag_evidence(reg), stack_trace)
        return results