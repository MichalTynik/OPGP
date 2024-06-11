import random
import pygame
import os

pygame.font.init()
pygame.mixer.init()

col = 10  # 10 stĺpcov
row = 20  # 20 riadkov
s_width = 1400  # šírka okna
s_height = 750  # výška okna
play_width = 300  # šírka hracej plochy; 300/10 = 30 šírka jednej kocky
play_height = 600  # výška hracej plochy; 600/20 = 30 výška jednej kocky
block_size = 30  # veľkosť kocky
screen = pygame.display.set_mode((s_width, s_height))

top_left_x = (s_width - play_width) // 2
top_left_y = s_height - play_height - 50

# Determine the script directory
script_dir = os.path.dirname(os.path.abspath(__file__))

# Construct full paths to resources
filepath = os.path.join(script_dir, 'highscore.txt')
fontpath = os.path.join(script_dir, 'arcade.TTF')
background_path = os.path.join(script_dir, "background.png")
prehra_sound_path = os.path.join(script_dir, "umretie.mp3")
clear_sound_path = os.path.join(script_dir, "clear.mp3")
bg_music_path = os.path.join(script_dir, 'bg.mp3')

# Tvarové formáty
S = [['.....',
      '.....',
      '..00.',
      '.00..',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['.....',
      '..0..',
      '..0..',
      '..0..',
      '..0..'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

shapes = [S, Z, I, O, J, L, T]
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]


class Piece(object):
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]  # set color
        self.rotation = 0  # set rotation


def create_grid(locked_pos={}):
    grid = [[(0, 0, 0) for x in range(col)] for y in range(row)]

    for y in range(row):
        for x in range(col):
            if (x, y) in locked_pos:
                color = locked_pos[(x, y)]
                grid[y][x] = color

    return grid


def convert_shape_format(piece):
    positions = []
    shape_format = piece.shape[piece.rotation % len(piece.shape)]

    for i, line in enumerate(shape_format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                positions.append((piece.x + j, piece.y + i))

    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)

    return positions


# Zvuky
prehra_zvuk = pygame.mixer.Sound(prehra_sound_path)
clear_zvuk = pygame.mixer.Sound(clear_sound_path)

# Background pesnička
pygame.mixer.music.load(bg_music_path)
pygame.mixer.music.play(-1)

# Nacitanie pozadia
background = pygame.image.load(background_path).convert()

def valid_space(piece, grid):
    accepted_pos = [[(x, y) for x in range(col) if grid[y][x] == (0, 0, 0)] for y in range(row)]
    accepted_pos = [x for item in accepted_pos for x in item]

    formatted_shape = convert_shape_format(piece)

    for pos in formatted_shape:
        if pos not in accepted_pos:
            if pos[1] >= 0:
                return False
    return True


def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True
    return False


def get_shape():
    return Piece(5, 0, random.choice(shapes))


def draw_text_middle(text, size, color, surface):
    font = pygame.font.Font(fontpath, size)
    label = font.render(text, 1, color)

    surface.blit(label, (top_left_x + play_width / 2 - (label.get_width() / 2), top_left_y + play_height / 2 - (label.get_height() / 2)))


def draw_grid(surface):
    grid_color = (0, 0, 0)

    for i in range(row):
        pygame.draw.line(surface, grid_color, (top_left_x, top_left_y + i * block_size),
                         (top_left_x + play_width, top_left_y + i * block_size))
        for j in range(col):
            pygame.draw.line(surface, grid_color, (top_left_x + j * block_size, top_left_y),
                             (top_left_x + j * block_size, top_left_y + play_height))


def clear_rows(grid, locked):
    increment = 0
    for i in range(len(grid) - 1, -1, -1):
        grid_row = grid[i]
        if (0, 0, 0) not in grid_row:
            increment += 1
            index = i
            for j in range(len(grid_row)):
                try:
                    del locked[(j, i)]
                except:
                    continue

    if increment > 0:
        clear_zvuk.play()
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < index:
                newKey = (x, y + increment)
                locked[newKey] = locked.pop(key)

    return increment


def draw_next_shape(piece, surface):
    font = pygame.font.Font(fontpath, 30)
    label = font.render('Next shape', 1, (255, 255, 255))

    start_x = top_left_x + play_width + 50
    start_y = top_left_y + (play_height / 2 - 100)

    shape_format = piece.shape[piece.rotation % len(piece.shape)]

    for i, line in enumerate(shape_format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface, piece.color,
                                 (start_x + j * block_size, start_y + i * block_size, block_size, block_size), 0)

    surface.blit(label, (start_x + 10, start_y - 30))


def draw_window(surface, grid, score=0, high_score=0, player_name="", next_piece=None):
    surface.blit(background, (0, 0))  # Background obrazok
    font = pygame.font.Font(fontpath, 60)<<<<<<< main
    label = font.render('Tetris', 1, (255, 255, 255))

    surface.blit(label, (top_left_x + play_width / 2 - (label.get_width() / 2), 30))

    # Current score
    font = pygame.font.Font(fontpath, 30)
    label = font.render('Score ' + str(score), 1, (255, 255, 255))

    start_x = top_left_x + play_width + 50
    start_y = top_left_y + (play_height / 2 - 100)

    surface.blit(label, (start_x + 20, start_y + 160))

    label = font.render('High Score ' + highscore, 1, (255, 255, 255))

    start_y = top_left_y + 200

    surface.blit(label, (start_x + 20, start_y + 160))

    # Player name
    label = font.render('Player: ' + player_name, 1, (255, 255, 255))
    surface.blit(label, (start_x + 20, start_y + 200))

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j], (
                top_left_x + j * block_size, top_left_y + i * block_size, block_size, block_size), 0)

    draw_grid(surface)
    pygame.draw.rect(surface, (255, 0, 0), (top_left_x, top_left_y, play_width, play_height), 5)

    if next_piece:
        draw_next_shape(next_piece, surface)

    pygame.display.update()


def main(player_name):
    locked_positions = {}
    grid = create_grid(locked_positions)

    change_piece = False
    run = True
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    score = 0

    while run:
        grid = create_grid(locked_positions)
        fall_speed = 0.27

        fall_time += clock.get_rawtime()
        clock.tick()

        if fall_time / 1000 >= fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not (valid_space(current_piece, grid)) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not valid_space(current_piece, grid):
                        current_piece.x += 1
                if event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not valid_space(current_piece, grid):
                        current_piece.x -= 1
                if event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not valid_space(current_piece, grid):
                        current_piece.y -= 1
                if event.key == pygame.K_UP:
                    current_piece.rotation = current_piece.rotation + 1 % len(current_piece.shape)
                    if not valid_space(current_piece, grid):
                        current_piece.rotation = current_piece.rotation - 1 % len(current_piece.shape)

        shape_pos = convert_shape_format(current_piece)

        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                grid[y][x] = current_piece.color

        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False
            score += clear_rows(grid, locked_positions) * 10

        draw_window(screen, grid, score, high_score=read_high_score(), player_name=player_name, next_piece=next_piece)

        if check_lost(locked_positions):

            draw_text_middle("YOU LOST", 80, (255, 255, 255), screen)

            pygame.display.update()
            pygame.time.delay(1500)
            run = False
            update_score(score)

    pygame.display.quit()


def update_score(nscore):
    score = read_high_score()

    with open(filepath, 'w') as f:
        if int(score) > nscore:
            f.write(str(score))
        else:
            f.write(str(nscore))


def read_high_score():
    with open(filepath, 'r') as f:
        lines = f.readlines()
        high_score = lines[0].strip()
    return high_score


def name_input_screen():
    run = True
    player_name = ""
    font = pygame.font.Font(fontpath, 30)
    input_box = pygame.Rect(top_left_x, top_left_y + 200, 140, 32)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        run = False
                    elif event.key == pygame.K_BACKSPACE:
                        player_name = player_name[:-1]
                    else:
                        player_name += event.unicode

        screen.fill((0, 0, 0))
        draw_text_middle("Enter your name", 60, (255, 255, 255), screen)
        
        txt_surface = font.render(player_name, True, color)
        width = max(200, txt_surface.get_width() + 10)
        input_box.w = width
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        pygame.draw.rect(screen, color, input_box, 2)

        button_font = pygame.font.Font(fontpath, 30)
        ok_button = pygame.Rect(top_left_x, top_left_y + 300, 100, 50)
        pygame.draw.rect(screen, (0, 255, 0), ok_button)
        ok_label = button_font.render("OK", True, (0, 0, 0))
        screen.blit(ok_label, (ok_button.x + 25, ok_button.y + 10))

        pygame.display.flip()

        if pygame.mouse.get_pressed()[0] and ok_button.collidepoint(pygame.mouse.get_pos()):
            run = False

    return player_name


def main_menu():
    run = True
    while run:
        screen.fill((0, 0, 0))

        draw_text_middle('Press any key to begin', 60, (255, 255, 255), screen)

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                player_name = name_input_screen()
                main(player_name)
    pygame.display.quit()
    quit()


main_menu()
