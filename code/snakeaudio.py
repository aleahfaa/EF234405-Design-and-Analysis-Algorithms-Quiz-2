import tkinter as tk
import random
import sqlite3
import pygame

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
    global snake, food, velocityX, velocityY, snakeBody, gameOver, score
    snake = Tile(random.randint(1, column - 2) * tileSize, random.randint(1, row - 2) * tileSize)
    food = Tile(random.randint(1, column - 2) * tileSize, random.randint(1, row - 2) * tileSize)
    velocityX = 0
    velocityY = 0
    snakeBody = []
    gameOver = False
    score = 0

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
    global velocityX, velocityY, gameOver
    if gameOver:
        game_init()
        return
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

def move():
    global snake, food, snakeBody, gameOver, score
    if gameOver:
        return
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
    # move snake head
    snake.x += velocityX * tileSize
    snake.y += velocityY * tileSize

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

# initialize the game
setup_database()
game_init()
setup_window()
draw()

# bind key events to change direction
window.bind("<KeyRelease>", change_direction)
window.mainloop()