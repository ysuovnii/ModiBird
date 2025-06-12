import pygame 
import random
pygame.init()
clock = pygame.time.Clock()

fps = 60 
screen_width = 260 
screen_height = 600 
start = 0
game_active = True

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Flappy Bird")

bg = pygame.image.load("Elements/background-day.png").convert_alpha()
base = pygame.image.load("Elements/base.png").convert_alpha()

font = pygame.font.Font("Pixeboy.ttf", 50)

base_rect = base.get_rect(bottomleft = (0, 600))

bird = []
for i in range(1, 4):
    frame = pygame.image.load(f'Elements/qyellowbird-{i}.png').convert_alpha()
    bird.append(frame)

bird_rect = bird[0].get_rect(center = (40, 250))

pipe = pygame.image.load("Elements/pipe.png").convert_alpha()
inverted_pipe = pygame.transform.flip(pipe, False, True)

button_rect = pygame.Rect(80, 250, 100, 100)

def start_menu():
    screen.fill((135, 206, 250))

    title = font.render("Flappy Bird", True, (255, 255, 255))
    screen.blit(title, title.get_rect(center=(130, 200)))

    pygame.draw.rect(screen, (0, 200, 0), button_rect, border_radius=15)
    text = font.render("Start", True, (255, 255, 255))
    screen.blit(text, text.get_rect(center=button_rect.center))

    pygame.display.update()

def wait_for_start():
    waiting = True
    while waiting:
        start_menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    waiting = False

        clock.tick(60)

def get_score():
    current_time = pygame.time.get_ticks() - start 
    score = font.render(f"{int(current_time/1000)}", False, "Black")
    score_rect = score.get_rect(topleft = (0, 0))
    screen.blit(score, score_rect)

def pipe_spawn(x_pos):
    gap_size = 150
    min_gap_y = 120  
    max_gap_y = screen_height - 120 - gap_size  

    gap_y = random.randint(min_gap_y, max_gap_y)

    top_pipe = inverted_pipe.get_rect(midbottom=(x_pos, gap_y))
    bottom_pipe = pipe.get_rect(midtop=(x_pos, gap_y + gap_size))

    return top_pipe, bottom_pipe

resume = pygame.image.load("Elements/Resume.png").convert_alpha()
resume_rect = resume.get_rect(center = (screen_width // 2, 300))

def game_over():
    screen.fill((160, 255, 248))  
    
    title = font.render("GAME OVER", True, "Red")
    title_rect = title.get_rect(center=(screen_width // 2, 150))
    screen.blit(title, title_rect)

    screen.blit(resume, resume_rect)
    
pipe_list = []
spawn = pygame.USEREVENT
pygame.time.set_timer(spawn, 1500)  

frame_index = 0
animation_speed = 0.2
bird_gravity = 0

wait_for_start()

run = True 
while run: 
    mouse = pygame.mouse.get_pressed()

    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            run = False

        if event.type == spawn:
            pipe_list.extend(pipe_spawn(screen_width+50))

    if mouse[0]:  
        bird_rect.y += 10 
    if mouse[2]:  
        bird_rect.y -= 10 

    screen.blit(bg, (0, 0))

    if game_active: 
        frame_index += animation_speed
        if frame_index >= len(bird):
            frame_index = 0

        for pipe_rect in pipe_list:
            pipe_rect.centerx -= 3
            if pipe_rect.bottom >= screen_height:
                screen.blit(pipe, pipe_rect)  
            else:
                screen.blit(inverted_pipe, pipe_rect)  

            if bird_rect.colliderect(pipe_rect):
                game_active = False

        get_score()

        screen.blit(base, base_rect)
        screen.blit(bird[int(frame_index)], bird_rect)

    else: 
        game_over()
        if event.type == pygame.MOUSEBUTTONDOWN: 
            if resume_rect.collidepoint(mouse_pos):
                bird_rect.center = (40, 250)
                pipe_list.clear()
                start = pygame.time.get_ticks()
                game_active = True

    pygame.display.flip()
    clock.tick(fps)
