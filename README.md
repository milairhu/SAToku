# SAToku : A SAT-based Sudoku solver

SAToku is a SAT-based Sudoku solver developed in Python. It uses the [Gophersat](https://github.com/crillab/gophersat) solver. This project is a part of the course **IA02** taught at the University of Technology of Compiègne (UTC) by **Prof. Sylvain Lagrue**, in 2022.

## Functionnalities

SAToku can solve any 9x9 Sudoku grid. The resulting grid is displayed in the terminal and in a Tkinter window, highlighting added numbers in green.

When solving the grid, SAToku creates a CNF formula representing the Sudoku grid, whose DIMACS is stored in a *cnf* folder. The DIMACS file is then passed to Gophersat, which returns the solution. The solution is then displayed in the terminal and in a Tkinter window.

## Usage

To solve a Sudoku grid, simply run the following command:

```bash
python3 satoku.py <path_to_grid>
```

Where `<path_to_grid>` is the path to a file containing the Sudoku grid. The grid must be a file formatted stricly as follows:

- 9 lines, each containing 9 digits separated by spaces
- Empty cells are represented by a 0

## Example

The following command:

```bash
python3 satoku.py grid_exemples/grid1.txt
```

Will solve the following grid:

```
5 3 0 0 7 0 0 0 0
6 0 0 1 9 5 0 0 0
0 9 8 0 0 0 0 6 0
8 0 0 0 6 0 0 0 3
4 0 0 8 0 3 0 0 1
7 0 0 0 2 0 0 0 6
0 6 0 0 0 0 2 8 0
0 0 0 4 1 9 0 0 5
0 0 0 0 8 0 0 7 9
```

And display the following solution:

```
5 3 4 6 7 8 9 1 2
6 7 2 1 9 5 3 4 8
1 9 8 3 4 2 5 6 7
8 5 9 7 6 1 4 2 3
4 2 6 8 5 3 7 9 1
7 1 3 9 2 4 8 5 6
9 6 1 5 3 7 2 8 4
2 8 7 4 1 9 6 3 5
```

## Areas of improvement

- The user could enter the grid directly in a Tkinter window instead of using a file.
- The program could include the generation of Sudoku grids and eventually the solution.
