import pygame
import random

pygame.init()
screen = pygame.display.set_mode((1250, 750))
clock = pygame.time.Clock()
running = True

# Initialiser la police pour afficher le score
font = pygame.font.SysFont(None, 48)
fontGO = pygame.font.SysFont(None, 100)

# Coordonnées du serpent (tête)
snake_pos = pygame.Vector2(600, 350)
taille_snake = (50, 50)
# Corps du serpent
snake_body = [pygame.Vector2(snake_pos)]

# Temps et vitesse de déplacement
speed = pygame.Vector2(50, 50)
move_delay = 120  # Vitesse du serpent, 100 = rapide, 120 = plus lent
lastMoveTime = pygame.time.get_ticks()

# Direction du mouvement
direction = None

# Position initiale de la pomme
pommes_pos = pygame.Vector2(115, 115)

# Score initial
score = 0

# Ajout de la variable "grow" pour gérer l'ajout d'un cube si pomme mangé
grow = False
game_over=False
pause=False
last_pause_time = 0

def gameOverScreen(score):
    screen.fill("black")
    go_text = fontGO.render('Game Over', True, (255, 255, 255))
    score_text = font.render(f'Score: {score}', True, (255, 255, 255))
    quit_text = font.render("C : Quitter", True, (255, 0, 0))
    restart_text = font.render("R : recommencer", True, (0, 255, 0))
    screen.blit(go_text, (screen.get_width() // 2 - go_text.get_width() // 2, screen.get_height() // 2 - go_text.get_height()))
    screen.blit(score_text, (screen.get_width() // 2 - score_text.get_width() // 2, screen.get_height() // 2 + go_text.get_height() // 2))
    screen.blit(quit_text, (screen.get_width() //4 - score_text.get_width() // 2, screen.get_height() // 2 + go_text.get_height()*2))
    screen.blit(restart_text, (screen.get_width() - score_text.get_width()*3, screen.get_height() // 2 + go_text.get_height()*2))
    pygame.display.flip()

def reset_game():
    """Réinitialise les variables pour recommencer le jeu."""
    global snake_pos, snake_body, direction, pommes_pos, score, grow, lastMoveTime
    snake_pos = pygame.Vector2(600, 350)
    snake_body = [pygame.Vector2(snake_pos)]
    direction = None
    pommes_pos = pygame.Vector2(random.randint(0, (screen.get_width() - taille_snake[0]) // 50) * 50 + 15,
                                random.randint(0, (screen.get_height() - taille_snake[1]) // 50) * 50 + 15)
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

        # Création des lignes pour faire des cases (grille)
        for x in range(0, screen.get_width(), 50):
            pygame.draw.line(screen, "black", (x, 0), (x, screen.get_height()))
        for y in range(0, screen.get_height(), 50):
            pygame.draw.line(screen, "black", (0, y), (screen.get_width(), y))

        #current_time = pygame.time.get_ticks()

        # Gestion des touches pour le déplacement
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

            # Mise à jour de la position de la tête
            if direction == "up":
                snake_pos.y -= speed.y
            elif direction == "right":
                snake_pos.x += speed.x
            elif direction == "down":
                snake_pos.y += speed.y
            elif direction == "left":
                snake_pos.x -= speed.x
            
            #déplacement à travers les murs géré ici (-50 pour éviter la case invisible en bordure)
            if snake_pos.x < 0:
                snake_pos.x = screen.get_width() - 50
            if snake_pos.x > screen.get_width() - 50:
                snake_pos.x = 0
            if snake_pos.y < 0:
                snake_pos.y = screen.get_height() - 50
            if snake_pos.y > screen.get_height() - 50:
                snake_pos.y = 0

            # Ajouter un nouveau segment après avoir mangé une pomme
            if grow:
                snake_body.append(snake_body[-1].copy())
                grow = False

            # Déplacer le corps du serpent (chaque segment prend la position du précédent)
            if len(snake_body) > 1:
                for i in range(len(snake_body) - 1, 0, -1):
                    snake_body[i] = snake_body[i - 1].copy()

            # La tête prend sa nouvelle position
            snake_body[0] = snake_pos.copy()

            # Après le mouvement, vérifier si une pomme est mangée
            if snake_pos.x == pommes_pos.x-15 and snake_pos.y==pommes_pos.y-15:
                score+=1
                #print(f"Score: {score}")
                grow = True
                pommes_pos = pygame.Vector2(random.randint(0,(screen.get_width()-taille_snake[0])//50)*50+15, random.randint(0,(screen.get_height()-taille_snake[1])//50)*50+15)
                #print(pommes_pos.x,pommes_pos.y)
                pygame.draw.rect(screen, "red", pygame.Rect(pommes_pos, (20, 20)))

            lastMoveTime = current_time

        # Dessiner la pomme initiale
        pygame.draw.rect(screen, "red", pygame.Rect(pommes_pos, (20, 20)))
        # Dessiner le serpent
        for cube in snake_body:
            pygame.draw.rect(screen, "black", pygame.Rect(cube, taille_snake))
        
        # Collision entre la tête du serpent et son propre corps
        for cube in snake_body[1:]:
            if snake_pos == cube:
                game_over=True

        # Affichage du score sur l'écran
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

    # Mise à jour de l'affichage
    pygame.display.flip()
    clock.tick(60)
pygame.quit()

"""
Next time build menu pause and maybe Start Menu
"""