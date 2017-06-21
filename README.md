# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

This is the first assignment in the first term of Udacity's Artificial Intelligence Nanodegree.  Our tasks were: 

0. Implement the functions in `solutions.py`

0. Answer the follwoing questions


# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: The "naked twins" contraint says that if two cells in one unit both contain the same two values then those two values cannot be in any other cell in that unit.  By searching each unit for "naked twins" and then removing those digits from all the peers in the unit we can further reduce the search space and therefore solve the puzzle faster.  As with elimiate and only_choice this new constraint should be applied in sequence repeatedly until no further reductions can be made.

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: The additional constraints of adding the two main diagonals to the existing set of units make the puzzle harder to solve. The underlying set of techniques (only choice, elimination, and naked twins) still apply in the same way but with these additional constraints as well.


### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solutions.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the ```assign_values``` function provided in solution.py

### Data

The data consists of a text file of diagonal sudokus for you to solve.
