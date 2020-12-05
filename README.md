# Tic-Tac-Toe
A simple implementation of a Q-Learning AI for Tic-Tac-Toe in Python. The algorithm learns to play perfectly by simulating many games against itself, and eventually produces an optimal policy.

### Goals
After learning Python this summer, I wanted to take on a miniature challenge that combined both my interests in AI with my love for building things. Because of the game's incredibly small state-space, Tic-Tac-Toe ended up being a great way to learn the basics of tabular Q-Learning, while at the same time allowing me to quickly check and see if the algorithm was working or not. Some of my lower-level goals for this project were:
*  To reinforce my understanding of Python.
*  To learn the basics of the Pygame module.
*  To understand Q-Learning and how to apply it to a real project.
*  To try and use good coding practices for projects (like increasing code-reuse, reducing global variables, keeping everything well-documented, seperating functionality into different classes, etc.).
*  To implement okay-ish looking graphics using Pygame (things like game-tiles changing color on mouse-over, hover-buttons, and a generally clean-looking interface).

### Improvements
Q_learning is a relatively simple algorithm in machine learning, and cannot be used on problems with larger state-spaces (for example: Chess, or Connect-Four), because of the exponential increase in computational complexity (Tic-Tac-Toe alone boasts around 18,000 possible board-states). When I attempted to apply this technique to a connect-four prototype that I built in Python, I immediately noticed poor performance after training for roughly 3-4 hours. I then realized that Connect-Four has a state-space around 4,000,000,000,000 and that my feeble laptop could only train about 2 million games every few hours. This led to the realization that it would take my laptop 900 years to simply *cover* Connect-Four's state-space. Yikes! So, something that could potentially be improved in future is the learning model. Specifically, upgrading to Deep-Q-Learning seems like the best way to fix this issue (and learn more about RL!).

### Acknowledgements
Much of my initial success in implementing Q-Learning with Python can be attributed to a handful of Medium articles on the subject. [One article](https://towardsdatascience.com/reinforcement-learning-implement-tictactoe-189582bea542), in particular, was especially helpful when I was first getting started.

### Screenshots
.
<img src="https://github.com/dodobird181/TicTacToe-QLearning/blob/main/images/menu.PNG" width="300" height="300">

<img src="https://github.com/dodobird181/TicTacToe-QLearning/blob/main/images/tie.PNG" width="300" height="300">

<img src="https://github.com/dodobird181/TicTacToe-QLearning/blob/main/images/xwins.PNG" width="300" height="300">

### Download
Finally, if you want to try out my Tic-Tac-Toe AI for yourself, feel free to [download](https://github.com/dodobird181/Tic-Tac-Toe/raw/main/build/TicTacToe.zip) a portable version for Windows.
