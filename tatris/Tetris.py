import random
import pygame

"""
    0 - S - zelena
    1 - Z - cervena
    2 - I - tyrkysova
    3 - O - zlta
    4 - J - modra
    5 - L - oranzova
    6 - T - fialova
"""

pygame.font.init()
pygame.mixer.init()

col = 10  # 10 stlpec
row = 20  # 20 riadkov
s_width = 1400  # sirka okna
s_height = 750  # vyska okna
play_width = 300  #  sirka okna; 300/10 = 30 sirka jednej kocky/ hracia plocha
play_height = 600  #  vyska okna; 600/20 = 20 vyska jednej kocky/ hracia plocha
block_size = 30  # velkost kocky
screen = pygame.display.set_mode((s_width, s_height))

top_left_x = (s_width - play_width) // 2
top_left_y = s_height - play_height - 50

filepath = './highscore.txt'
fontpath = './arcade.ttf'

# tvary formats

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

tvary = [S, Z, I, O, J, L, T]
farba_tvarov = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]


class Piece(object):
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = farba_tvarov[tvary.index(shape)]  # nastavenie farby
        self.rotation = 0  # aka je rotacia tvaru


# mriezkovanie / rozdelenie plochy na kocky
def create_grid(locked_pos={}):
    grid = [[(0, 0, 0) for x in range(col)] for y in range(row)]

    # (x,y):(r,g,b)
    for y in range(row):
        for x in range(col):
            if (x, y) in locked_pos:
                color = locked_pos[(x, y)]  
                grid[y][x] = color  # nastavenie farby kocke

    return grid


#vytvaranie tvarov
def convert_shape_format(piece):
    positions = []
    shape_format = piece.shape[piece.rotation % len(piece.shape)]  

    for i, line in enumerate(shape_format):
        row = list(line)  
        for j, stlpec in enumerate(row):  
            if stlpec == '0':
                positions.append((piece.x + j, piece.y + i))

    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)

    return positions


#zvuky
prehra_zvuk = pygame.mixer.Sound("umretie.mp3")
clear_zvuk = pygame.mixer.Sound("clear.mp3")

# background pesnicka
pygame.mixer.music.load('bg.mp3')
pygame.mixer.music.play(-1)


# kontrola tvaru
def valid_space(piece, grid):
    accepted_pos = [[(x, y) for x in range(col) if grid[y][x] == (0, 0, 0)] for y in range(row)]
    accepted_pos = [x for item in accepted_pos for x in item]

    formatted_shape = convert_shape_format(piece)

    for pos in formatted_shape:
        if pos not in accepted_pos:
            if pos[1] >= 0:
                return False
    return True


# kontroluje ci hrac prehral
def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True
    return False


# vyberie tvar
def get_shape():
    return Piece(5, 0, random.choice(tvary))


# napis text
def draw_text_middle(text, size, color, surface):
    font = pygame.font.Font(fontpath, size)
    label = font.render(text, 1, color)

    surface.blit(label, (top_left_x + play_width/2 - (label.get_width()/2), top_left_y + play_height/2 - (label.get_height()/2)))


# nakresli hraciu plochu
def draw_grid(surface):
    r = g = b = 0
    grid_color = (r, g, b)

    for i in range(row):
        #horizontalne
        pygame.draw.line(surface, grid_color, (top_left_x, top_left_y + i * block_size),
                         (top_left_x + play_width, top_left_y + i * block_size))
        for j in range(col):
            #vertikalne
            pygame.draw.line(surface, grid_color, (top_left_x + j * block_size, top_left_y),
                             (top_left_x + j * block_size, top_left_y + play_height))


# vycisti riadok ak je zaplneny
def clear_riadkov(grid, locked):
    increment = 0
    for i in range(len(grid) - 1, -1, -1):      
        grid_row = grid[i]                      
        if (0, 0, 0) not in grid_row:           
            increment += 1
            #vycistenie 
            index = i                           
            for j in range(len(grid_row)):
                try:
                    del locked[(j, i)] 
                    pygame.mixer.Sound.play(clear_zvuk)    
                except ValueError:
                    continue

    #opravenie hracej plochy / ked sa jeden riadok vymaze tak sa hore vytvori novy
    if increment > 0:
        for key in sorted(list(locked), key=lambda a: a[1])[::-1]:
            x, y = key
            if y < index:                       
                new_key = (x, y + increment)    
                locked[new_key] = locked.pop(key)

    return increment


# nakresli dalsi tvar
def draw_next_shape(piece, surface):
    font = pygame.font.Font(fontpath, 30)
    label = font.render('DALSI     TVAR', 1, (255, 255, 0))

    start_x = top_left_x + play_width + 50
    start_y = top_left_y + (play_height / 2 - 100)

    shape_format = piece.shape[piece.rotation % len(piece.shape)]

    for i, line in enumerate(shape_format):
        row = list(line)
        for j, stlpec in enumerate(row):
            if stlpec == '0':
                pygame.draw.rect(surface, piece.color, (start_x + j*block_size, start_y + i*block_size, block_size, block_size), 0)

    surface.blit(label, (start_x, start_y - 30))


# pozadie
def draw_window(surface, grid, score=0, max_score=0):
    # pozadie
    background_image = pygame.image.load("background.png")

    # vsadenie pozadia sirke obrazu
    background_image = pygame.transform.scale(background_image, (s_width, s_height))
    # vycisti obrazovku
    screen.fill((0, 0, 0))

    # prekresli pozadie
    screen.blit(background_image, (0, 0))


    pygame.font.init()  # typ pisma
    font = pygame.font.Font(fontpath, 65)
    label = font.render('TATRIS', 1, (0, 0, 0))  

    surface.blit(label, ((top_left_x + play_width / 2) - (label.get_width() / 2), 30))  # vycentrovanie nazvu

    # skore
    font = pygame.font.Font(fontpath, 30)
    label = font.render('SKORE   ' + str(score), 1, (255,255,0))

    start_x = top_left_x + play_width + 50
    start_y = top_left_y + (play_height / 2 - 100)

    surface.blit(label, (start_x, start_y + 200))

    # najvacsie skore
    label_hi1 = font.render('NAJVACSIE  ', 1, (255, 255, 0))
    label_hi2 = font.render('SKORE   ', 1, (255, 255, 0))
    label_hi3 = font.render(str(max_score), 1, (255, 255, 0))

    start_x_hi = top_left_x - 240
    start_y_hi = top_left_y + 200

    surface.blit(label_hi1, (start_x_hi + 20, start_y_hi))
    surface.blit(label_hi2, (start_x_hi + 20, start_y_hi + 50))
    surface.blit(label_hi3, (start_x_hi + 20, start_y_hi + 100))
    # kresli grid
    for i in range(row):
        for j in range(col):
            pygame.draw.rect(surface, grid[i][j],
                             (top_left_x + j * block_size, top_left_y + i * block_size, block_size, block_size), 0)

    # kresli lajny gridu
    draw_grid(surface)

    # kresli hraciu plochu
    border_color = (255, 255, 255)
    pygame.draw.rect(surface, border_color, (top_left_x, top_left_y, play_width, play_height), 4)


# aktualizuj max skore
def update_score(new_score):
    score = get_max_score()

    with open(filepath, 'w') as file:
        if new_score > score:
            file.write(str(new_score))
        else:
            file.write(str(score))


# vyber max skore
def get_max_score():
    with open(filepath, 'r') as file:
        lines = file.readlines()        # precita skore zo suboru
        score = int(lines[0].strip())   # remove \n

    return score

# hlavny program
def main(window):
    locked_positions = {}
    create_grid(locked_positions)

    change_piece = False
    run = True
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.35
    level_time = 0
    score = 0
    max_score = get_max_score()

    while run:
        # kresli grid
        grid = create_grid(locked_positions)

        #ziskavanie casu
        fall_time += clock.get_rawtime()
        level_time += clock.get_rawtime()

        clock.tick()  # aktualizuj cas

        if level_time/1000 > 5:    # kazdych 10 sek. zrychli az po rychlost 0.15
            level_time = 0
            if fall_speed > 0.15:   
                fall_speed -= 0.005

        if fall_time / 1000 > fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not valid_space(current_piece, grid) and current_piece.y > 0:
                current_piece.y -= 1
                # vytvaranie tvaru v spravny cas
                change_piece = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                quit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1  # posuvanie dolava
                    if not valid_space(current_piece, grid):
                        current_piece.x += 1

                elif event.key == pygame.K_RIGHT:
                    current_piece.x += 1  # posuvanie doprava
                    if not valid_space(current_piece, grid):
                        current_piece.x -= 1

                elif event.key == pygame.K_DOWN:
                    # posunutie nizsie / zrychlenie
                    current_piece.y += 1
                    if not valid_space(current_piece, grid):
                        current_piece.y -= 1

                elif event.key == pygame.K_UP:
                    # otoc tvar
                    current_piece.rotation = current_piece.rotation + 1 % len(current_piece.shape)
                    if not valid_space(current_piece, grid):
                        current_piece.rotation = current_piece.rotation - 1 % len(current_piece.shape)

        piece_pos = convert_shape_format(current_piece)

        # pridavanie farby kocke / jednej casti gridu
        for i in range(len(piece_pos)):
            x, y = piece_pos[i]
            if y >= 0:
                grid[y][x] = current_piece.color

        if change_piece:  # ak naplnime riadok
            for pos in piece_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color       
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False
            score += clear_riadkov(grid, locked_positions) * 10    # pridaj 10 bodov
            update_score(score)

            if max_score < score:
                max_score = score
        # nakresli okno a tvar
        draw_window(window, grid, score, max_score)
        draw_next_shape(next_piece, window)
        pygame.display.update()

        if check_lost(locked_positions):
            run = False

    # Prehral si!
    draw_text_middle('Prehral   si', 40, (255, 255, 255), window)
    pygame.mixer.Sound.play(prehra_zvuk)
    pygame.mixer.music.stop()
    pygame.display.update()
    pygame.time.delay(2000)
    pygame.quit()
# prve menu
def main_menu(window):
    run = True
    while run:
        draw_text_middle('Stlac   tlacidlo   aby   si   zacal', 50, (255, 255, 255), window)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                main(window)

    pygame.quit()

#spustenie hry
if __name__ == '__main__':
    win = pygame.display.set_mode((s_width, s_height))
    pygame.display.set_caption('Tatris')

    main_menu(win)
