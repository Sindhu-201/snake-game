# Imported important libraries for GUI and random number generation
from tkinter import * 
import random

## Defined constants for the game
GAME_WIDTH =800 # Game window width
GAME_HEIGHT=500 # Game window height
SPEED=100  # Speed of the game (milliseconds between each frame)
SPACE_SIZE=25  # Speed of the game (milliseconds between each frame)
BODY_PARTS=20 # Initial size of the snake (number of body parts)
SNAKE_COLOR="green"  # Color of the snake
HEAD_COLOR = "darkgreen"   # Color of the snake's head
FOOD_COLOR="Red" # Color of the food
BACKGROUND_COLOR="#000000" # Background color of the game canvas

# Define the Snake class
class Snake:
    def __init__(self): 
       self.body_size= BODY_PARTS # Set initial size of snake
       self.coordinates=[] # List to store the coordinates of each body part
       self.squares=[] # List to store the graphical representations of the squares
      # Initialize snake's body parts at the start
       for i in range(0, BODY_PARTS):
          self.coordinates.append([0, 0]) # All body parts start at position (0, 0)

       for x,y in self.coordinates: # Create the squares on the canvas for each body part
          square=canvas.create_oval(x,y,x +  SPACE_SIZE,y + SPACE_SIZE,fill=SNAKE_COLOR,tag="snake")
          self.squares.append(square)
class Food: # Define the Food class
      def __init__(self):
         # Randomly generate food coordinates within the game area
        x = random.randint(0, (GAME_WIDTH // SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT // SPACE_SIZE) - 1) * SPACE_SIZE
        self.coordinates = [x, y] # Store food's position
        # Create the food on the canvas
        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food")

# Function to make the snake move in the next direction
def next_turn(snake,food):
    x,y=snake.coordinates[0] # Get current head position of the snake

    # Change position based on the current direction
    if direction =="up":
      y-=SPACE_SIZE
    elif direction =="down":
      y+=SPACE_SIZE
    elif direction =="left":
      x-=SPACE_SIZE
    elif direction =="right":
      x+=SPACE_SIZE
    # Insert the new head of the snake at the beginning
    snake.coordinates.insert(0,(x,y))
    square=canvas.create_oval(x, y, x +  SPACE_SIZE,y + SPACE_SIZE,fill=SNAKE_COLOR)
    snake.squares.insert(0,square)
    # Check if snake has eaten food
    if x==food.coordinates[0] and y==food.coordinates[1]:

      global score

      score+=1 # Increase score when snake eats food
      label.config(text="Score:{}".format(score)) # Update score display
      canvas.delete("food") # Remove the current food
      food=Food()  # Create a new food
    else:
      # Remove the last segment of the snake (tail)
      del snake.coordinates[-1]
      canvas.delete(snake.squares[-1])
      del snake.squares[-1]
    # Check for collisions (game over condition)
    if check_collisions(snake):
      game_over()
    else:
      # Continue the game after the specified speed interval
      window.after(SPEED,next_turn,snake,food)

def change_direction(new_direction): # Function to change the direction of the snake
    global direction 
    if new_direction == 'left':
        if direction != 'right':
            direction = new_direction
    elif new_direction == 'right':
        if direction != 'left':
            direction = new_direction
    elif new_direction == 'up':
        if direction != 'down':
            direction = new_direction
    elif new_direction == 'down':
        if direction != 'up':
            direction = new_direction

def check_collisions(snake): # Function to check if the snake has collided with walls or itself
    x, y = snake.coordinates[0]    # Get the head's position of the snake
    if x < 0 or x >= GAME_WIDTH or y < 0 or y >= GAME_HEIGHT:   # Check if out of bounds
        return True
    for body_part in snake.coordinates[1:]:  # Check if the head hits any body part
        if x == body_part[0] and y == body_part[1]:
            return True
    return False

def game_over(): # Function to handle the game over scenario
  canvas.delete(ALL)# Delete all elements on the canvas
    # Display "GAME OVER" text in the center of the canvas
  canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2, font=('consolas',70), text="GAME OVER", fill="red", tag="gameover")
  canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() / 2 + 100, font=('consolas', 30),
                       text="Press 'Enter' to Restart", fill="yellow", tag="restart")
  
  

  window.bind("<Return>", restart_game) # Bind the Enter key to restart the game
  window.bind("<Escape>", exit_game)  # Bind the Escape key to exit the game


def restart_game(event):  # Function to restart the game
    global score, direction
    score = 0 # Reset score
    direction = "down" # Reset the snake direction to "down"
    canvas.delete("gameover") # Remove game over screen
    canvas.delete("restart") # Remove restart message

    
    label.config(text="Score: {}".format(score)) # Reset score label


    snake = Snake()  # Create a new snake
    food = Food() # Create new food

    next_turn(snake, food)  # Start the game loop

    window.unbind("<Return>") # Unbind the restart key after it's pressed

def exit_game(event): # Function to exit the game
    window.quit() # Close the game window

def key_press(event): # Function to handle key press events and change the snake's direction
    if event.keysym == "Left":
        change_direction("left")
    elif event.keysym == "Right":
        change_direction("right")
    elif event.keysym == "Up":
        change_direction("up")
    elif event.keysym == "Down":
        change_direction("down")




window = Tk()  # Initialize the main window (game window)
window.title("snake game") # Set the title of the window
window.resizable(False,False)  # Make the window size fixed (non-resizable)
score=0 # Initialize score and direction
direction='down'

# Display the score at the top of the window
label=Label(window,text="score:{}".format(score),font=('consolas',40))
label.pack()

# Create the canvas where the game will be drawn
canvas = Canvas(window,bg=BACKGROUND_COLOR,height=GAME_HEIGHT,width=GAME_WIDTH)
canvas.pack()

# Center the game window on the screen
window.update()  # Update the window to get its dimensions
window_width=window.winfo_width()
window_height=window.winfo_height()
screen_width=window.winfo_screenwidth()
screen_height=window.winfo_screenheight()
x=int((screen_width/2) - (window_width/2))
y=int((screen_height/2) - (window_height/2))
window.geometry(f"{window_width}x{window_height}+{x}+{y}")  # Set the window geometry

# Create the initial snake and food objects
snake=Snake()
food=Food()

# Bind key press events to change the direction
window.bind("<Left>", key_press)
window.bind("<Right>", key_press)
window.bind("<Up>", key_press)
window.bind("<Down>", key_press)

# Start the game loop
next_turn(snake, food)

# Run the game
window.mainloop()