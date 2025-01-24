# =============================
# Student Names:
# Group ID:
# Date:
# =============================
# CISC 352 - W23
# propagators.py
# desc:
#


#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented to complete problem solution.

'''This file will contain different constraint propagators to be used within
   bt_search.

    1. prop_FC (worth 0.5/3 marks)
        - a propagator function that propagates according to the FC algorithm that 
          check constraints that have exactly one Variable in their scope that has 
          not assigned with a value, and prune appropriately

    2. prop_GAC (worth 0.5/3 marks)
        - a propagator function that propagates according to the GAC algorithm, as 
          covered in lecture

   propagator == a function with the following template
      propagator(csp, newly_instantiated_variable=None)
           ==> returns (True/False, [(Variable, Value), (Variable, Value) ...]

      csp is a CSP object---the propagator can use this to get access
      to the variables and constraints of the problem. The assigned Variables
      can be accessed via methods, the values assigned can also be accessed.

      newly_instaniated_variable is an optional argument.
      if newly_instantiated_variable is not None:
          then newly_instantiated_variable is the most
           recently assigned Variable of the search.
      else:
          progator is called before any assignments are made
          in which case it must decide what processing to do
           prior to any Variables being assigned. SEE BELOW

       The propagator returns True/False and a list of (Variable, Value) pairs.
       Return is False if a deadend has been detected by the propagator.
       in this case bt_search will backtrack
       return is true if we can continue.

      The list of Variable values pairs are all of the values
      the propagator pruned (using the Variable's prune_value method).
      bt_search NEEDS to know this in order to correctly restore these
      values when it undoes a Variable assignment.

      NOTE propagator SHOULD NOT prune a value that has already been
      pruned! Nor should it prune a value twice

      PROPAGATOR called with newly_instantiated_variable = None
      PROCESSING REQUIRED:
        for plain backtracking (where we only check fully instantiated
        constraints)
        we do nothing...return true, []

        for forward checking (where we only check constraints with one
        remaining Variable)
        we look for unary constraints of the csp (constraints whose scope
        contains only one Variable) and we forward_check these constraints.

        for gac we establish initial GAC by initializing the GAC queue
        with all constaints of the csp


      PROPAGATOR called with newly_instantiated_variable = a Variable V
      PROCESSING REQUIRED:
         for plain backtracking we check all constraints with V (see csp method
         get_cons_with_var) that are fully assigned.

         for forward checking we forward check all constraints with V
         that have one unassigned Variable left

         for gac we initialize the GAC queue with all constraints containing V.
   '''

def prop_BT(csp, newVar=None):
    '''Do plain backtracking propagation. That is, do no
    propagation at all. Just check fully instantiated constraints'''

    if not newVar:
        return True, []
    for c in csp.get_cons_with_var(newVar):
        if c.get_n_unasgn() == 0:
            vals = []
            vars = c.get_scope()
            for var in vars:
                vals.append(var.get_assigned_value())
            if not c.check_tuple(vals):
                return False, []
    return True, []

def prop_FC(csp, newVar=None):
    '''Do forward checking. That is, check constraints with
       only one uninstantiated Variable. Keep track of all pruned
       Variable-value pairs and return them.'''
    
    # Initialize the list of pruned values
    pruned = []

    # Determine which constraints to check
    if newVar is None:
        # If no variable is newly assigned, check all constraints
        constraints_to_check = csp.get_all_cons()
    else:
        # Otherwise, check only the constraints involving the newly assigned variable
        constraints_to_check = csp.get_cons_with_var(newVar)

    # Iterate through the selected constraints
    for constraint in constraints_to_check:
        # Check if exactly one variable in the constraint's scope is unassigned
        if constraint.get_n_unasgn() == 1:
            # Retrieve the single unassigned variable
            unassigned_var = constraint.get_unasgn_vars()[0]

            # Iterate through all values in the unassigned variable's current domain
            for value in unassigned_var.cur_domain():
                # Check if the value has support in the constraint
                if not constraint.has_support(unassigned_var, value):
                    # If the value is unsupported, prune it
                    unassigned_var.prune_value(value)
                    pruned.append((unassigned_var, value))

            # Check if the unassigned variable's domain is now empty
            if unassigned_var.cur_domain_size() == 0:
                # Dead end detected, return False and the list of pruned values
                return False, pruned

    # Return True and the list of pruned values if no dead ends are detected
    return True, pruned


def prop_GAC(csp, newVar=None):
    '''Do GAC propagation. If newVar is None, enforce initial GAC by processing
       all constraints. Otherwise, process constraints containing newVar.'''
    
    # Initialize the list of pruned values
    pruned = []

    # Determine the constraints to check
    if newVar is None:
        # If no new variable is assigned, initialize the GAC queue with all constraints
        gac_queue = csp.get_all_cons()
    else:
        # If a new variable is assigned, initialize the GAC queue with all constraints involving that variable
        gac_queue = csp.get_cons_with_var(newVar)

    # Process the GAC queue
    while gac_queue:
        # Dequeue a constraint to enforce arc consistency
        constraint = gac_queue.pop(0)
        
        # For each variable in the constraint's scope, check arc consistency
        for var in constraint.get_scope():
            # Check if the variable's domain has any value supported by the constraint
            for value in var.cur_domain():
                if not constraint.has_support(var, value):
                    # If no support exists, prune the value
                    var.prune_value(value)
                    pruned.append((var, value))

                    # If pruning occurs, add all constraints involving the variable to the queue
                    for neighbor in csp.get_cons_with_var(var):
                        if neighbor not in gac_queue:
                            gac_queue.append(neighbor)

            # Check if the domain of the variable is empty after pruning
            if var.cur_domain_size() == 0:
                # If a domain becomes empty, return False indicating a dead end
                return False, pruned

    # If the GAC queue is empty and no dead ends were detected, return True
    return True, pruned