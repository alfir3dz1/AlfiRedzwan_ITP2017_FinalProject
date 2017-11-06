#From Paul Vincent Harvent
import math
import pygame
# Define some colors
black = (0, 0, 0)
white = (255, 255, 255)
blue = (0, 0, 255)
red = (255, 0, 0)
green = (0, 255, 0)
yellow = (255, 255, 0)
# If you complete the sets of level set the block smaller to make it a higher challenge
block_width = 1000
block_height = 15

# You have only one life, use it well
class Block(pygame.sprite.Sprite):
    def __init__(self, color, x, y):
        """ Constructor. Pass in the color of the block,
            and its x and y position. """

        # Call the parent class (Sprite) constructor
        super().__init__()

        # Create the image of the block of appropriate size
        # The width and height are sent as a list for the first parameter.
        self.image = pygame.Surface([block_width, block_height])

        # Fill the image with the appropriate color
        self.image.fill(color)

        # Fetch the rectangle object that has the dimensions of the image
        self.rect = self.image.get_rect()

        # Move the top left of the rectangle to x,y.
        # This is where our block will appear..
        self.rect.x = x
        self.rect.y = y


class Ball(pygame.sprite.Sprite):
    """ This class represents the ball
        It derives from the "Sprite" class in Pygame """

    # Speed in pixels per cycle
    speed = 10.0

    # Floating point representation of where the ball is
    x = 200.0
    y = 300.0

    # Direction of ball (in degrees)
    direction = 200

    width = 10
    height = 10

    # Constructor. Pass in the color of the block, and its x and y position
    def __init__(self):
        # Call the parent class (Sprite) constructor
        super().__init__()

        # Create the image of the ball
        self.image = pygame.Surface([self.width, self.height])

        # Color the ball
        self.image.fill(white)

        # Get a rectangle object that shows where our image is
        self.rect = self.image.get_rect()

        # Get attributes for the height/width of the screen
        self.screenheight = pygame.display.get_surface().get_height()
        self.screenwidth = pygame.display.get_surface().get_width()


    def bounce(self, diff):
        """ This function will bounce the ball
            off a horizontal surface (not a vertical one) """

        self.direction = (180 - self.direction) % 360
        self.direction -= diff

    def update(self):
        """ Update the position of the ball. """
        # Sine and Cosine work in degrees, so we have to convert them
        direction_radians = math.radians(self.direction)

        # Change the position (x and y) according to the speed and direction
        self.x += self.speed * math.sin(direction_radians)
        self.y -= self.speed * math.cos(direction_radians)

        # Move the image to where our x and y are
        self.rect.x = self.x
        self.rect.y = self.y

        # Do we bounce off the top of the screen?
        if self.y <= 0:
            self.bounce(0)
            self.y = 1

        # Do we bounce off the left of the screen?
        if self.x <= 0:
            self.direction = (360 - self.direction) % 360
            self.x = 1

        # Do we bounce of the right side of the screen?
        if self.x > self.screenwidth - self.width:
            self.direction = (360 - self.direction) % 360
            self.x = self.screenwidth - self.width - 1

        # Did we fall off the bottom edge of the screen?
        if self.y > 800:
            return True
        else:
            return False


class Player(pygame.sprite.Sprite):
    """ This class represents the bar at the bottom that the
    player controls. """

    def __init__(self):
        """ Constructor for Player. """
        # Call the parent's constructor
        super().__init__()

        self.width = 75
        self.height = 15
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill((white))

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.screenheight = pygame.display.get_surface().get_height()
        self.screenwidth = pygame.display.get_surface().get_width()

        self.rect.x = 0
        self.rect.y = self.screenheight-self.height

    def update(self):
        """ Update the player position. """
        # Get where the mouse is
        pos = pygame.mouse.get_pos()
        # Set the left side of the player bar to the mouse position
        self.rect.x = pos[0]
        # Make sure we don't push the player paddle
        # off the right side of the screen
        if self.rect.x > self.screenwidth - self.width:
            self.rect.x = self.screenwidth - self.width

# Call this function so the Pygame library can initialize itself
file = '5th Symphony Metal Version.mp3'
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load(file)
pygame.mixer.music.play()
sound = pygame.mixer.Sound("break3.wav")
effect = pygame.mixer.Sound("Paddle ball hit 1.wav")
# Setup the screen display
screen = pygame.display.set_mode([1200, 750])

# One life, no HUD display, how far will you go? Finish the level and you will proceed by manually inputting the settings as you advance. Difficulty ranges from Beginner to Insane
pygame.display.set_caption('Hardcore Brick Breaker')

# Enable this to make the mouse disappear when over our window
pygame.mouse.set_visible(0)

# This is a font we use to draw text on the screen (size 36)
font = pygame.font.Font(None, 36)

# Create a surface we can draw on
background = pygame.Surface(screen.get_size())

# Create sprite lists
blocks = pygame.sprite.Group()
balls = pygame.sprite.Group()
allsprites = pygame.sprite.Group()

# Create the player paddle object
player = Player()
allsprites.add(player)

# Create the ball
ball = Ball()
allsprites.add(ball)
balls.add(ball)

# The top of the block (y position)
top = 2

# Setup the blocks from the first level until it's game over. If you complete the level you can setup the blockcount for a new challenge
blockcount = 1

# --- Create blocks

# Set the number of rows from the lowest to the highest starting for the first level
for row in range(5):
    # Columns according to the size of the screen
    for column in range(0, blockcount):
        # Create a block (color,x,y)
        block = Block(blue, column * (block_width + 2) + 1, top)
        blocks.add(block)
        allsprites.add(block)
    # Move the top of the next row down
    top += block_height + 2

# Clock to limit speed
clock = pygame.time.Clock()

# Is the game over?
game_over = False

# Exit the program?
exit_program = False

# Main program loop
while not exit_program:

    # Limit to 30 fps
    clock.tick(30)
    # Clear the screen
    screen.fill(black)
    # Process the events in the game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit_program = True


    # Update the ball and player position as long
    # as the game is not over.
    if not game_over:
        # Update the player and ball positions
        player.update()
        game_over = ball.update()

    # If th
    if game_over:
        text = font.render("Game Over", True, red)
        textpos = text.get_rect(centerx=background.get_width()/2)
        textpos.top = 300
        screen.blit(text, textpos)

    # See if the ball hits the player paddle
    if pygame.sprite.spritecollide(player, balls, False):
        effect.play()
        #If you hit the paddle even on the right angle it will bounce randomly
        diff = (player.rect.x + player.width/2) - (ball.rect.x+ball.width/2)
        #Don't ever try to hit the paddle on the edge other wise it will be hard to bounce back
        ball.rect.y = screen.get_height() - player.rect.height - ball.rect.height - 1
        ball.bounce(diff)

    deadblocks = pygame.sprite.spritecollide(ball, blocks, True)

    if len(deadblocks) > 0:
        sound.play()
        ball.bounce(0)
        print("hit")
        # Level ends and sets up manually for the next level
        if len(blocks) == 0:
            game_over = True
            text = font.render("Congratulations", True, blue)
            textpos = text.get_rect(centerx=background.get_width()/2)
            textpos.top = 300
            screen.blit(text, textpos)

            print("Great, now try setting up the difficulty")
            # Cooldown and setting up the game harder. Notice that it takes time to set up
            # Please note that HUD for the score is OFF

    allsprites.draw(screen)

    pygame.display.flip()

pygame.quit()

#I put / which means the first is when the game is not over and the second is when the game is over. Count your score in your mind after finishing a level or when game over. Only count the final score if the game is over(sum of bricks in every level)

if len(blocks) == 0:
    c = input("Current score")#You have to remember what's previous score in the previous level after level 2 and so on
    print(c)
#If you quit or game over calculate the final score from the current level and the score of the previous level
Final = input("Final score")#Total of hits on the command
print(Final + "\nGame over")
