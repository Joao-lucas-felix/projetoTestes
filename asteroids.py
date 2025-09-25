# Example file showing a basic pygame "game loop"
import pygame
import random

class GameSetup:
    def __init__(self, dimensions=(500,600)):
        pygame.init()
        self.screen =  pygame.display.set_mode(dimensions)
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_over = False 
        self.dt = 0 
        self.screen.fill((0, 0, 0))

    def draw_objects(self, asteroids, bullets, bullet_radius): 
        ast = [pygame.draw.circle(self.screen, (255, 165, 0), a['pos'], a['size']) for a in asteroids]    
        # Desenha os disparos
        for bullet in bullets:
            pygame.draw.circle(self.screen, "white", bullet['pos'], bullet_radius)
        return ast
    
    def check_colisions(self, asteroids, player): 
        for a in asteroids:
            if player.colliderect(a):
                self.game_over = True
                self.running = False
                print("Game Over!")
                break
    def flips(self): 
        pygame.display.flip()
        self.dt = self.clock.tick(60) / 1000
class Player: 
    def __init__(self, screen):
        self.player_pos = pygame.Vector2(
            #posicionado no centro do eixox
            screen.get_width()/2, 
            #posicionado um pouco acima do fim da tela (10% da tela)                        
            screen.get_height() -screen.get_height() / 10)
        self.player_radius = 20
        self.player = pygame.draw.circle(screen, "red", self.player_pos, self.player_radius)
    
    def update_player(self, screen): 
        #Trocar depois para uma classe
        screen.fill((0, 0, 0))
        self.player = pygame.draw.circle(screen, "red", self.player_pos, self.player_radius)

    def handle_player_move(self, keys, screen, dt): 
        if keys[pygame.K_a]:
            self.player_pos.x -= 300 * dt
        if keys[pygame.K_d]:
            self.player_pos.x += 300 * dt
        self.player_pos.x = max(self.player_radius, min(screen.get_width() - self.player_radius, self.player_pos.x))

class Asteroids: 
    def __init__(self):
        self.asteroids = []
        self.asteroid_spawn_timer = 0
        self.asteroid_spawn_interval = 0.5  # segundos entre cada spawn
        self.asteroid_speed = 100  # pixels por segundo
        self.max_asteroids = 10    # número máximo de asteroids na tela
    
    # Função para criar um novo asteroid
    def create_asteroid(self, screen):
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
            'speed': self.asteroid_speed * (25/size)  # Asteroids maiores são mais lentos
        }
    #Spawna asteroids
    def  asteroid_spawn(self, dt, screen): 
        self.asteroid_spawn_timer += dt
        if self.asteroid_spawn_timer >= self.asteroid_spawn_interval and len(self.asteroids) < self.max_asteroids:
            self.asteroids.append(self.create_asteroid(screen))
            self.asteroid_spawn_timer = 0

    # Função para atualizar os asteroids
    def update_asteroids(self, dt, player_pos, screen):
        
        # Atualiza a posição de cada asteroid em direção ao jogador
        for asteroid in self.asteroids:
            # Calcula a direção para o jogador
            direction = player_pos - asteroid['pos']
            if direction.length() > 0:  # Evita divisão por zero
                direction.normalize_ip()
            
            # Move o asteroid
            asteroid['pos'] += direction * asteroid['speed'] * dt
        
        # Remove asteroids que saíram da tela
        self.asteroids = [a for a in self.asteroids if (
            0 - a['size'] <= a['pos'].x <= screen.get_width() + a['size'] and
            0 - a['size'] <= a['pos'].y <= screen.get_height() + a['size']
        )]

class Bullets: 
    def __init__(self):
        self.bullets = []
        self.bullet_speed = 400 # pixels por segundo
        self.bullet_radius = 5 # tamanho do disparo


    # Função para criar um novo disparo
    def create_bullet(self, player):
        """Cria um novo disparo na posição atual do jogador"""
        return {
            'pos': pygame.Vector2(player.player_pos.x, player.player_pos.y),
            'direction': pygame.Vector2(0, -1),  # Dispara para cima
            'active': True
        }

    # Função para atualizar os disparos
    def update_bullets(self, dt, screen, asteroids):
        """Atualiza a posição dos disparos e verifica colisões com asteroids"""
        
        bullets_to_remove = []
        asteroids_to_remove = []
        
        for i, bullet in enumerate(self.bullets):
            if not bullet['active']:
                continue
                
            # Move o disparo
            bullet['pos'] += bullet['direction'] * self.bullet_speed * dt
            
            # Verifica se o disparo saiu da tela
            if (bullet['pos'].x < 0 or bullet['pos'].x > screen.get_width() or 
                bullet['pos'].y < 0 or bullet['pos'].y > screen.get_height()):
                bullets_to_remove.append(i)
                continue
            
            # Verifica colisão com asteroids
            bullet_rect = pygame.Rect(bullet['pos'].x - self.bullet_radius, 
                                    bullet['pos'].y - self.bullet_radius, 
                                    self.bullet_radius * 2, self.bullet_radius * 2)
            
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
            if index < len(self.bullets):
                self.bullets.pop(index)
        
        for index in sorted(asteroids_to_remove, reverse=True):
            if index < len(asteroids):
                asteroids.pop(index)






# setup inicial
def game():
        
    game = GameSetup() 
    player = Player(game.screen)
    disparos = Bullets()
    asteroids = Asteroids()

    # Fluxo principal do game
    while game.running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.running = False
            # Dispara quando a barra de espaço é pressionada
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    disparos.bullets.append(disparos.create_bullet(player))

        # Atualiza o timer de spawn
        #func asteroid spawn
        asteroids.asteroid_spawn(dt=game.dt, screen=game.screen)

        # Atualiza a posição do jogador a cada frame
        player.update_player(screen=game.screen)

        # RENDER YOUR GAME HERE

        # Movimento lateral do jogador
        # func player movement
        keys = pygame.key.get_pressed()
        player.handle_player_move(keys=keys, screen=game.screen, dt=game.dt)

        # Atualiza os asteroids
        
        asteroids.update_asteroids(dt=game.dt, player_pos= player.player_pos, screen=game.screen)

        # Atualiza os disparos
        disparos.update_bullets(dt=game.dt, screen=game.screen, asteroids=asteroids.asteroids)
        # Mantém o jogador dentro da tela

        
        # faz os disparos: 
        ast = game.draw_objects(asteroids=asteroids.asteroids, bullets=disparos.bullets, bullet_radius=disparos.bullet_radius)

        # Checa colisões
        # func collision
        game.check_colisions(asteroids=ast, player=player.player)

        # flip() the display to put your work on screen
        game.flips()

    pygame.quit()  # Atualiza a tela

if __name__=="__main__": 
    game()