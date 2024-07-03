# SAToku : A SAT-based Sudoku solver

SAToku is a SAT-based Sudoku solver developed in Python. It uses the [Gophersat](https://github.com/crillab/gophersat) solver. This project was initiated as a part of the course **IA02** taught at the University of Technology of Compiègne (UTC) by **Prof. Sylvain Lagrue**, in 2022. 

## Functionnalities

SAToku can solve any 9x9 Sudoku grid. The resulting grid is displayed in the terminal and in a Tkinter window, highlighting added numbers in green.

When solving the grid, SAToku creates a CNF formula representing the Sudoku grid, whose DIMACS is stored in a *cnf* folder. The DIMACS file is then passed to Gophersat, which returns the solution. The solution is then displayed in the same Tkinter window used for the entires. A V1 version of the program reads the grid from a file given in command line, while current version allows the user to enter the grid directly in the Tkinter

## Usage

To solve a Sudoku grid, simply run the following command:

```bash
python satoku.py
```

The user can fill the grid by clicking on the cells and typing the number given by the problem. The user can let the other cells empty or fill them with 0. By clicking on the button, a DIMACS file is created and the empty cells filled with solution are highlighted in green.

In V1, the file given in argument must be a file containing the grid. The grid must be a file formatted stricly as follows:

- 9 lines, each containing 9 digits separated by spaces.
- Empty cells are represented by a 0.

## Areas of improvement

- The program could include the generation of Sudoku grids and eventually the solution.
- Visual improvements.

