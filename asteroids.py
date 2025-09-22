# Example file showing a basic pygame "game loop"
import pygame
import random
import math

# pygame setup
pygame.init()
screen = pygame.display.set_mode((500, 720))
clock = pygame.time.Clock()
running = True
game_over = False
dt = 0


#player meta
player_pos = pygame.Vector2(
    #posicionado no centro do eixox
    screen.get_width()/2, 
    #posicionado um pouco acima do fim da tela (10% da tela)                        
    screen.get_height() -screen.get_height() / 10 
    )
player_radius = 20

# Configurações dos asteroids
asteroids = []
asteroid_spawn_timer = 0
asteroid_spawn_interval = 2.0  # segundos entre cada spawn
asteroid_speed = 100  # pixels por segundo
max_asteroids = 10    # número máximo de asteroids na tela


# Função para criar um novo asteroid
def create_asteroid():
    # Escolhe um lado aleatório para spawnar (cima, esquerda ou direita)
    side = random.choice(['top', 'left', 'right'])
    
    if side == 'top':
        x = random.randint(0, screen.get_width())
        y = -30  # pouco acima da tela
    elif side == 'left':
        x = -30  # pouco à esquerda da tela
        y = random.randint(0, screen.get_height()/2)
    else:  # right
        x = screen.get_width() + 30  # pouco à direita da tela
        y = random.randint(0, screen.get_height()/2)
    
    # Tamanho aleatório entre 15 e 35 pixels
    size = random.randint(15, 35)
    
    return {
        'pos': pygame.Vector2(x, y),
        'size': size,
        'speed': asteroid_speed * (25/size)  # Asteroids maiores são mais lentos
    }

# Função para atualizar os asteroids
def update_asteroids(dt):
    global asteroids
    
    # Atualiza a posição de cada asteroid em direção ao jogador
    for asteroid in asteroids:
        # Calcula a direção para o jogador
        direction = player_pos - asteroid['pos']
        if direction.length() > 0:  # Evita divisão por zero
            direction.normalize_ip()
        
        # Move o asteroid
        asteroid['pos'] += direction * asteroid['speed'] * dt
    
    # Remove asteroids que saíram da tela
    asteroids = [a for a in asteroids if (
        0 - a['size'] <= a['pos'].x <= screen.get_width() + a['size'] and
        0 - a['size'] <= a['pos'].y <= screen.get_height() + a['size']
    )]


while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    # Atualiza o timer de spawn
    #func asteroid spawn
    asteroid_spawn_timer += dt
    if asteroid_spawn_timer >= asteroid_spawn_interval and len(asteroids) < max_asteroids:
        asteroids.append(create_asteroid())
        asteroid_spawn_timer = 0

    # fill the screen with a color to wipe away anything from last frame
    screen.fill((0, 0, 0))
    pygame.draw.circle(screen, "red", player_pos, player_radius)
    # RENDER YOUR GAME HERE

    # Movimento lateral do jogador
    # func player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        player_pos.x -= 300 * dt
    if keys[pygame.K_d]:
        player_pos.x += 300 * dt
    player_pos.x = max(player_radius, min(screen.get_width() - player_radius, player_pos.x))

    # Atualiza os asteroids
    update_asteroids(dt)
    # Mantém o jogador dentro da tela

    

    # Desenha os asteroids (esferas laranja)
    for asteroid in asteroids:
        pygame.draw.circle(screen, (255, 165, 0), asteroid['pos'], asteroid['size'])

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()  # Atualiza a tela