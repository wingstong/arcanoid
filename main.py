import pygame
pygame.init()

clock = pygame.time.Clock()
screen_width = 800
screen_height = 600
player_speed = 6
flag_win = False
flag_lose = False
running = True

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Arcanoid")

background_img = pygame.transform.scale(pygame.image.load('bg.png'), (screen_width, screen_height))
player_img = pygame.transform.scale(pygame.image.load('platform.png'), (120, 40))
ball_img = pygame.transform.scale(pygame.image.load('ball.png'), (30, 30))
enemy_img = pygame.transform.scale(pygame.image.load('enemy.png'),(50, 50))

def show_text(text, x, y):
    font = pygame.font.SysFont('Century Gothic', 30)
    text = font.render(text, True, (253, 255, 237))
    screen.blit(text, (x, y))

def show_menu():
    menu_running = True
    while menu_running:
        screen.blit(background_img, (0, 0))
        show_text("Arcanoid!", 350, 250)
        show_text("Нажмите 'S' чтобы начать игру", 200, 300)
        show_text("Нажмите 'Q' чтобы выйти", 200, 350)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    menu_running = False
                if event.key == pygame.K_q:
                    exit()

def restart_game():
    global flag_win, flag_lose
    flag_win = False
    flag_lose = False
    ball_rect.x = screen_width // 2
    ball_rect.y = screen_height - 100
    enemy_rect.clear()
    enemy_x = 50
    enemy_y = 50
    player_rect.x = screen_width - 450
    player_rect.y = screen_height - 65
    for i in range(3):
        for j in range(14):
            l_rect = enemy_img.get_rect()
            l_rect.x = enemy_x
            l_rect.y = enemy_y
            enemy_rect.append(l_rect)
            enemy_x += 50
        enemy_x = 50
        enemy_y += 50
    show_menu()

# Массив врагов
enemy_rect = []
enemy_x = 50
enemy_y = 50
for i in range(3):
    for j in range(14):
        l_rect = enemy_img.get_rect()
        l_rect.x = enemy_x
        l_rect.y = enemy_y
        enemy_rect.append(l_rect)
        enemy_x += 50
    enemy_x = 50
    enemy_y += 50

# Начальные координаты игрока и мяча
player_rect = player_img.get_rect()
player_rect.x = screen_width - 450
player_rect.y = screen_height - 65

ball_rect = ball_img.get_rect()
ball_rect.x = screen_width // 2
ball_rect.y = screen_height - 100
ball_speed_x = 4
ball_speed_y = -4


show_menu()
while running:
    screen.blit(background_img, (0, 0))
    screen.blit(player_img, player_rect)
    screen.blit(ball_img, ball_rect)

    if flag_win:
        show_text("Вы выиграли!", 300, 300)
    if flag_lose:
        show_text("Вы проиграли!", 300, 300)
        show_text("Нажмите 'R' чтобы начать сначала", 200, 350)

    for i in enemy_rect:
        screen.blit(enemy_img, i)

    ball_rect.x += ball_speed_x
    ball_rect.y += ball_speed_y

    keys = pygame.key.get_pressed()
    if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and player_rect.x > 0:
        player_rect.x -= player_speed
    if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and player_rect.x < screen_width-120:
        player_rect.x += player_speed

    # Отскок мяча от стенок
    if ball_rect.right >= screen_width or ball_rect.x <= 0:
        ball_speed_x *= -1
    if ball_rect.top <= 0:
        ball_speed_y *= -1

    # Отскок мяча от игрока
    if player_rect.colliderect(ball_rect):
        if ball_rect.bottom >= player_rect.y + ball_speed_y:
            if player_rect.center[0] > ball_rect.x:
                ball_rect.x -= abs(ball_speed_x) * 2
            else:
                ball_rect.x += abs(ball_speed_x) * 2
            ball_speed_x *= -1
        ball_speed_y *= -1

    if ball_rect.y >= screen_height:
        flag_lose = True

    # Удаление врагов при столкновении с мячом
    for i in enemy_rect:
        if ball_rect.colliderect(i):
            ball_speed_y *= -1
            enemy_rect.remove(i)
    if len(enemy_rect) == 0:
        flag_win = True

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                restart_game()
            if event.key == pygame.K_q:
                exit()

    pygame.display.flip()
    clock.tick(60)