import gdb
# So. what does this look like?
# we have a crash or a bug. in either case, there is a condition
# that's true (e.g., a hard fault, or a variable value isn't what we
# expect) and shouldn't be. 

# To determine the kind of fault, I think we have a decision tree
# of tests. the leaves of this tree (or all nodes? maybe it's
# a graph?) each point to a specific form of analysis to perform.
# This decision tree takes a set of Symptom objects as an input.

# Then, there's the analyzer itself. this interacts with GDB, source,
# linker, and elf files to perform crash analysis and generate some
# kind of fault object.

# Then, there's printers. These understand how to display fault objects
# to the user.

# Step 1: gather symptoms.
#  - interact with GDB to gather symptoms
#  - is this also a tree? if we see a symptom, then get it and some
#    set of related symptoms?

# Step 2: decide what kind of analysis is useful.
#  - use the set of symptoms to traverse the analyzer graph.
#  - more than 1 analyzer is okay.

# Step 3: run analysis
#  - analyzers accept symptoms as inputs
#  - analyzers can gather further Evidence from GDB
#  - analyzers output Faults or maybe-Faults, Symptoms,
#    (including their inputs), and Evidence

# Step 4: output
#  - then, there are printers to display all this stuff.


# - are Symptoms and Evidence the same thing?
#   I don't think so. finding Evidence could result in a new Symptom,
#   but they aren't the same. I think the difference is whether the
#   Evidence is a problem or not? So maybe they are the same?
# - is this an iterative process? keep going until we stabilize?
#   is that a design smell? maybe not.
# - what constitutes a Symptom?
#   - location in the stack
#   - potentially other location data - PC, etc

# Maybe symptoms are actually faults, and the analyzers are attempting
# to build a fault graph? root node(s) are the crash itself. then,
# we build up a graph of faults and present that to the user...?
# itsagraph.png
# maybe that's it. we have a graph of Faults. a Fault can have
# associated Evidence & Symptoms. Symptoms are "caused" by faults,
# and so a Fault is associated with a symptom.

# Symptoms are downgraded Faults. Evidence is informational, and
# can be upgraded to a symptom?

# For a stack overflowing crash, what does this look like?
# - visible symptom is a hard fault.
# - symptom pointing to that is a hard fault.
#   - the kind of the symptom tells us where to look next.
#   - in this case, we need to gather the faulting instruction & register values.
# - the faulting instruction becomes a symptom.
#   - look at the registers/values it's dealing with
#   - look at what the instruction does
#   - look at memory regions
# - ideally, at least one more symptom comes out of this
#   - in this case, it'd probably be a register value
# - look at where that register was last changed
#   - another instruction as a symptom
# - keep going until...?
# - meanwhile, we should be somehow associating addresses with objects in memory

# things that are missing:
# - when do we look at the stack pointer to see if we've overflowed?
#   okay. this maybe becomes clear if we track addresses and when they're written to/read from.
#   like, if we figure out above that the faulting register value ultimately came from an
#   address, we should be tracing backwards to see if that address was written to
#   or potentially written to. which doesn't cover a case where the fault isn't
#   on the stack.
# - when do we look at the stack frames themselves - function arguments, etc?
#   - probably when we look at registers. we should be able to directly associate
#     them with arguments.
# - maybe an answer to some of this is that it's okay to just look at something up
#   front and add a symptom for it. off the bat, it's pretty clear if the stack
#   pointer has overrun that memory region. just add it to the graph. ideally, if
#   the fault is on the stack, we'll end up with a single (not disjoint) graph.

# Maybe there are also stack frame nodes?
# - everything has an associated stack frame node
# - that node has frame information...?

# how does the fact that the sp is past the end of the stack fit into this?
# like... how does this take memory regions into account? does it need to do
# so in a more formal way? probably.


# So then, we have analyzers that:
# - can match a subgraph
# - take the full graph as an input
# - can add nodes to the graph

# For example, there's a set of instruction analyzers. For a load/store analyzer:
# - look at the register(s) used by the instruction and add them as evidence
# - add register values as evidence
# - calculate the actual addresses accessed, if any, and add them as evidence
# - mark addresses with their regions?

# Then, maybe there's a stack analyzer? Its job is to look at e.g. sp register nodes
#  and mark it as a symptom if it's outside the associated region.












