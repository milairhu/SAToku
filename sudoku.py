"""
Sudoku SAT-Solver
As part of IA02 course, taught at UTC by Sylvain Lagrue
"""

from typing import List, Tuple
import itertools
import pprint
import subprocess

# alias de types
Variable = int
Literal = int
Clause = List[Literal]
Model = List[Literal]
Clause_Base = List[Clause]
Grid = List[List[int]]

example: Grid = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9],
]


example2: Grid = [
    [0, 0, 0, 0, 2, 7, 5, 8, 0],
    [1, 0, 0, 0, 0, 0, 0, 4, 6],
    [0, 0, 0, 0, 0, 9, 0, 0, 0],
    [0, 0, 3, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 5, 0, 2, 0],
    [0, 0, 0, 8, 1, 0, 0, 0, 0],
    [4, 0, 6, 3, 0, 1, 0, 0, 9],
    [8, 0, 0, 0, 0, 0, 0, 0, 0],
    [7, 2, 0, 0, 0, 0, 3, 1, 0],
]


empty_grid: Grid = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
]

#### Functions provided by Mr. Lagrue


def write_dimacs_file(dimacs: str, filename: str):
    with open(filename, "w", newline="") as cnf:
        cnf.write(dimacs)


def exec_gophersat(
    filename: str, cmd: str = "gophersat", encoding: str = "utf8"
) -> Tuple[bool, List[int]]:
    result = subprocess.run(
        [cmd, filename], capture_output=True, check=True, encoding=encoding
    )
    string = str(result.stdout)
    lines = string.splitlines()

    if lines[1] != "s SATISFIABLE":
        return False, []

    model = lines[2][2:].split(" ")

    return True, [int(x) for x in model]



#### Personal work
    
def cell_to_variable(i: int, j: int, val: int) -> int:
    res=0
    for a in range (0, i):
        for b in range (0,9):
            for z in range (1,10):
                res=res+1
    #on est mtn à la bonne ligne
    for b in range (0,j):
        for z in range (1,10):
                res=res+1
    
    #on est bonne ligne + bonne colonne
    for z in range (1, val+1):
        res=res+1
        
    return res
                
def variable_to_cell(var: int) -> Tuple[int, int, int]:
    v=0
    for i in range (0,9):
        for j in range (0,9):
            for val in range (1,10):
                v=v+1
                if (v==var):
                    return (i,j,val)
                
#revoir           
def at_least_one(vars: List[int]) -> List[int] : ## retourne un ou des var, donc retourne la liste?
    res=[]
    for i in vars:
        res.append(i)
    return res


def unique(vars: List[int]) -> List[List[int]] :
    liste=[]
    liste.append(at_least_one(vars))
    
    for i in itertools.combinations(vars,2):
        l=[]
        l.append(-1*i[0])
        l.append(-1*i[1])
        liste.append(l)
    return liste
    

def create_cell_constraints() -> List[List[int]]:
    liste=[]
    
    for i in range(0,9):
        for j in range(0,9):
            binf=cell_to_variable(i,j,1)
            bsup=cell_to_variable(i,j,9)
           
                
            nv_clause=[]
            nv_clause=unique(range(binf,bsup+1 ))
            liste=liste+nv_clause
    return liste
def create_line_constraints() -> List[List[int]]:
    liste=[]
    
    for val in range (1,10):
        
        for i in range (0,9):
            nv_clause= []
            for j in range (0,9):
                
                nv_clause.append(cell_to_variable(i,j,val))
            liste.append(nv_clause)
    return liste
                
            
                
        
    
def create_column_constraints() -> List[List[int]]:
    liste=[]
    
    for val in range (1,10):
        
        for j in range (0,9):
            nv_clause= []
            for i in range (0,9):
                
                nv_clause.append(cell_to_variable(i,j,val))
            liste.append(nv_clause)
    return liste
                
def create_box_constraints() -> List[List[int]]:
    res=[]
    for l in range(1,4):
        for c in range (1,4):
            for val in range (1,10):
                nv_clause=[]
                for i in range (l*3-3,l*3):
                    for j in range (c*3-3, c*3):
                        nv_clause.append(cell_to_variable(i,j,val))
                res.append(nv_clause)
    return res



def create_value_constraints(grid: List[List[int]]) -> List[List[int]]:
    liste=[]
    for i in range (0,9):
        for j in range(0,9):
            if (grid[i][j] != 0):
                clause=[]
                clause.append((cell_to_variable(i,j,grid[i][j])))
                liste.append(clause)
    return liste

def generate_problem(grid: List[List[int]]) -> List[List[int]] :

    res=[]
    res=res+create_value_constraints(grid)
    res=res+create_box_constraints()
    res=res+create_cell_constraints()
    res=res+create_column_constraints()
    res=res+create_line_constraints()

    return res

problem=generate_problem(example)
#print(problem)
def clauses_to_dimacs(clauses: List[List[int]], nb_vars: int) ->str:
    res=""
    res=res+"c TP3 IA02\n"
    res = res + "c SUDOKU\nc\n"
    res = res + "p cnf "+str(nb_vars)+" "+str(len(clauses))+"\n"

    for clause in clauses:
    
     
        for i in clause:
            res=res+str(i)+" "
        res=res+"0 \n"

    return res
dimacs=clauses_to_dimacs(problem,729) #729 variables

def write_dimacs_file(dimacs: str,filename: str):
    f=open(filename,"w")
    f.write(dimacs)
    f.close()
write_dimacs_file(dimacs,"sudoku.cnf")


exec_gophersat("sudoku.cnf","../gophersat")

def model_to_grid(model: List[int], nb_vals: int = 9) -> List[List]: 
    grid=empty_grid

    for litt in model[1] :
        if litt >0:
            case=variable_to_cell(litt)
        
            grid[case[0]][case[1]]=case[2]

    return grid


#### Run codes


#Exemple1
pb1=generate_problem(example)
dimacsex1=clauses_to_dimacs(pb1,729)

write_dimacs_file(dimacsex1,"sudoku1.cnf")
modelex1=exec_gophersat("sudoku1.cnf","../gophersat")

gridex1=model_to_grid(modelex1)

pprint.pprint(gridex1)


#Exemple2
#pb2=generate_problem(example2)
#dimacsex2=clauses_to_dimacs(pb2,729)
#write_dimacs_file(dimacsex2,"sudoku2.cnf")
#modelex2=exec_gophersat("sudoku2.cnf","../gophersat")

#gridex2=model_to_grid(modelex2)

#pprint.pprint(gridex2)



def main():
    pass


if __name__ == "__main__":
    main()
