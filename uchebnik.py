import pygame
import sys
import os




def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey)
        image = image.convert_alpha()
        return image
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)


class Puly(pygame.sprite.Sprite):
    def __init__(self,px, py, mx, my, pg, pv):
        super().__init__(puly_group, all_sprites)
        if mx != 0:
            k = my / mx
            self.vx = int(((300 ** 2) / (k ** 2 + 1)) ** 0.5)
            self.vy = int((300 ** 2 - self.vx ** 2) ** 0.5)
        else:
            self.vy = 300
            self.vx = 0
        self.pg = pg
        self.pv = pv
        self.image = puly
        self.rect = self.image.get_rect().move(
            px, py)
        
    def update(self):
        self.rect.x += (self.pg * self.vx) /fps
        self.rect.y += (self.pv * self.vy) / fps
        test = pygame.sprite.spritecollide(self, tiles_group, False)
        for i in test:
            if i.type == 'wall':
                puly_group.remove(self)
            
            


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.type = tile_type
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        self.nap = "l"
        super().__init__(player_group, all_sprites)
        self.stoy = {"l": player_imagesl, "r": player_imagesr}
        self.image = self.stoy[self.nap]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)
        self.beg = {"l": player_imagebl, "r": player_imagebr}
        self.n = 0
        self.potron = 20
        
    def update(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy
        self.image = self.beg[self.nap][int(self.n)]
        self.n = (self.n + 0.2) % 6
        test = pygame.sprite.spritecollide(self, tiles_group, False)
        for i in test:
            if i.type == 'wall':
                flag = False
                self.rect.x -= dx
                self.rect.y -= dy
                break


def terminate():
    pygame.quit()
    sys.exit()


def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    max_width = max(map(len, level_map))

    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
    return new_player, x, y


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - WIDTH // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - HEIGHT // 2)


def start_screen():
    intro_text = ["ЗАСТАВКА", "",
                  "Правила игры",
                  "Если в правилах несколько строк,",
                  "приходится выводить их построчно"]

    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == \
                    pygame.KEYDOWN or event.type == \
                    pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(fps)


pygame.init()
v = 100
player = None
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
puly_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
size = 1000, 1000
HEIGHT = 1000
WIDTH = 1000
fps = 25
screen = pygame.display.set_mode(size)
puly = load_image("puly.png")
tile_images = {
    "empty": load_image("grass.png"),
    "wall": load_image("box.png")
}
player_imagebl = [load_image("begl1.png"),
                  load_image("begl2.png"),
                  load_image("begl3.png"),
                  load_image("begl4.png"),
                  load_image("begl3.png"),
                  load_image("begl2.png")]
player_imagebr = [load_image("begr1.png"),
                  load_image("begr2.png"),
                  load_image("begr3.png"),
                  load_image("begr4.png"),
                  load_image("begr3.png"),
                  load_image("begr2.png")]
player_imagesl = load_image("stoyl.png")
player_imagesr = load_image("stoyr.png")
tile_width = tile_height = 50
player, player_x, player_y = generate_level(load_level('levelex.txt'))
start_screen()
running = True
moveg = 0
movev = 0
while running:
    for event in pygame.event.get():
        keystate = pygame.key.get_pressed()
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.K_UP:
            player.image = player.stoy[player.nap]
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                moveg -= 1
                player.nap = "l"
            if event.key == pygame.K_a:
                moveg -= 1
                player.nap = "l"
            if event.key == pygame.K_RIGHT:
                moveg += 1
                player.nap = "r"
            if event.key == pygame.K_d:
                moveg += 1
                player.nap = "r"
            if event.key == pygame.K_UP:
                movev -= 1
            if event.key == pygame.K_w:
                movev -= 1
            if event.key == pygame.K_DOWN:
                movev += 1
            if event.key == pygame.K_s:
                movev += 1
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                moveg += 1
                player.nap = "l"
            if event.key == pygame.K_a:
                moveg += 1
                player.nap = "l"
            if event.key == pygame.K_RIGHT:
                moveg -= 1
                player.nap = "r"
            if event.key == pygame.K_d:
                moveg -= 1
                player.nap = "r"
            if event.key == pygame.K_UP:
                movev += 1
            if event.key == pygame.K_w:
                movev += 1
            if event.key == pygame.K_DOWN:
                movev -= 1
            if event.key == pygame.K_s:
                movev -= 1
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if player.rect.x + 32 > event.pos[0]:
                pg = -1
            else:
                pg = 1
            if player.rect.y + 32 > event.pos[1]:
                pv = -1
            else:
                pv = 1

            Puly(player.rect.x + 32, player.rect.y + 32,
                 event.pos[0] - player.rect.x - 32,  event.pos[1] - player.rect.y - 32, pg, pv)
    if movev != 0 or moveg != 0:
        player.update(moveg * v / fps, movev * v / fps)
    else:
        player.image = player.stoy[player.nap]
        player.n = 0
    for i in puly_group:
        i.update()
    screen.fill((0, 0, 0))
    tiles_group.draw(screen)
    player_group.draw(screen)
    puly_group.draw(screen)
    pygame.display.flip()
    clock.tick(fps)
