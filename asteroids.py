# Example file showing a basic pygame "game loop"
import pygame
import random
import math

# pygame setup
pygame.init()
screen = pygame.display.set_mode((500, 600))
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

# Configurações dos disparos
bullets = []
bullet_speed = 400  # pixels por segundo
bullet_radius = 5   # tamanho do disparo

# Função para criar um novo disparo
def create_bullet():
    """Cria um novo disparo na posição atual do jogador"""
    return {
        'pos': pygame.Vector2(player_pos.x, player_pos.y),
        'direction': pygame.Vector2(0, -1),  # Dispara para cima
        'active': True
    }

# Função para atualizar os disparos
def update_bullets(dt):
    """Atualiza a posição dos disparos e verifica colisões com asteroids"""
    global bullets, asteroids
    
    bullets_to_remove = []
    asteroids_to_remove = []
    
    for i, bullet in enumerate(bullets):
        if not bullet['active']:
            continue
            
        # Move o disparo
        bullet['pos'] += bullet['direction'] * bullet_speed * dt
        
        # Verifica se o disparo saiu da tela
        if (bullet['pos'].x < 0 or bullet['pos'].x > screen.get_width() or 
            bullet['pos'].y < 0 or bullet['pos'].y > screen.get_height()):
            bullets_to_remove.append(i)
            continue
        
        # Verifica colisão com asteroids
        bullet_rect = pygame.Rect(bullet['pos'].x - bullet_radius, 
                                 bullet['pos'].y - bullet_radius, 
                                 bullet_radius * 2, bullet_radius * 2)
        
        for j, asteroid in enumerate(asteroids):
            asteroid_rect = pygame.Rect(asteroid['pos'].x - asteroid['size'], 
                                       asteroid['pos'].y - asteroid['size'], 
                                       asteroid['size'] * 2, asteroid['size'] * 2)
            
            if bullet_rect.colliderect(asteroid_rect):
                # Marca o disparo e o asteroid para remoção
                bullets_to_remove.append(i)
                if j not in asteroids_to_remove:  # Evita duplicatas
                    asteroids_to_remove.append(j)
                break
    
    # Remove elementos marcados (do último para o primeiro para evitar problemas de índice)
    for index in sorted(bullets_to_remove, reverse=True):
        if index < len(bullets):
            bullets.pop(index)
    
    for index in sorted(asteroids_to_remove, reverse=True):
        if index < len(asteroids):
            asteroids.pop(index)


# Função para criar um novo asteroid
def create_asteroid():
    # Escolhe um lado aleatório para spawnar (cima, esquerda ou direita)
    side = random.choice(['top', 'left', 'right'])
    
    if side == 'top':
        x = random.randint(0, screen.get_width())
        y = -30  # pouco acima da tela
    elif side == 'left':
        x = -30  # pouco à esquerda da tela
        y = random.randint(0, screen.get_height()//2)
    else:  # right
        x = screen.get_width() + 30  # pouco à direita da tela
        y = random.randint(0, screen.get_height()//2)
    
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
        # Dispara quando a barra de espaço é pressionada
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullets.append(create_bullet())


    # Atualiza o timer de spawn
    #func asteroid spawn
    asteroid_spawn_timer += dt
    if asteroid_spawn_timer >= asteroid_spawn_interval and len(asteroids) < max_asteroids:
        asteroids.append(create_asteroid())
        asteroid_spawn_timer = 0

    # fill the screen with a color to wipe away anything from last frame
    screen.fill((0, 0, 0))
    player = pygame.draw.circle(screen, "red", player_pos, player_radius)
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
    # Atualiza os disparos
    update_bullets(dt)
    # Mantém o jogador dentro da tela

    
    ast = [pygame.draw.circle(screen, (255, 165, 0), a['pos'], a['size']) for a in asteroids]    
    # Desenha os disparos
    for bullet in bullets:
        pygame.draw.circle(screen, "white", bullet['pos'], bullet_radius)


    # Checa colisões
    # func collision
    for a in ast:
        if player.colliderect(a):
            game_over = True
            running = False
            print("Game Over!")
            break

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()  # Atualiza a tela