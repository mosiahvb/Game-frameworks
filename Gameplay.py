# Importing Tools to be used in the software.
import pygame
import random
pygame.init()

# Setting dimensions for the display box 
WIDTH = 700 
HEIGHT = 500
# Creating the display window and Window title
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

# set speed four frames per second/the speed of the game
FPS = 60

# Variables to hold COLORS!
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Paddle and ball Variables
PADDLE_WIDTH = 20
PADDLE_HEIGHT = 100
BALL_SIZE = 8

# Font for Scoreboard and needed points to win
FONT = pygame.font.SysFont("Times New Roman", 45)
NEEDED_TO_WIN = 10

# Paddle design specifications
class Paddle:

    # speed of paddle
    speed = 4

    # Initializing positions and attributes for paddles
    def __init__(self, x, y, width, height):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.width = width
        self.height = height
        self.color = WHITE

    # Creates the paddle on the screen
    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))

    # Inputs for paddles ability to move up and down
    def move(self, up=True):
        if up:
            self.y -= self.speed
        else:
            self.y += self.speed

    # Receipts the paddle to beginning position 
    # and sets the color back to white
    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.color = WHITE  

# ball movement and attributes
class Ball:
    speed = 5

    def __init__(self, x, y, radius):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.radius = radius
        self.x_spe = self.speed
        self.y_spe = 0
        self.color = WHITE

    # Displays the ball on the screen.
    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)

    
    def move(self):
        self.x += self.x_spe
        self.y += self.y_spe

    # resent the ball in the middle of your screen after every point
    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.y_spe = 0
        self.x_spe *= -1
        
        
# Creating the Design and aesthetics of the game.
def draw(window, paddles, ball, left_score, right_score):
    
    # Color of the background
    window.fill(BLACK)

    # Score board for right and left sids
    right_score_text = FONT.render(f"{right_score}", 1, WHITE)
    window.blit(right_score_text, (WIDTH * (3 / 4) - right_score_text.get_width() // 2, 20))
    left_score_text = FONT.render(f"{left_score}", 1, WHITE)
    window.blit(left_score_text, (WIDTH // 4 - left_score_text.get_width() // 2, 20))
    
    # Screen divider
    for i in range(10, HEIGHT, HEIGHT // 20):
        if i % 2 == 1:
            continue
        # creats the ashes between both players 
        pygame.draw.rect(window, WHITE, (WIDTH // 2 - 5, i, 10, HEIGHT // 20))

    # Displays the paddles 
    for paddle in paddles:
        paddle.draw(window)

    #  draws the ball
    ball.draw(window)

    pygame.display.update()

#Ball movement 
def handle_collision(ball, left_paddle, right_paddle):

    # identifies if the ball hits the top or bottom of the window
    if ball.y + ball.radius >= HEIGHT:
        ball.y_spe *= -1
    elif ball.y - ball.radius <= 0:
        ball.y_spe *= -1

    # Identifying if the ball hits the left paddle, Then redirecting
    # its movement. First, the checks, if it's within the height of the
    # paddle then it Identifies what part it hits, then redirects the ball.
    if ball.x_spe < 0:
        if ball.y >= left_paddle.y and ball.y <= left_paddle.y + left_paddle.height:
            if ball.x - ball.radius <= left_paddle.x + left_paddle.width:
                ball.x_spe *= -1
                middle_y = left_paddle.y + left_paddle.height / 2
                difference_in_y = middle_y - ball.y
                reduction_factor = (left_paddle.height / 2) / ball.speed
                y_spe = difference_in_y / reduction_factor
                ball.y_spe = -1 * y_spe
                # changes color of the paddle after being hit.
                left_paddle.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    # actions for when the ball hits the right battle. This is a mirror of the 
    # left paddle program above
    else:
        if ball.y >= right_paddle.y and ball.y <= right_paddle.y + right_paddle.height:
            if ball.x + ball.radius >= right_paddle.x:
                ball.x_spe *= -1
                middle_y = right_paddle.y + right_paddle.height / 2
                difference_in_y = middle_y - ball.y
                reduction_factor = (right_paddle.height / 2) / ball.speed
                y_spe = difference_in_y / reduction_factor
                ball.y_spe = -1 * y_spe

                right_paddle.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

def handle_paddle_movement(keys, left_paddle, right_paddle):
    
    # movement of the left paddle up and down with W & S,
    # Preventing the paddle from Moving lower than the window
    if keys[pygame.K_w] and left_paddle.y - left_paddle.speed >= 0:
        left_paddle.move(up=True)
    if keys[pygame.K_s] and left_paddle.y + left_paddle.speed + left_paddle.height <= HEIGHT:
        left_paddle.move(up=False)

    # The right side paddle moving up and down.
    if keys[pygame.K_UP] and right_paddle.y - right_paddle.speed >= 0:
        right_paddle.move(up=True)
    if keys[pygame.K_DOWN] and right_paddle.y + right_paddle.speed + right_paddle.height <= HEIGHT:
        right_paddle.move(up=False)


def main():
    # Specifications for attributes of the pong game
    run = True
    clock = pygame.time.Clock()
    left_paddle = Paddle(10, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
    right_paddle = Paddle(WIDTH - 10 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
    ball = Ball(WIDTH // 2, HEIGHT // 2, BALL_SIZE)

    left_score = 0
    right_score = 0

    # Loop that runs the again as long as run = true
    while run:
        clock.tick(FPS)
        
        # calls the draw function to create the game visuals
        draw(WINDOW, [left_paddle, right_paddle], ball, left_score, right_score)

        # Stops running the program after exiting the game window.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        # Calls the function for left and right Paddle movement
        keys = pygame.key.get_pressed()
        handle_paddle_movement(keys, left_paddle, right_paddle)

        # Call is the function for ball movement based off of
        # paddle Interaction with the ball
        ball.move()
        handle_collision(ball, left_paddle, right_paddle)

        # Scoring a point- When the ball it's the other players 
        # wall (equals less than zero on the X coordinates) a 
        # points added to the score
        if ball.x < 0:
            right_score += 1
            ball.reset()
        elif ball.x > WIDTH:
            left_score += 1
            ball.reset()

        # A winner is picked after needed to win hits 10 or 
        # Whatever you set as Needed to win. then the winning 
        # side is Displayed
        won = False
        if left_score >= NEEDED_TO_WIN:
            won = True
            win_text = "Left Side Won!"
        elif right_score >= NEEDED_TO_WIN:
            won = True
            win_text = "Right Side Won!"

        # When won = true, The winner is displayed, and the game resets after
        # 4 seconds and starts again 
        if won:
            text = FONT.render(win_text, 1, WHITE)
            WINDOW.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
            pygame.display.update()
            pygame.time.delay(4000)
            ball.reset()
            left_paddle.reset()
            right_paddle.reset()
            left_score = 0
            right_score = 0

    pygame.quit()

if __name__ == '__main__':
    main()