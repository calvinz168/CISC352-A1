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

def cagey_csp_model(cagey_grid):
    ##IMPLEMENT
     n, cages = cagey_grid
    csp, var_array = binary_ne_grid(cagey_grid)  # or nary_ad_grid if needed

    for value, cells, op in cages:
        vars_in_cage = [var_array[i][j] for (i, j) in cells]
        if op == '+': # addition constraint
            c = Constraint(f"Cage_Add_{cells}", vars_in_cage)
            c.add_satisfying_tuples(
                [(tuple(val) for val in zip(*[var.domain() for var in vars_in_cage])) if sum(val) == value else None for val in zip(*[var.domain() for var in vars_in_cage])]
            )
            csp.add_constraint(c)
        elif op == '*': # creates constraint for multiplication
            c = Constraint(f"Cage_Mul_{cells}", vars_in_cage)
            c.add_satisfying_tuples(
                [(tuple(val) for val in zip(*[var.domain() for var in vars_in_cage])) if product(val) == value else None for val in zip(*[var.domain() for var in vars_in_cage])]
            )
            csp.add_constraint(c)

    return csp, var_array
