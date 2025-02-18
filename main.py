import pygame
from sys import exit
from random import randint

# Configuration 
pygame.init()
pygame.display.set_caption("Flappy Bird 2.0")
screen = pygame.display.set_mode((400, 600))
clock = pygame.time.Clock()

# Background
background = pygame.image.load('ressource/image/background-night.png').convert_alpha()
background_rect = background.get_rect(center=(200, 300))
base = pygame.image.load('ressource/image/base.png').convert_alpha()
player = pygame.image.load('ressource/image/redbird-midflap.png').convert_alpha()

# Vérifier les dimensions de l'image pour qu'elles soient parfaitement adaptées à la fenêtre 
background = pygame.transform.scale(background, (400, 600))
base = pygame.transform.scale(base, (400, 100))

# Game over surface
game_over = pygame.image.load('ressource/image/gameover.png').convert_alpha()
game_over_rect = game_over.get_rect(center=(200, 300))

# Start surface
start_message = pygame.image.load('ressource/image/message.png').convert_alpha()
start_message_rect = start_message.get_rect(center=(200, 300))

# Charger la police Arial
font = pygame.font.SysFont('Poppins', 50)

# Charger les images des chiffres
score_images = [
    pygame.image.load('ressource/image/0.png').convert_alpha(),
    pygame.image.load('ressource/image/1.png').convert_alpha(),
    pygame.image.load('ressource/image/2.png').convert_alpha(),
    pygame.image.load('ressource/image/3.png').convert_alpha(),
    pygame.image.load('ressource/image/4.png').convert_alpha(),
    pygame.image.load('ressource/image/5.png').convert_alpha(),
    pygame.image.load('ressource/image/6.png').convert_alpha(),
    pygame.image.load('ressource/image/7.png').convert_alpha(),
    pygame.image.load('ressource/image/8.png').convert_alpha(),
    pygame.image.load('ressource/image/9.png').convert_alpha()
]

# Variables pour contrôler l'état de game_over et le score final
game_over_state = False
final_score = 0

# Fonction pour afficher le score
def display_score():
    if not game_over_state:
        current_time = int(pygame.time.get_ticks() / 1000) - start_time
        draw_score(current_time)
        print(f'Votre score est de: {current_time}')
    else:
        draw_score(final_score)  # Affiche le score final

# Fonction pour dessiner le score en utilisant des images
def draw_score(score):
    score_str = str(score)
    total_width = sum(score_images[int(digit)].get_width() for digit in score_str)
    x_offset = (400 - total_width) // 2

    for digit in score_str:
        digit_image = score_images[int(digit)]
        screen.blit(digit_image, (x_offset, 50))
        x_offset += digit_image.get_width()

# Fonction pour réinitialiser la position du tuyau
def reset_pipe(pipe_rect, inverted=False):
    pipe_rect.left = 400
    if inverted:
        pipe_rect.bottom = randint(100, 300)
    else:
        pipe_rect.top = randint(350, 400)

# Fonction pour réinitialiser le jeu
def reset_game():
    global player_rect, player_gravity, pipe_green_rect, pipe_green_inverted_rect, score, start_time, game_active, music_sound, show_start_message, game_over_state, final_score
    player_rect = player.get_rect(midleft=(50, 300))
    player_gravity = 0
    pipe_green_rect = pipe_green.get_rect(midleft=(400, 450))
    pipe_green_inverted_rect = pipe_green_inverted.get_rect(midleft=(400, 0))
    score = 0
    start_time = pygame.time.get_ticks() // 1000
    game_active = True
    show_start_message = False
    game_over_state = False
    music_sound.stop()
    music_sound.play(-1)
    music_sound.set_volume(0.1)

def check_time():
    global start_time
    elapsed_time = pygame.time.get_ticks() // 1000 - start_time
    return elapsed_time >= 25
    elapsed_time50 = pygame.time.get_ticks() // 1000 - start_time
    return elapsed_time50 >= 50
# Rectangle
player_rect = player.get_rect(midleft=(50, 300))

# Gravité
player_gravity = 0


# Score
score = 0
start_time = pygame.time.get_ticks() // 1000

# Positions initiales du fond et du sol
background_x = 0
base_x = 0

# Obstacle
pipe_green = pygame.image.load('ressource/image/pipe-green.png').convert_alpha()
pipe_green_rect = pipe_green.get_rect(midleft=(400, 450))

# Obstacle inversé
pipe_green_inverted = pygame.transform.flip(pipe_green, False, True)
pipe_green_inverted_rect = pipe_green_inverted.get_rect(midleft=(400, 0))

# Son
jump_sound = pygame.mixer.Sound('ressource/sound/jump.wav')
jump_sound.set_volume(0.2)
music_sound = pygame.mixer.Sound('ressource/sound/music.wav')
music_sound.play(-1)
game_over_sound = pygame.mixer.Sound('ressource/sound/gameover_sound.wav')
# Initialisation de game_active
game_active = False

# Variable pour contrôler l'affichage du message de démarrage
show_start_message = True

# Boucle 
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print("Fermeture du jeu")
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if show_start_message:
                    game_active = True
                    show_start_message = False
                    start_time = pygame.time.get_ticks() // 1000
                elif not game_active:
                    reset_game()
                player_gravity = -3.7
                jump_sound.play()
                print('Jump')

    screen.blit(background, (0, 0))

    if game_active:
        player_gravity += 0.2
        player_rect.y += player_gravity

        # Condition 1: Collision avec les tuyaux
        if player_rect.colliderect(pipe_green_rect) or player_rect.colliderect(pipe_green_inverted_rect):
            game_active = False
            game_over_state = True
            final_score = int(pygame.time.get_ticks() / 1000) - start_time  # Stocker le score final
            print('Collision sur un tuyaux détectée')
            game_over_sound.play()
            game_over_sound.set_volume(0.1)
            print('Pas mal le score mais tu à toucher un tuyaux :=)')
            print('Pourquoi pas recommencer, non ? :)')

        # Condition 2: Collision avec le sol
        if player_rect.bottom >= 500:
            game_active = False
            game_over_state = True
            final_score = int(pygame.time.get_ticks() / 1000) - start_time  # Stocker le score final
            print('Une collision vers le sol a été détectée')
            game_over_sound.play()
            game_over_sound.set_volume(0.1)
            print('Pas mal le score mais tu à toucher le sol :=)')
            print('Pourquoi pas recommencer, non ? :)')

        # Condition 3: Collision avec le plafond
        if player_rect.top <= 0:
            game_active = False 
            game_over_state = True
            final_score = int(pygame.time.get_ticks() / 1000) - start_time  # Stocker le score final
            print('Une collision vers le haut a été détectée')
            game_over_sound.play()
            game_over_sound.set_volume(0.1)
            print('Pas mal le score mais tu à toucher le plafond :=)')
            print('Pourquoi pas recommencer, non ? :)')

        if game_active:
            # Définir un certains volume pour le son music.wav
            music_sound.set_volume(0.1)

        # Condition 4: Mise à jour des tuyaux
        pipe_speed = 3 if check_time() else 2
        pipe_green_rect.x -= pipe_speed
        pipe_green_inverted_rect.x -= pipe_speed
        pipe_speed = 5 if check_time() else 2
        pipe_green_rect.x -= pipe_speed
        pipe_green_inverted_rect.x -= pipe_speed
        # Réinitialisation des tuyaux lorsqu'ils sortent de l'écran
        if pipe_green_rect.right <= 0:
            reset_pipe(pipe_green_rect)
        if pipe_green_inverted_rect.right <= 0:
            reset_pipe(pipe_green_inverted_rect, inverted=True)

        screen.blit(base, (0, 500))
        screen.blit(base, (base_x, 500))

        screen.blit(pipe_green, pipe_green_rect)
        screen.blit(pipe_green_inverted, pipe_green_inverted_rect)

        screen.blit(player, player_rect)
        display_score()

    else:
        if not show_start_message:
            # Afficher "Game Over"
            screen.blit(game_over, game_over_rect)
            # Afficher le score de "Game Over"
            game_over_score = font.render(f'Votre Score est de : {final_score}', True, (255, 255, 255))
            game_over_score_rect = game_over_score.get_rect(center=(200, 350))
            screen.blit(game_over_score, game_over_score_rect)
        
        if show_start_message:
            screen.blit(start_message, start_message_rect)
            # Définir un certains volume pour le son music.wav lors du démarrage
            music_sound.set_volume(0.1)

    pygame.display.update()
    clock.tick(60)
