# =============================
# Student Names: Alice Fraimovich, Jacob Shin, Calvin Zheng
# Group ID: 22
# Date: 2025 Jan 30
# =============================
# CISC 352 - W23
# cagey_csp.py
# desc: 
#


#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented to complete problem solution.

'''This file will contain different constraint propagators to be used within
   the propagators

1. ord_dh (worth 0.25/3 points)
    - a Variable ordering heuristic that chooses the next Variable to be assigned 
      according to the Degree heuristic

2. ord_mv (worth 0.25/3 points)
    - a Variable ordering heuristic that chooses the next Variable to be assigned 
      according to the Minimum-Remaining-Value heuristic


var_ordering == a function with the following template
    var_ordering(csp)
        ==> returns Variable

    csp is a CSP object---the heuristic can use this to get access to the
    Variables and constraints of the problem. The assigned Variables can be
    accessed via methods, the values assigned can also be accessed.

    var_ordering returns the next Variable to be assigned, as per the definition
    of the heuristic it implements.
   '''

def ord_dh(csp):
    '''Return the next Variable to be assigned according to the Degree Heuristic.
    The Degree Heuristic chooses the variable involved in the largest number of constraints
    with other unassigned variables.'''
    unassigned_vars = [var for var in csp.get_all_unasgn_vars()]
    
    if not unassigned_vars:
        return None  # No unassigned variables left

    # Compute the degree for each unassigned variable
    max_degree_var = max(unassigned_vars, 
                         key=lambda var: sum(1 for c in csp.get_cons_with_var(var) 
                                             if any(unasgn_var.is_assigned() is False for unasgn_var in c.get_scope())))
    return max_degree_var

def ord_mrv(csp):
    '''Return the Variable to be assigned according to the Minimum Remaining Values heuristic.
    MRV chooses the variable with the smallest domain size.'''
    unassigned_vars = [var for var in csp.get_all_unasgn_vars()]

    if not unassigned_vars:
        return None  # No unassigned variables left

    # Find the variable with the smallest domain size
    min_domain_var = min(unassigned_vars, key=lambda var: var.cur_domain_size())
    return min_domain_var
