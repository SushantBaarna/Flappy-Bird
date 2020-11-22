import pygame
import sys
import random
def ground_movement():
    screen.blit(ground, (ground_x_pos, 440))
    screen.blit(ground, (ground_x_pos + 288, 440))

def create_pipe():
    random_pipe_pos = random.choice(pipe_heigt)
    bottom_pipe = pipes_surface.get_rect(midtop=(500,random_pipe_pos))
    top_pipe = pipes_surface.get_rect(midbottom=(500,random_pipe_pos - 150))
    return bottom_pipe,top_pipe

def move_pipe(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 512 :
            screen.blit(pipes_surface, pipe)
        else :
            flip_pipe = pygame.transform.flip(pipes_surface,False,True)
            screen.blit(flip_pipe,pipe)
def bird_animation():
    new_bird = bird_frame[bird_index]
    new_bird_rect = new_bird.get_rect(center = (50,bird_rec.centery))
    return  new_bird,new_bird_rect

def collison(pipes):
    for pipe in pipes:
        if bird_rec.colliderect(pipe):
            death_sound.play()
            return False

    if bird_rec.top <= -50 or bird_rec.bottom >= 440 :
        return False
    return True

def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird,-movement * 3,1)
    return new_bird

def update_score(score,highscore):
    if score > highscore:
        highscore = score
    return highscore

def score_display(game_state):
    if game_state == 'main_game':
        score_surface = game_font.render(f'Score: {(int(score))}',True,(255,255,255))
        score_rect =score_surface.get_rect(center = (144,50))
        screen.blit(score_surface,score_rect)
    if game_state == 'game_over':
        score_surface = game_font.render(f'Score: {(int(score))}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(144, 50))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render(f'High Score: {(int(highscore))}', True, (255, 255, 255))
        high_score_rect = score_surface.get_rect(center=(130, 420))
        screen.blit(high_score_surface, high_score_rect)
pygame.mixer.pre_init(frequency=44100,size =-16,channels=1)
pygame.init()

#Game Variables

gravity = 0.25
movement = 0
game_active = False
score = 0
highscore = 0
screen = pygame.display.set_mode((288,512))

game_oversurface =pygame.image.load("assets/message.png").convert_alpha()
game_oversurface_rect = game_oversurface.get_rect(center = (144,256))
clock = pygame.time.Clock()
game_font = pygame.font.Font('04B_19.TTF',20)
bg_surface = pygame.image.load("assets/background-night.png").convert()
flap_sound = pygame.mixer.Sound('sound/sfx_wing.wav')
death_sound =pygame.mixer.Sound('sound/sfx_hit.wav')
score_sound = pygame.mixer.Sound('sound/sfx_point.wav')
floor_sound =pygame.mixer.Sound('sound/sfx_die.wav')
score_sound_countdown = 100
ground = pygame.image.load("assets/base.png").convert()
bird_upflap =pygame.image.load("assets/redbird-upflap.png").convert_alpha()
bird_midflap = pygame.image.load("assets/redbird-midflap.png").convert_alpha()
bird_downflap = pygame.image.load("assets/redbird-downflap.png").convert_alpha()
bird_frame = [bird_downflap,bird_midflap,bird_upflap]
bird_index = 0
bird = bird_frame[bird_index]
bird_rec = bird.get_rect(center = (50,256))
BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP,200)

pipes_surface = pygame.image.load("assets/pipe-red.png").convert()
pipelist = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE,1200)
pipe_heigt = [200,250,300,350,400]
ground_x_pos = 0
while True:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                movement = 0
                movement -= 6
                flap_sound.play()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active ==False:
                game_active = True
                pipelist.clear()
                bird_rec.center = (50,256)
                movement = 0
                score = 0
        if event.type == SPAWNPIPE:
            pipelist.extend(create_pipe())
        if event.type == BIRDFLAP:
            if bird_index < 2:
                bird_index += 1
            else :
                bird_index = 0
            bird,bird_rec = bird_animation()


    #Screen
    screen.blit(bg_surface,(0,0))

    if game_active:
        #Bird
        rotated_bird = rotate_bird(bird)
        screen.blit(rotated_bird,bird_rec)
        movement += gravity
        bird_rec.centery += movement



        #Pipes
        pipelist = move_pipe(pipelist)
        draw_pipes(pipelist)
        game_active = collison(pipelist)
        score += 0.05
        score_display('main_game')
        score_sound_countdown -= 1
        if score_sound_countdown <= 0:
            score_sound.play()
            score_sound_countdown = 100
    else:
        highscore = update_score(score,highscore)
        score_display('game_over')
        screen.blit(game_oversurface,game_oversurface_rect)

    #Ground
    ground_x_pos -= 1
    ground_movement()
    if ground_x_pos <= -288:
        ground_x_pos = 0

    pygame.display.update()
    clock.tick(60)