import pygame
import time
import random

snake_speed = 15

#window size
win_x = 720
win_y = 480

#defining colors
black = pygame.Color(0,0,0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255,0,0)
green = pygame.Color(0,255,0)
blue = pygame.Color(0,0,255)

#initialize pygame
pygame.init()

#initialize game window
pygame.display.set_caption('Snakes')
game_window = pygame.display.set_mode((win_x, win_y))

#fps
fps = pygame.time.Clock()

#define snake's default position
snake_pos = [100,50]

#define first 4 blocks of snake
#body
snake_body = [ [100,50],
               [90,50],
               [80,50],
               [70,50]
]

#fruit position
fruit_position = [
    random.randrange(1, (win_x//10)) * 10,
    random.randrange(1, (win_y//10)) * 10
]

fruit_spawn = True

#set default snake direction to right
direction = 'RIGHT'
change_to = direction

#initial score
score = 0 

#displaying score func
def show_score(choice, color, font, size):

    #creating font object
    #render method is used in Pygame for displaying text
    score_font = pygame.font.SysFont(font, size)

    #creating display surface object
    score_surface = score_font.render('Score : ' + str(score), True, color)
    #True: This parameter typically specifies whether or not you want to use anti-aliasing (smoothing) on the text. 
    #If set to True, it applies anti-aliasing, which makes the text look smoother.

    #rectangular object for text surface object
    score_rect = score_surface.get_rect()

    #display text
    #blit method is used to copy contents of one surface to another surface
    #this places the rendered text on the game window specified by score_rect
    game_window.blit(score_surface, score_rect)

#game over function
def game_over():

    my_font = pygame.font.SysFont('times new roman', 50)

    game_over_surface = my_font.render('Your score is :' + str(score), True, red)

    game_over_rect = game_over_surface.get_rect()

    #setting position of text
    game_over_rect.midtop = (win_x/2, win_y/4)

    game_window.blit(game_over_surface, game_over_rect)
    pygame.display.flip()
    #flip()is used to update the contents of the display surface and make any changes visible on the screen.

    #quit the program after 2s
    time.sleep(2)

    #deactivate pygame lib
    pygame.quit()

    #quit the program
    quit()

#driver code
while True:
    #KEYDOWN used to indicate that a key is pressed
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:   
            if event.key == pygame.K_UP:
                change_to = 'UP'
            if event.key == pygame.K_DOWN:
                change_to = 'DOWN'
            if event.key == pygame.K_LEFT:
                change_to = 'LEFT'
            if event.key == pygame.K_RIGHT:
                change_to = 'RIGHT'


    #if two keys pressed simultaneously, then don't move snake in two directions
    #This condition checks if the desired direction of movement is 'UP' and the current direction is not 'DOWN'. If both conditions are met, it sets the direction to 'UP'. This ensures that if the character is currently moving downwards ('DOWN'), 
    #it won't immediately change its direction to 'UP', which would cause it to reverse.
    if change_to == 'UP' and direction != 'DOWN':
        direction = 'UP'
    
    if change_to == 'DOWN' and direction != 'UP':
        direction = 'DOWN'

    if change_to == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'

    if change_to == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'

    #move the snake
    #snake_position[1] indicate y-coordinate
     #snake_position[0] indicate x-coordinate
    if direction == 'UP':
        snake_pos[1] -= 10

    if direction == 'DOWN':
        snake_pos[1] += 10

    if direction == 'LEFT':
        snake_pos[0] -= 10
    
    if direction == 'RIGHT':
        snake_pos[0] += 10

    #snake body growing mechanism
    #if fruits and snakes collide then scores will be incremented by 10

    #inserts a copy of the current snake_pos (snake's head position) as 
    #the first element of the snake_body list. 
    snake_body.insert(0, list(snake_pos))

    if snake_pos[0] == fruit_position[0] and snake_pos[1] == fruit_position[1]:
        score += 10
        fruit_spawn = False
    
    #This line removes the last element of the snake_body list. Since a new segment was added to 
    #the front of the snake, removing the last segment simulates the snake moving forward.
    else:
        snake_body.pop()

    if not fruit_spawn:
        fruit_position = [random.randrange(1, (win_x//10)) * 10,
                          random.randrange(1, (win_y//10)) * 10
                          ]
    fruit_spawn = True
    #fills the game window with a black background, typically at the beginning of a new frame in your game loop. This is a common 
    #practice to clear the previous frame's content before drawing the updated game state.
    game_window.fill(black)

    #used to draw snake and fruit
    for pos in snake_body:
        pygame.draw.rect(game_window, green, pygame.Rect(
            pos[0], pos[1], 10, 10
        ))
    
    pygame.draw.rect(game_window, white, pygame.Rect(
        fruit_position[0], fruit_position[1], 10, 10
    ))

    #game-over condition

    #If the x-coordinate is less than 0 (i.e., the snake has gone beyond the left boundary) or greater than the width of 
    #the game window minus 10 (i.e., the snake has gone beyond the right boundary), it calls game_over().

    #If the y-coordinate is less than 0 (i.e., the snake has gone beyond the top boundary) or greater than the height of 
    #the game window minus 10 (i.e., the snake has gone beyond the bottom boundary), it calls game_over().
    if snake_pos[0] < 0 or snake_pos[0] > win_x-10:
        game_over()
    if snake_pos[1] < 0 or snake_pos[1] > win_y-10:
        game_over()


    #touching the snake body
    for block in snake_body[1:]:
        if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
            game_over()

    #Within the loop, this condition checks if the x-coordinate of the snake's head (snake_pos[0]) 
    #is equal to the x-coordinate of the current block (block[0]), and if the y-coordinate of the snake's head (snake_pos[1]) is equal to the y-coordinate of the current block (block[1]).

    #If both conditions are met, it means that the snake's head has collided with one of the blocks in its body, 
    # indicating that the game is over.

    #displaying score continuously
    show_score(1, white, 'times new roman', 20)

    #refresh game screen
    pygame.display.update()

    #fps
    fps.tick(snake_speed)
    #The tick() method of the Clock class is used to control the frame rate by adding a delay between frames. 
    #In this case, snake_speed is the desired frame rate in frames per second.

