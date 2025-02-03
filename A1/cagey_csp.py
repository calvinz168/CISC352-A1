# =============================
# Student Names: Alice Fraimovich, Jacob Shin, Calvin Zheng
# Group ID: 22
# Date: 2025 Jan 30
# =============================
# CISC 352 - W23
# cagey_csp.py
# desc: 
#

#Look for #IMPLEMENT tags in this file.
'''
All models need to return a CSP object, and a list of lists of Variable objects
representing the board. The returned list of lists is used to access the
solution.

For example, after these three lines of code

    csp, var_array = binary_ne_grid(board)
    solver = BT(csp)
    solver.bt_search(prop_FC, var_ord)

var_array is a list of all Variables in the given csp. If you are returning an entire grid's worth of Variables
they should be arranged linearly, where index 0 represents the top left grid cell, index n-1 represents
the top right grid cell, and index (n^2)-1 represents the bottom right grid cell. Any additional Variables you use
should fall after that (i.e., the cage operand variables, if required).

1. binary_ne_grid (worth 0.25/3 marks)
    - A model of a Cagey grid (without cage constraints) built using only
      binary not-equal constraints for both the row and column constraints.

2. nary_ad_grid (worth 0.25/3 marks)
    - A model of a Cagey grid (without cage constraints) built using only n-ary
      all-different constraints for both the row and column constraints.

3. cagey_csp_model (worth 0.5/3 marks)
    - a model of a Cagey grid built using your choice of (1) binary not-equal, or
      (2) n-ary all-different constraints for the grid, together with Cagey cage
      constraints.


Cagey Grids are addressed as follows (top number represents how the grid cells are adressed in grid definition tuple);
(bottom number represents where the cell would fall in the var_array):
+-------+-------+-------+-------+
|  1,1  |  1,2  |  ...  |  1,n  |
|       |       |       |       |
|   0   |   1   |       |  n-1  |
+-------+-------+-------+-------+
|  2,1  |  2,2  |  ...  |  2,n  |
|       |       |       |       |
|   n   |  n+1  |       | 2n-1  |
+-------+-------+-------+-------+
|  ...  |  ...  |  ...  |  ...  |
|       |       |       |       |
|       |       |       |       |
+-------+-------+-------+-------+
|  n,1  |  n,2  |  ...  |  n,n  |
|       |       |       |       |
|n^2-n-1| n^2-n |       | n^2-1 |
+-------+-------+-------+-------+

Boards are given in the following format:
(n, [cages])

n - is the size of the grid,
cages - is a list of tuples defining all cage constraints on a given grid.


each cage has the following structure
(v, [c1, c2, ..., cm], op)

v - the value of the cage.
[c1, c2, ..., cm] - is a list containing the address of each grid-cell which goes into the cage (e.g [(1,2), (1,1)])
op - a flag containing the operation used in the cage (None if unknown)
      - '+' for addition
      - '-' for subtraction
      - '*' for multiplication
      - '/' for division
      - '?' for unknown/no operation given

An example of a 3x3 puzzle would be defined as:
(3, [(3,[(1,1), (2,1)],"+"),(1, [(1,2)], '?'), (8, [(1,3), (2,3), (2,2)], "+"), (3, [(3,1)], '?'), (3, [(3,2), (3,3)], "+")])

'''

from cspbase import *
import itertools
import math

def binary_ne_grid(cagey_grid):
    '''
    Create a CSP model of a Cagey grid using binary not-equal constraints for rows and columns.
    '''
    n, cages = cagey_grid
    csp = CSP("Binary Not-Equal Grid")
    var_array = []

    
    for i in range(n): # var for each cell in grid
        row = []
        for j in range(n):
            var = Variable(f"Cell({i+1},{j+1})", list(range(1, n + 1)))
            csp.add_var(var)
            row.append(var)
        var_array.append(row)

    for i in range(n):     # adds binary not-equal constraints for rows
        for j1 in range(n):
            for j2 in range(j1 + 1, n):
                con = Constraint(f"Row({i+1})_{j1+1},{j2+1}", [var_array[i][j1], var_array[i][j2]])
                sat_tuples = [(a, b) for a in range(1, n + 1) for b in range(1, n + 1) if a != b]
                con.add_satisfying_tuples(sat_tuples)
                csp.add_constraint(con)

    
    for j in range(n):   # adds binary not-equal constraints for cols
        for i1 in range(n):
            for i2 in range(i1 + 1, n):
                con = Constraint(f"Col({j+1})_{i1+1},{i2+1}", [var_array[i1][j], var_array[i2][j]])
                sat_tuples = [(a, b) for a in range(1, n + 1) for b in range(1, n + 1) if a != b]
                con.add_satisfying_tuples(sat_tuples)
                csp.add_constraint(con)

    return csp, [var for row in var_array for var in row]

def nary_ad_grid(cagey_grid):
    '''
    creates CSP model of a Cagey grid
    '''
    n, cages = cagey_grid
    csp = CSP("N-ary All-Different Grid")
    var_array = []

    for i in range(n): # creates vars for each cell in grid
        row = [] # initializes list
        for j in range(n):
            var = Variable(f"Cell({i+1},{j+1})", list(range(1, n + 1)))
            csp.add_var(var)
            row.append(var)
        var_array.append(row)

    
    for i in range(n): # adds n-ary all differing constraints for rows
        con = Constraint(f"Row({i+1})", var_array[i])
        sat_tuples = [tup for tup in itertools.permutations(range(1, n + 1), n)]
        con.add_satisfying_tuples(sat_tuples)
        csp.add_constraint(con)


    for j in range(n): # adds n-ary all differing constraints for cols
        column_vars = [var_array[i][j] for i in range(n)]
        con = Constraint(f"Col({j+1})", column_vars)
        sat_tuples = [tup for tup in itertools.permutations(range(1, n + 1), n)]
        con.add_satisfying_tuples(sat_tuples)
        csp.add_constraint(con)

    return csp, [var for row in var_array for var in row]


def cagey_csp_model(board):
    """
    This function converts the input board into a CSP model.
    """
    variables = []  # Will hold variables in the CSP
    var_dict = {}  # To map variable names to their domains
    
    # Unpack the board
    size, cages = board  # Assuming board is of the form (size, list_of_cages)

    # Create a list of variables from the cages
    for cage in cages:
        num_cells, cells, operator = cage  # Unpacking each cage
        var_names = [Variable(f"cage_{x},{y}") for x, y in cells]  # Create Variable instances
        domain = list(range(1, 10))  # Domain for each variable (1-9)
        
        # Map each variable to its domain
        for var in var_names:
            var_dict[var.name] = domain
        
        # Add to the variable list
        target = None  # Placeholder; modify as needed based on your actual board structure
        variables.append((var_names, operator, target))

    constraints = []  # Constraints to be added to CSP

    # Create constraints based on the operator
    for var_names, operator, target in variables:
        if operator == "+":
            constraint = create_sum_constraint(var_names, target)
        elif operator == "-":
            constraint = create_difference_constraint(var_names, target)
        elif operator == "*":
            constraint = create_multiplication_constraint(var_names, target)
        elif operator == "/":
            constraint = create_division_constraint(var_names, target)
        else:
            raise ValueError(f"Unsupported operator {operator}")
        
        constraints.append(constraint)

    # Create the CSP with the variables and constraints
    csp = CSP(var_dict)
    for constraint in constraints:
        csp.add_constraint(constraint)

    return csp, variables


def create_sum_constraint(var_names, target_sum):
    """
    Creates a sum constraint for the given variables.
    """
    satisfying_tuples = []
    for combination in itertools.product(range(1, 10), repeat=len(var_names)):
        if sum(combination) == target_sum:
            satisfying_tuples.append(combination)
    
    constraint = Constraint("sum", var_names)
    constraint.add_satisfying_tuples(satisfying_tuples)
    return constraint


def create_difference_constraint(var_names, target_difference):
    """
    Creates a difference constraint for the given variables.
    """
    satisfying_tuples = []
    for combination in itertools.product(range(1, 10), repeat=len(var_names)):
        if abs(combination[0] - combination[1]) == target_difference:
            satisfying_tuples.append(combination)
    
    constraint = Constraint("difference", var_names)
    constraint.add_satisfying_tuples(satisfying_tuples)
    return constraint


def create_multiplication_constraint(var_names, target_product):
    """
    Creates a multiplication constraint for the given variables.
    """
    satisfying_tuples = []
    for combination in itertools.product(range(1, 10), repeat=len(var_names)):
        if math.prod(combination) == target_product:
            satisfying_tuples.append(combination)
    
    constraint = Constraint("multiplication", var_names)
    constraint.add_satisfying_tuples(satisfying_tuples)
    return constraint


def create_division_constraint(var_names, target_quotient):
    """
    Creates a division constraint for the given variables.
    """
    satisfying_tuples = []
    for combination in itertools.product(range(1, 10), repeat=len(var_names)):
        if combination[1] != 0 and combination[0] / combination[1] == target_quotient:
            satisfying_tuples.append(combination)
    
    constraint = Constraint("division", var_names)
    constraint.add_satisfying_tuples(satisfying_tuples)
    return constraint