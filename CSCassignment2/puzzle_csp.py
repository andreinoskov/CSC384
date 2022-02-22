#Look for #IMPLEMENT tags in this file.
'''
All models need to return a CSP object, and a list of lists of Variable objects 
representing the board. The returned list of lists is used to access the 
solution. 

For example, after these three lines of code

    csp, var_array = caged_csp_model(board)
    solver = BT(csp)
    solver.bt_search(prop_FC, var_ord)

var_array[0][0].get_assigned_value() should be the correct value in the top left
cell of the FunPuzz puzzle.

The grid-only models do not need to encode the cage constraints.

1. binary_ne_grid (worth 10/100 marks)
    - A model of a FunPuzz grid (without cage constraints) built using only 
      binary not-equal constraints for both the row and column constraints.

2. nary_ad_grid (worth 10/100 marks)
    - A model of a FunPuzz grid (without cage constraints) built using only n-ary 
      all-different constraints for both the row and column constraints. 

3. caged_csp_model (worth 25/100 marks) 
    - A model built using your choice of (1) binary binary not-equal, or (2) 
      n-ary all-different constraints for the grid.
    - Together with FunPuzz cage constraints.

'''
from cspbase import *
import itertools

def acceptable(possvalue, varlist, row, col):
    size = len(varlist)
    for i in range(col):
        varlist[i][col].domain() == [possvalue]
        return False
    for j in range(row):
        if varilist[row][j].domain() == [possvalue]:
            return False
    return True

def genvalue( t1 , t2, rang):
    result = []
    product = itertools.product(t1, t2)
    for prod in product:
        if prod in rang:
            result.append(prod)
    return result
    

def binary_ne_grid(fpuzz_grid):
    # initialize a variable list
    varrow = []
    varcol = []
    varlist = []
    conlist = []

    # create a variable for each position in the table
    size = fpuzz_grid[0][0]
    lispos = [i for i in range(1, size + 1)]
    
    for col in range(size):
        varrow.append([])
        varcol.append([])
        for row in range(size):
            variable = Variable("Var{}{}".format(col,row), lispos)
            varlist.append(variable)
            varrow[col].append(0)
            varcol[col].append(0)

    for col in range(size):
        for row in range(size):
            for var in varlist:
                x = "Var{}{}"
                if var.name == x.format(col,row):
    
                    varrow[row][col] = var
                    varcol[col][row] = var
    

    boardcsp = CSP('binary', varlist)
    compare = []

    for i in lispos:
        lispos2 = lispos[:]
        lispos2.remove(i)
        compare += zip([i]*(len(lispos)-1), lispos2)

    for lis in varcol + varrow:
        for var in lis:
            lis2 = lis[:]
            lis2.remove(var)
            for var2 in lis2:
                con = Constraint("Con{}{}".format(var, var2), [var, var2])
                con.add_satisfying_tuples(compare)
                boardcsp.add_constraint(con)
                
    return boardcsp, varrow
                
    
    

    
    

def nary_ad_grid(fpuzz_grid):
    varrow = []
    varcol = []
    varlist = []
    conlist = []

    # create a variable for each position in the table
    size = fpuzz_grid[0][0]
    lispos = [i for i in range(1, size + 1)]
    
    for col in range(size):
        varrow.append([])
        varcol.append([])
        for row in range(size):
            variable = Variable("Var{}{}".format(col,row), lispos)
            varlist.append(variable)
            varrow[col].append(0)
            varcol[col].append(0)

    for col in range(size):
        for row in range(size):
            for var in varlist:
                x = "Var{}{}"
                if var.name == x.format(col,row):
    
                    varrow[row][col] = var
                    varcol[col][row] = var
    

    boardcsp = CSP('narray', varlist)
    rowcomp = list(itertools.permutations(lispos, size))
 
    for lis in varcol + varrow:
        con = Constraint(f"{lis}", lis)
        con.add_satisfying_tuples(rowcomp)
        boardcsp.add_constraint(con)
                
    return boardcsp, varrow
                
    
def prod(row):
    value = 1
    for i in row:
        value = value * i
    return value

def caged_csp_model(fpuzz_grid):
    boardcsp , varrow = binary_ne_grid(fpuzz_grid)
    lispos = [i for i in range(1, fpuzz_grid[0][0] + 1)]
    for cage in fpuzz_grid[1:]:
        if cage[-1] == 0:
            size = len(cage) - 2
            rowcomp = list(itertools.product(lispos,repeat = size))
            colcomp = []
            for row in rowcomp:
                if sum(row) == cage[-2]:
                    colcomp.append(row)
            varlist = []
            for var in cage[0:size]:
                varlist.append(varrow[var // 10 - 1][var%10-1])

            con = Constraint(f"{varlist}", varlist)
            con.add_satisfying_tuples(colcomp)
            boardcsp.add_constraint(con)
        
        if cage[-1] == 1:
            size = len(cage) - 2
            rowcomp = list(itertools.product(lispos,repeat =size))
            colcomp = []
            for row in rowcomp:
                if 2*max(row) - sum(row) == cage[-2]:
                    colcomp.append(row)
            varlist = []
            for var in cage[0:size]:
                varlist.append(varrow[var // 10 - 1][var%10-1])

            con = Constraint(f"{varlist}", varlist)
            con.add_satisfying_tuples(colcomp)
            boardcsp.add_constraint(con)
        
                
        if cage[-1] == 3:
            size = len(cage) - 2
            rowcomp = list(itertools.product(lispos,repeat = size))
            colcomp = []
            for row in rowcomp:
                if prod(row) == cage[-2]:
                    colcomp.append(row)
            varlist = []
            for var in cage[0:size]:
                varlist.append(varrow[var // 10 - 1][var%10-1])

            con = Constraint(f"{varlist}", varlist)
            con.add_satisfying_tuples(colcomp)
            boardcsp.add_constraint(con)

        if cage[-1] == 2:
            size = len(cage) - 2
            rowcomp = list(itertools.product(lispos,repeat = size))
            colcomp = []
            for row in rowcomp:
                if max(row)**2 / prod(row) == cage[-2]:
                    colcomp.append(row)
            varlist = []
            for var in cage[0:size]:
                varlist.append(varrow[var // 10 - 1][var%10-1])

            con = Constraint(f"{varlist}", varlist)
            con.add_satisfying_tuples(colcomp)
            boardcsp.add_constraint(con)
        
                

        
        
    return boardcsp, varrow
    
