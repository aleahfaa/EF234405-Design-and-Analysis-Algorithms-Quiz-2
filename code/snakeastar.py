import tkinter as tk
import random
import sqlite3
import pygame
from queue import PriorityQueue

row = 25
column = 25
tileSize = 25

windowWidth = tileSize * column
windowHeight = tileSize * row

pygame.mixer.init()

eat_sound = pygame.mixer.Sound("eat.wav")
gameOver_sound = pygame.mixer.Sound("die.wav")

class Tile:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __lt__(self, other):
        return (self.x, self.y) < (other.x, other.y)

def setup_database():
    conn = sqlite3.connect('snake_game.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS scores (score INTEGER)''')
    conn.commit()
    conn.close()

def save_score(score):
    conn = sqlite3.connect('snake_game.db')
    c = conn.cursor()
    c.execute('INSERT INTO scores (score) VALUES (?)', (score,))
    conn.commit()
    conn.close()

def get_highest_score():
    conn = sqlite3.connect('snake_game.db')
    c = conn.cursor()
    c.execute('SELECT MAX(score) FROM scores')
    result = c.fetchone()
    conn.close()
    return result[0] if result[0] is not None else 0

def game_init():
    global snake, food, velocityX, velocityY, snakeBody, gameOver, score, ai_control
    snake = Tile(random.randint(1, column - 2) * tileSize, random.randint(1, row - 2) * tileSize)
    food = Tile(random.randint(1, column - 2) * tileSize, random.randint(1, row - 2) * tileSize)
    velocityX = 0
    velocityY = 0
    snakeBody = []
    gameOver = False
    score = 0
    ai_control = False

def setup_window():
    global window, canvas
    window = tk.Tk()
    window.title("Snake")
    window.resizable(False, False)
    canvas = tk.Canvas(window, bg="black", width=windowWidth, height=windowHeight, borderwidth=0, highlightthickness=0)
    canvas.pack()
    # center the window
    window.update_idletasks()
    window_width = window.winfo_width()
    window_height = window.winfo_height()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    window_x = (screen_width - window_width) // 2
    window_y = (screen_height - window_height) // 2
    window.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")

def change_direction(event):
    global velocityX, velocityY, gameOver, ai_control
    if gameOver:
        game_init()
        return
    # disable ai control when user provides input
    ai_control = False
    if event.keysym == "Up" and velocityY == 0:
        velocityX = 0
        velocityY = -1
    elif event.keysym == "Down" and velocityY == 0:
        velocityX = 0
        velocityY = 1
    elif event.keysym == "Left" and velocityX == 0:
        velocityX = -1
        velocityY = 0
    elif event.keysym == "Right" and velocityX == 0:
        velocityX = 1
        velocityY = 0

def toggle_ai_control(event):
    global ai_control
    ai_control = not ai_control

def heuristic(a, b):
    return abs(a.x - b.x) + abs(a.y - b.y)

def a_star(start, goal, obstacles):
    open_set = PriorityQueue()
    open_set.put((0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}
    while not open_set.empty():
        _, current = open_set.get() 
        if current.x == goal.x and current.y == goal.y:
            path = []
            while current in came_from:
                current = came_from[current]
                path.append(current)
            return path[::-1]  # return reversed path
        neighbors = [
            Tile(current.x + tileSize, current.y),
            Tile(current.x - tileSize, current.y),
            Tile(current.x, current.y + tileSize),
            Tile(current.x, current.y - tileSize)
        ]
        for neighbor in neighbors:
            if (neighbor.x, neighbor.y) in obstacles or neighbor.x < tileSize or neighbor.x >= windowWidth - tileSize or neighbor.y < tileSize or neighbor.y >= windowHeight - tileSize:
                continue
            tentative_g_score = g_score[current] + 1
            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = g_score[neighbor] + heuristic(neighbor, goal)
                open_set.put((f_score[neighbor], neighbor))
    return []

def move():
    global snake, food, snakeBody, gameOver, score, ai_control
    if gameOver:
        return
    if ai_control:
        obstacles = {(tile.x, tile.y) for tile in snakeBody}
        path = a_star(snake, food, obstacles)
        if path:
            next_move = path[0]
            snake.x, snake.y = next_move.x, next_move.y
        else:
            gameOver = True
            gameOver_sound.play()
            return
    else:
        snake.x += velocityX * tileSize
        snake.y += velocityY * tileSize
    # check for wall collision with the border
    if snake.x < tileSize or snake.x >= windowWidth - tileSize or snake.y < tileSize or snake.y >= windowHeight - tileSize:
        gameOver = True
        gameOver_sound.play()
        return
    # check for self collision
    for tile in snakeBody:
        if snake.x == tile.x and snake.y == tile.y:
            gameOver = True
            gameOver_sound.play()
            return
    # check for food collision
    if snake.x == food.x and snake.y == food.y:
        snakeBody.append(Tile(food.x, food.y))
        food.x = random.randint(1, column - 2) * tileSize
        food.y = random.randint(1, row - 2) * tileSize
        score += 1
        eat_sound.play()
    # update snake body
    if snakeBody:
        snakeBody = [Tile(snake.x, snake.y)] + snakeBody[:-1]
    
def draw_border():
    for i in range(column):
        # top border
        canvas.create_rectangle(i * tileSize, 0, (i + 1) * tileSize, tileSize, fill='gray')
        # bottom border
        canvas.create_rectangle(i * tileSize, (row - 1) * tileSize, (i + 1) * tileSize, row * tileSize, fill='gray')
    for j in range(row):
        # left border
        canvas.create_rectangle(0, j * tileSize, tileSize, (j + 1) * tileSize, fill='gray')
        # right border
        canvas.create_rectangle((column - 1) * tileSize, j * tileSize, column * tileSize, (j + 1) * tileSize, fill='gray')

def draw():
    global snake, food, snakeBody, gameOver, score
    move()
    canvas.delete("all")
    draw_border()
    # draw food
    canvas.create_oval(food.x, food.y, food.x + tileSize, food.y + tileSize, fill='red')
    # draw snake head
    canvas.create_rectangle(snake.x, snake.y, snake.x + tileSize, snake.y + tileSize, fill='yellow')
    # draw snake body
    for tile in snakeBody:
        canvas.create_rectangle(tile.x, tile.y, tile.x + tileSize, tile.y + tileSize, fill='lime green')
    # display score and game over message
    if gameOver:
        highest_score = get_highest_score()
        save_score(score)
        if score > highest_score:
            message = f"Game Over\nScore: {score}\nNew Highest Score"
        else:
            message = f"Game Over\nScore: {score}\nHighest Score: {highest_score}"
        canvas.create_text(windowWidth / 2, windowHeight / 2, font="Arial 20", text=message, fill="white", anchor=tk.CENTER, justify="center")
    else:
        canvas.create_text(30, 20, font="Arial 10", text=f"Score: {score}", fill="white")
    window.after(100, draw)

setup_database()
game_init()
setup_window()
draw()
window.bind("<KeyRelease>", change_direction)
window.bind("a", toggle_ai_control)
window.mainloop()
