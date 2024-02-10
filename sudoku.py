"""
Sudoku SAT-Solver
As part of IA02 course, taught at UTC by Sylvain Lagrue
"""

import os
import tkinter as tk
from typing import List, Tuple
import itertools
import pprint
import subprocess
import sys

# alias
Variable = int
Literal = int
Clause = List[Literal]
Model = List[Literal]
Clause_Base = List[Clause]
Grid = List[List[int]]

#### Functions provided by Mr. Lagrue


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

empty_grid = [[0 for _ in range(9)] for _ in range(9)]
    
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
                
           
def at_least_one(vars: List[int]) -> List[int] : 
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

def write_dimacs_file(dimacs: str,filename: str):
    # Create the cnf directory if it doesn't exist
    os.makedirs('cnf', exist_ok=True)

    # Create the path for the file in the cnf directory
    filename = os.path.join('cnf', filename)
    with open(filename, "w", newline="") as cnf:
        cnf.write(dimacs)

def model_to_grid(model: List[int]) -> List[List]:
    grid=empty_grid

    for litt in model[1] :
        if litt >0:
            case=variable_to_cell(litt)
        
            grid[case[0]][case[1]]=case[2]

    return grid

#To convert the content of a file into a matrix of int
def convert_to_matrix(grid_file):
    lines = grid_file.strip().split('\n')
    matrix = [list(map(int, line.split())) for line in lines]
    return matrix


def draw_grid(grid, added_elements):
    root = tk.Tk()
    cell_size = 20
    canvas = tk.Canvas(root, width = cell_size*len(grid[0]), height = cell_size*len(grid))
    canvas.pack()

    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            x1 = j * cell_size
            y1 = i * cell_size
            x2 = x1 + cell_size
            y2 = y1 + cell_size
            color = "light green" if (i, j) in added_elements else "white"
            canvas.create_rectangle(x1, y1, x2, y2, fill=color)
            canvas.create_text((x1+x2)/2, (y1+y2)/2, text=str(cell))

    root.mainloop()
    
def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py <file>")
        sys.exit(1)

    file = sys.argv[1]
    filename_without_ext = os.path.splitext(os.path.basename(file))[0]
    cnf_file = filename_without_ext + ".cnf"
    with open(file, 'r') as f:
        grid_file = f.read()

    matrix = convert_to_matrix(grid_file)
    
    pb = generate_problem(matrix)
    dimacs = clauses_to_dimacs(pb, 729)

    write_dimacs_file(dimacs, cnf_file)
    cnf_file = os.path.join('cnf', cnf_file)
    model = exec_gophersat(cnf_file, "./gophersat.exe")

    grid = model_to_grid(model)

    pprint.pprint(grid)

    #Get new elements
    added_elements = []
    for i in range(9):
        for j in range(9):
            if grid[i][j] != matrix[i][j]:
                added_elements.append((i, j))
    #Draw the grid
    draw_grid(grid, added_elements)

if __name__ == "__main__":
    main()