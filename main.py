import pygame
from pygame.locals import *
from random import choice, randint

pygame.init()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.frames = [ pygame.image.load('assets/graphics/Player/player_walk_1.png'), 
               pygame.image.load('assets/graphics/Player/player_walk_2.png')]
        self.current_frame = 0
        self.frame_rate = .1
        self.jump_image = pygame.image.load('assets/graphics/Player/jump.png')
        self.jump_force = -20
        self.jump_sound = pygame.mixer.Sound('assets/audio/jump.mp3')
        self.jump_sound.set_volume(.1)
        self.image = self.frames[self.current_frame]
        self.floor = 300
        self.gravity = 0
        self.rect = self.image.get_rect(midbottom=(80, self.floor))

    def user_input(self):
        keys = pygame.key.get_pressed()
        if (keys[K_SPACE] or keys[K_UP] or mouse_click) and self.rect.bottom >= self.floor:
            self.gravity = self.jump_force
            self.jump_sound.play()

    def apply_gravity(self):
        self.gravity += .9
        self.rect.y += self.gravity
        if self.rect.bottom > self.floor: self.rect.bottom = self.floor

    def animate(self):
        if self.rect.bottom >= self.floor:
            self.current_frame = (self.current_frame + self.frame_rate) % len(self.frames)
            self.image = self.frames[int(self.current_frame)]
        else: self.image = self.jump_image

    def reset(self):
        self.rect.bottom = self.floor

    def update(self):
        self.user_input()
        self.apply_gravity()
        self.animate()

class Enemy(pygame.sprite.Sprite):
    def __init__(self, floor=300):
        super().__init__()
        self.type = choice(['fly', 'snail', 'snail', 'snail'])
        if self.type == 'fly':
            self.frames = snail_frames
            y_pos = floor - 100
        else:
            self.frames = fly_frames
            y_pos = floor

        self.current_frame = 0
        self.frame_rate = .1
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect(bottomleft=(randint(900, 1100), y_pos))

    def animate(self):
        self.current_frame = (self.current_frame + self.frame_rate) % len(self.frames)
        self.image = self.frames[int(self.current_frame)]
        self.rect.x -= 5

    def update(self):
        self.animate()
        if self.rect.right <= 0:
            self.kill()

class Score():
    def __init__(self, font):
        self.start_time = pygame.time.get_ticks() // 1000
        self.current_score = 0
        self.font = font
        self.text = font.render(f'Score: {self.current_score}', False, 'black')
        self.rect = self.text.get_rect(center=(screen_width // 2, 50))

    def reset(self):
        self.current_score = 0
        self.start_time = pygame.time.get_ticks() // 1000

    def update(self):
        self.current_score = pygame.time.get_ticks() // 1000 -  self.start_time
        self.text = self.font.render(f'Score: {self.current_score}', False, 'black')

    def display(self):
        pygame.draw.rect(screen, 'skyblue', self.rect.scale_by(1.5).move(0, -5), 0, 50)
        screen.blit(self.text, self.rect)

def is_game_over():
    if pygame.sprite.spritecollide(player.sprite, enemys, False): # Check for collision
        enemys.empty() # Remove all enemys
        screen.fill('skyblue')  # Fill screen with skyblue (my favourite color <3)
        player.sprite.reset() # if player jump set it position to top of floor
        score.display() # Display score
        screen.blit(player_stand, player_stand_rect) # Display icon
        screen.blit(message, message.get_rect(center=(screen_width // 2, 310))) # Display a message
        score.reset() # Set score back to 0
        return True
    return False

# Create screen
screen_width, screen_height = 800, 400
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Pixel Runner: Escape the Obstacles')

# Upload assets

# Fonts
fonts = pygame.font.Font('assets/font/Pixeltype.ttf', 50)

# Images
sky = pygame.image.load('assets/graphics/Sky.png')
floor = pygame.image.load('assets/graphics/ground.png')
snail_frames = [pygame.image.load('assets/graphics/Fly/Fly1.png').convert_alpha(),
                pygame.image.load('assets/graphics/Fly/Fly2.png').convert_alpha()]
fly_frames = [pygame.image.load('assets/graphics/snail/snail1.png').convert_alpha(),
              pygame.image.load('assets/graphics/snail/snail2.png').convert_alpha()]
player_stand = pygame.transform.scale_by(pygame.image.load('assets/graphics/Player/player_stand.png'), 2)
player_stand_rect = player_stand.get_rect(center=(screen_width // 2, 180))
pygame.display.set_icon(player_stand)
message = fonts.render('Press R to restart', False, 'black')

# Audio
music = pygame.mixer.Sound('assets/audio/music.wav')
music.set_volume(.2)
music.play(loops=-1)

# Initialize the player
player = pygame.sprite.GroupSingle()
player.add(Player())

# Initialize enemys group
enemys = pygame.sprite.Group()
enemys.add(Enemy())

# Create Score
score = Score(fonts)

# Create event for spawning enemy every 1500ms
spawn_enemy = pygame.USEREVENT + 1
pygame.time.set_timer(spawn_enemy, 1500)

# Game loop
clock = pygame.time.Clock()
game_over = False
game_running = True
while game_running:
    for event in pygame.event.get():
        if event.type == QUIT:
            game_running = False

        if game_over:
            # Restart game if key R or mouse button pressed
            if (event.type == KEYDOWN and event.key == K_r) or event.type == MOUSEBUTTONDOWN:
                game_over = False
        else:
            if event.type == spawn_enemy: # Spawn one enemy every 1500ms
                enemys.add(Enemy())
            if event.type == MOUSEBUTTONDOWN:
                mouse_click = True
            else: mouse_click = False

    if not game_over:
        # Draw sky and floor
        screen.blit(sky, (0, 0))
        screen.blit(floor, (0, 300))

        # Draw player
        player.update()
        player.draw(screen)

        # Draw enemys
        enemys.update()
        enemys.draw(screen)

        # Draw score
        score.update()
        score.display()

        # Check if game is over
        game_over = is_game_over()

    pygame.display.update() # Update screen
    clock.tick(60) # Limit fps to 60


pygame.quit()