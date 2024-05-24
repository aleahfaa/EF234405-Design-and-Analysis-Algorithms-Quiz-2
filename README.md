<div align="center">
  <h1>Design and Analysis of Algorithms - EF234405 (2024)</h1>
</div>

<p align="center">
  <b>Institut Teknologi Sepuluh Nopember</b><br>
  Sepuluh Nopember Institute of Technology
</p>

<p align="center">
  <img src="Badge_ITS.png" width="50%">
</p>

## Project Overview

This project is a computer program developed as part of [Quiz 2](https://drive.google.com/file/d/1ileQVv-8C4LQUtaw9evw9a-BjgzmcHKO/view?usp=sharing) for the Design and Analysis of Algorithms class. The program is a collaborative effort by the following contributors:

<div align="center">

|    NRP     |      Name      |
|:----------:|:--------------:|
| 5025221067 | [Syalbia Noor Rahmah](https://github.com/syalbianoor) |
| 5025221068 | [Areta Athayayumna Arwaa](https://github.com/aretaath) |
| 5025221077 | [Iffa Amalia Sabrina](https://github.com/aleahfaa) |

</div>

On behalf of:

**Ir. M.M. Irfan Subakti, S.Kom., M.Sc.Eng., M.Phil., IPM (Sr. Pro. Eng.)**



---

# Snake Game

This repository contains a Snake game implemented using `tkinter` for graphics and `pygame` for sound effects. The game includes manual control as well as AI control using the A* algorithm.

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Game Mechanics](#game-mechanics)
- [Algorithms Used](#algorithms-used)
- [Documentation](#documentation)

## Features
- Interactive graphical interface using `tkinter`
- Sound effects using `pygame`
- Manual snake control via keyboard
- AI snake control using the A* algorithm
- Scoring system with high score tracking using SQLite

## Installation

### Prerequisites
- Python 3.x
- `tkinter` library (usually included with Python)
- `pygame` library
- `sqlite3` library (usually included with Python)

### Steps
1. Clone the repository:
    ```sh
    git clone https://github.com/aleahfaa/EF234405-Design-and-Analysis-Algorithms-Quiz-2.git
    cd code
    ```

2. Install the required Python packages:
    ```sh
    pip install pygame
    ```

3. Ensure that `tkinter` is installed. For most systems, `tkinter` is included with Python. If not, you may need to install it manually.

## Usage
To start the game, simply run the `snake_game.py` script:
```sh
python snakeastar.py
```

## Game Mechanics
- **Movement**: Use the arrow keys to control the snake's direction.
- **AI Control**: Press 'a' to toggle AI control on or off.
- **Objective**: Eat the red food to grow the snake and increase your score.
- **Game Over**: The game ends if the snake collides with the wall or itself. Your score is saved and the highest score is displayed.


## Algorithms Used

### A* Algorithm
- The AI uses the A* algorithm to find the shortest path from the snake to the food, avoiding obstacles.
- The heuristic used is the Manhattan distance, which calculates the distance between two points on a grid.

### Manhattan Heuristic
- Used in the A* algorithm to compute the cost of moving from the current position to the food.

## Code Explanation

### Main Game Loop
The main loop initializes the game, sets up the window, and handles the drawing and updating of game elements.

### Event Binding
- `change_direction(event)`: Handles manual direction changes based on keyboard input.
- `toggle_ai_control(event)`: Toggles the AI control on and off.

### A* Pathfinding
The `a_star` function calculates the shortest path from the snake to the food using the A* algorithm.


## Documentation
![2 (2)](https://github.com/aleahfaa/EF234405-Design-and-Analysis-Algorithms-Quiz-2/assets/112534174/67a12e2a-8b9b-4e69-8f85-2eaf2d7379c8)
![3 (2)](https://github.com/aleahfaa/EF234405-Design-and-Analysis-Algorithms-Quiz-2/assets/112534174/7a3995a1-5d9c-4c06-b023-e209c0db7de3)
