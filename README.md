# Sudoko AI

Once you start training machine learning models, it's easy to forget that not all AI needs to use a model trained on a GPU. Training neural networks to solve difficult problems is really cool, but I think it's become common for people to over-engineer simple problems. This repository is a good example of an AI that requires zero training data and can solve the puzzles quickly and with 100% accuracy. 

### What is Sudoku

Sudoku was created in 1979 by Howard Garns, a semi-retired puzzle creator from Indiana. The earlist predecessor to Sudoku was a game called Numbers, which appeared in French newspapers throughout the 1800s. While similar to Sudoku, Numbers involved arithmatic instead of logic to solve and there were sometimes double-digit numbers. 

Unfortunately, Howard Garns died before his invention took off. In the mid-late 1980s a Japenese newspaper started publishing the puzzle regularly and Maki Kaji gave it the name Sudoku. It wasn't until the late 1990s and early 2000s that Sudoku made its way back to the States and spread throughout the rest of the world.

### How do you play

Sudoku is played on a 9x9 grid which is also separated into 9 3x3 sections. The objective of the game is to figure out how to put the digits 1-9 on the grid so that each digit appears exactly once in each row, column, and 3x3 section. The game will start off with a handful of squared filled out; these are locked in. In general, the fewer sections that start off filled, the more difficult the game is. Of course, there is a critical point whereby once you get down to too few squares filled out there becomes many correct solutions and the game becomes easier again. 

![Sudoku](/assets/sudoku.png)

### Using this repository

Feel free to use this repository however you like, whether you want to use it to learn, for a Sudoku app, or to solve a pesky Sudoku puzzle you're stuck on. Using the code is pretty simple. 

First, you'll need to translate the Sudoku puzzle you're interested in solving into a one-dimensional string where empty squares are represented by a ".". You'll read the Sudoku puzzle left-to-right and down the page like a book to get it into the proper grid format.

```
grid = '8..........36......7..9.2...5...7.......457.....1...3...1....68..85...1..9....4..'
```

Next, you'll create a Sudoku puzzle with the grid string by instantiating a Sudoku object.

```
puzzle = Sudoku(grid)
```

The solver AI can be instantiated in the same way and can be used to solve multiple Sudoku puzzles.

```
solver = SudokuSolver()
```

Finally, pass the puzzle into the Sudoku AI. It should print the solution to sdout.

```
solver.solve(puzzle)
```

For more examples and use cases, check out the tests file.

# Connect with me

If you'd like to collaborate on a project, learn more about me, or just say hi, feel free to contact me using any of the social channels listed below.

- [Personal Website](https://zackthoutt.com)
- [Email](mailto:zackarey.thoutt@colorado.edu)
- [LinkedIn](https://www.linkedin.com/in/zack-thoutt-57275655/)
- [Twitter](https://twitter.com/zthoutt)
- [Medium](https://medium.com/@zthoutt)
- [Quora](https://www.quora.com/profile/Zack-Thoutt)
- [HackerNews](https://news.ycombinator.com/submitted?id=zthoutt)
- [Reddit](https://www.reddit.com/user/zthoutt/)
- [Kaggle](https://www.kaggle.com/zynicide)
- [Instagram](https://www.instagram.com/zthoutt/)
- [500px](https://500px.com/zthoutt)
