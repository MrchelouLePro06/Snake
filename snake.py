import pygame
import random

pygame.init()
screen = pygame.display.set_mode((1250, 750))
clock = pygame.time.Clock()
running = True

#Initialize font to display score
font = pygame.font.SysFont(None, 48)
fontGO = pygame.font.SysFont(None, 100)

#Snake coordinates (head)
snake_pos = pygame.Vector2(600, 350)
snake_size = (50, 50)
#Snake body
snake_body = [pygame.Vector2(snake_pos)]

#Time and move speed
speed = pygame.Vector2(50, 50)
move_delay = 120  #snake's move speed, 100 = fast, 120 = slower
lastMoveTime = pygame.time.get_ticks()

#Direction of movement
direction = None

#initial position of the apple
apple_pos = pygame.Vector2(115, 115)

#initialize the score
score = 0

#used to know if the snake ate an apple
grow = False

#used to switch between state play or game over 
game_over=False
pause=False
last_pause_time = 0

def gameOverScreen(score):
    screen.fill("black")
    go_text = fontGO.render('Game Over', True, (255, 255, 255))
    score_text = font.render(f'Score: {score}', True, (255, 255, 255))
    quit_text = font.render("C : Quit", True, (255, 0, 0))
    restart_text = font.render("R : Restart", True, (0, 255, 0))
    screen.blit(go_text, (screen.get_width() // 2 - go_text.get_width() // 2, screen.get_height() // 2 - go_text.get_height()))
    screen.blit(score_text, (screen.get_width() // 2 - score_text.get_width() // 2, screen.get_height() // 2 + go_text.get_height() // 2))
    screen.blit(quit_text, (screen.get_width() //4 - score_text.get_width() // 2, screen.get_height() // 2 + go_text.get_height()*2))
    screen.blit(restart_text, (screen.get_width() - score_text.get_width()*3, screen.get_height() // 2 + go_text.get_height()*2))
    pygame.display.flip()

def reset_game():
    global snake_pos, snake_body, direction, apple_pos, score, grow, lastMoveTime
    snake_pos = pygame.Vector2(600, 350)
    snake_body = [pygame.Vector2(snake_pos)]
    direction = None
    apple_pos = pygame.Vector2(random.randint(0, (screen.get_width() - snake_size[0]) // 50) * 50 + 15,
                                random.randint(0, (screen.get_height() - snake_size[1]) // 50) * 50 + 15)
    score = 0
    grow = False
    lastMoveTime = pygame.time.get_ticks()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    current_time = pygame.time.get_ticks()

    keys=pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE] and current_time -last_pause_time >300:
        pause=not pause
        last_pause_time = current_time

    if not game_over and not pause:
        screen.fill("green")

        #Creating lines to make boxes (grid)
        for x in range(0, screen.get_width(), 50):
            pygame.draw.line(screen, "black", (x, 0), (x, screen.get_height()))
        for y in range(0, screen.get_height(), 50):
            pygame.draw.line(screen, "black", (0, y), (screen.get_width(), y))

        #Management of keys for movement
        keys = pygame.key.get_pressed()
        if current_time - lastMoveTime > move_delay:
            if keys[pygame.K_z] and direction != "down":
                direction = "up"
            elif keys[pygame.K_d] and direction != "left":
                direction = "right"
            elif keys[pygame.K_s] and direction != "up":
                direction = "down"
            elif keys[pygame.K_q] and direction != "right":
                direction = "left"

            #Updating head position
            if direction == "up":
                snake_pos.y -= speed.y
            elif direction == "right":
                snake_pos.x += speed.x
            elif direction == "down":
                snake_pos.y += speed.y
            elif direction == "left":
                snake_pos.x -= speed.x
            
            #movement through walls managed here (-50 to avoid the invisible box at the border)
            if snake_pos.x < 0:
                snake_pos.x = screen.get_width() - 50
            if snake_pos.x > screen.get_width() - 50:
                snake_pos.x = 0
            if snake_pos.y < 0:
                snake_pos.y = screen.get_height() - 50
            if snake_pos.y > screen.get_height() - 50:
                snake_pos.y = 0

            #Add a new cube after eating an apple
            if grow:
                snake_body.append(snake_body[-1].copy())
                grow = False

            #Move the body of the snake (each cube takes the position of the previous one)
            if len(snake_body) > 1:
                for i in range(len(snake_body) - 1, 0, -1):
                    snake_body[i] = snake_body[i - 1].copy()

            #The head takes its new position
            snake_body[0] = snake_pos.copy()

            #After the movement, check if an apple is eaten
            if snake_pos.x == apple_pos.x-15 and snake_pos.y==apple_pos.y-15:
                score+=1
                #print(f"Score: {score}")
                grow = True
                apple_pos = pygame.Vector2(random.randint(0,(screen.get_width()-snake_size[0])//50)*50+15, random.randint(0,(screen.get_height()-snake_size[1])//50)*50+15)
                #print(apple_pos.x,apple_pos.y)
                pygame.draw.rect(screen, "red", pygame.Rect(apple_pos, (20, 20)))

            lastMoveTime = current_time

        #Draw the initial apple
        pygame.draw.rect(screen, "red", pygame.Rect(apple_pos, (20, 20)))
        #Draw the snake
        for cube in snake_body:
            pygame.draw.rect(screen, "black", pygame.Rect(cube, snake_size))
        
        #Collision between the snake's head and its own body
        for cube in snake_body[1:]:
            if snake_pos == cube:
                game_over=True

        #Score display on screen
        score_text = font.render(f'Score: {score}', True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

    elif pause:
        pause_text = fontGO.render('Pause', True, (255, 255, 255))
        screen.blit(pause_text, (screen.get_width() // 2 - pause_text.get_width() // 2, screen.get_height() // 2 - pause_text.get_height()))
        pygame.display.flip()

    else:
        gameOverScreen(score)
        keys=pygame.key.get_pressed()
        if keys[pygame.K_c]:
            running=False
        if keys[pygame.K_r]:
            reset_game()
            game_over=False

    #Updating the display
    pygame.display.flip()
    clock.tick(60)
pygame.quit()

"""
Next time code a Start Menu
"""