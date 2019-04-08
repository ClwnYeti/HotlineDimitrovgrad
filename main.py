import pygame
import sys
import os
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QInputDialog
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt
from random import randint
plstart = []


class Menu(QWidget):
    def __init__(self):
        global plstart
        super().__init__()
        uic.loadUi('menu.ui', self)
        self.initUI()
    
    def initUI(self):
        self.b1.clicked.connect(self.start)
        self.b2.clicked.connect(self.vibor)
        self.b3.clicked.connect(self.exite)
    
    def vibor(self):
        with open('data/levels.txt', 'r', encoding='utf-8') as f:
            f = list(f.read())
        i, okBtnPressed = QInputDialog.getText(
            self, 'Уровень',
            "Введите номер уровня"
        )
        if okBtnPressed:
            if 0 > int(i) or int(i) > 2:
                print('Нет такого уровня')
                return
            elif f[int(i) - 1] != 'p':
                print('Пройдите предыдущие уровни')
                return
            player, player_x, player_y = generate_level(load_level(f'levelex{int(i)}.txt'))
            plstart.append(player)
            plstart.append(player_x)
            plstart.append(player_y)
            global flag
            flag = True
            self.close()
    
    def exite(self):
        sys.exit(self.exec())
    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            global flag
            flag = True
            self.close()
            
    def start(self):
        global flag
        flag = True
        with open('data/levels.txt', 'w', encoding='utf-8') as f:
            f.write('pc')
        player, player_x, player_y = generate_level(load_level(f'levelex1.txt'))
        plstart.append(player)
        plstart.append(player_x)
        plstart.append(player_y)
        self.close()


class Pause(QWidget):
    def __init__(self):
        global plstart
        super().__init__()
        uic.loadUi('pause.ui', self)
        self.initUI()
    
    def initUI(self):
        self.bt.clicked.connect(self.exite)
    
    def exite(self):
        sys.exit(self.exec())
    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            global flag
            flag = True
            self.close()
    

def win():
    with open('data/levels.txt', 'r', encoding='utf-8') as f:
        a = list(f.read())
        a[1] = 'p'
    with open('data/levels.txt', 'w', encoding='utf-8') as f:
        f.write(''.join(a))
    fon = pygame.transform.scale(load_image('win.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    flag = False
    player_group.empty()
    tiles_group.empty()
    puly_group.empty()
    zombi_group.empty()
    ex = Menu()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == \
                    pygame.KEYDOWN or event.type == \
                    pygame.MOUSEBUTTONDOWN:
                flag = False
                exit()
        pygame.display.flip()
        clock.tick(fps)


def death():
    fon = pygame.transform.scale(load_image('death.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    flag = False
    player_group.empty()
    tiles_group.empty()
    puly_group.empty()
    zombi_group.empty()
    ex = Menu()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == \
                    pygame.KEYDOWN or event.type == \
                    pygame.MOUSEBUTTONDOWN:
                flag = False
                exit()
        pygame.display.flip()
        clock.tick(fps)


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
    def __init__(self, px, py, mx, my, pg, pv):
        super().__init__(puly_group, all_sprites)
        self.type = 'puly'
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
        self.rect.x += (self.pg * self.vx) / fps
        self.rect.y += (self.pv * self.vy) / fps
        test = pygame.sprite.spritecollide(self, tiles_group, False)
        test2 = pygame.sprite.spritecollide(self, zombi_group, False)
        for i in test:
            if i.type == 'wall':
                puly_group.remove(self)
        for i in test2:
            a = randint(0, 5)
            if a == 0:
                Potron(self.rect.x, self.rect.y)
            zd.stop()
            zd.play()
            zombi_group.remove(i)
            puly_group.remove(self)


class Potron(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(potron_group, all_sprites)
        self.image = potron
        self.rect = self.image.get_rect().move(
            x, y)
    
    def update(self):
        if pygame.sprite.spritecollideany(self, player_group, False):
            potron_group.remove(self)
            player.potron += 2


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
        self.type = 'pl'
        super().__init__(player_group, all_sprites)
        self.stoy = {"l": player_imagesl, "r": player_imagesr}
        self.image = self.stoy[self.nap]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)
        self.beg = {"l": player_imagebl, "r": player_imagebr}
        self.n = 2
        self.potron = 10
        
    def update(self, dx, dy):
        self.rect.x += dx
        test = pygame.sprite.spritecollide(self, tiles_group, False)
        for i in test:
            if i.type == 'wall':
                self.rect.x -= dx
                break
        self.rect.y += dy
        test = pygame.sprite.spritecollide(self, tiles_group, False)
        test2 = pygame.sprite.spritecollide(self, zombi_group, False)
        for i in test:
            if i.type == 'wall':
                self.rect.y -= dy
                break
            if i.type == 'exit':
                win()
        for i in test2:
            death()
        self.image = self.beg[self.nap][int(self.n)]
        self.n = (self.n + 0.2) % 6


class Zombie(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, pospx):
        self.type = 'z'
        if pos_x > pospx:
            self.nap = "l"
        else:
            self.nap = "r"
        self.n = 2
        super().__init__(zombi_group, all_sprites)
        self.beg = {"l": zombl, "r": zombr}
        self.image = self.beg[self.nap][self.n]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)
    
    def update(self, plx, ply):
        if self.rect.x > plx:
            self.nap = "l"
        else:
            self.nap = "r"
        if plx - self.rect.x != 0:
            k = (ply - self.rect.y) / (plx - self.rect.x)
            self.vx = int(((100 ** 2) / (k ** 2 + 1)) ** 0.5)
            self.vy = int((100 ** 2 - self.vx ** 2) ** 0.5)
        else:
            self.vy = 100
            self.vx = 0
        if plx + 32 > self.rect.x:
            pg = 1
        else:
            pg = -1
        if ply + 32 > self.rect.y:
            pv = 1
        else:
            pv = -1
        self.pg = pg
        self.pv = pv
        self.rect.x += int(self.vx * self.pg / fps)
        test = pygame.sprite.spritecollide(self, tiles_group, False)
        test2 = pygame.sprite.spritecollide(self, zombi_group, False)
        for i in test:
            if i.type == 'wall':
                self.rect.x -= int(self.vx * self.pg / fps)
                break
        for i in test2:
            if i != self:
                self.rect.x -= int(self.vx * self.pg / fps)
                break
        self.rect.y += int(self.vy * self.pv / fps)
        test = pygame.sprite.spritecollide(self, tiles_group, False)
        test2 = pygame.sprite.spritecollide(self, zombi_group, False)
        for i in test:
            if i.type == 'wall':
                self.rect.y -= int(self.vy * self.pv / fps)
                break
        for i in test2:
            if i != self:
                self.rect.y -= int(self.vy * self.pv / fps)
                break
        self.image = self.beg[self.nap][int(self.n)]
        self.n = (self.n + 0.2) % 6


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
                px = x
            elif level[y][x] == 'e':
                Tile('exit', x, y)
    
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == 'x':
                Tile('empty', x, y)
                Zombie(x, y, px)
    return new_player, x, y


def start_screen():
    global flag
    intro_text = ["Здравствуйте", "",
                  "Привила игры",
                  "Передвижение: WASD или стрелочки",
                  "Задача: Выбраться наружу"
                  "Нажмите любую клавишу,"
                  "чтобы зайти в меню"]

    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    flag = False
    ex = Menu()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == \
                    pygame.KEYDOWN or event.type == \
                    pygame.MOUSEBUTTONDOWN:
                flag = False
                ex.show()
            if flag:
                return
        pygame.display.flip()
        clock.tick(fps)


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


pygame.init()
v = 100
player = None
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
puly_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
zombi_group = pygame.sprite.Group()
potron_group = pygame.sprite.Group()
size = 1000, 1000
HEIGHT = 1000
WIDTH = 1000
fps = 25
screen = pygame.display.set_mode(size)
puly = load_image("puly.png")
potron = load_image('potron.png')
tile_images = {
    "empty": load_image("wall.png"),
    "wall": load_image("floor.png"),
    "exit": load_image("exit.png")
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
zombl = [load_image("zl1.png"),
         load_image("zl2.png"),
         load_image("zl3.png"),
         load_image("zl4.png"),
         load_image("zl3.png"),
         load_image("zl2.png")]
zombr = [load_image("zr1.png"),
         load_image("zr2.png"),
         load_image("zr3.png"),
         load_image("zr4.png"),
         load_image("zr3.png"),
         load_image("zr2.png")]
player_imagesl = load_image("stoyl.png")
player_imagesr = load_image("stoyr.png")
tile_width = tile_height = 65
app = QApplication(sys.argv)
start_screen()
player, player_x, player_y = plstart
running = True
moveg = 0
movev = 0
camera = Camera()
gun = pygame.mixer.Sound('data/shoot.wav')
gun.set_volume(0.2 * gun.get_volume())
xod = pygame.mixer.Sound('data/007.wav')
xod.set_volume(0.5 * xod.get_volume())
zd = pygame.mixer.Sound('data/zombiedeath.wav')
zd.set_volume(0.5 * zd.get_volume())
while running:
    for event in pygame.event.get():
        keystate = pygame.key.get_pressed()
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                ex = Pause()
                flag = False
                ex.show()
            elif flag:
                player.image = player.stoy[player.nap]
                player.n = 2
        if event.type == pygame.KEYDOWN and flag:
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
        if event.type == pygame.KEYUP and flag:
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
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and flag:
            if player.rect.x + 32 > event.pos[0]:
                pg = -1
            else:
                pg = 1
            if player.rect.y + 32 > event.pos[1]:
                pv = -1
            else:
                pv = 1
            if player.potron != 0:
                gun.stop()
                gun.play()
                Puly(player.rect.x + 32, player.rect.y + 32, event.pos[0] - player.rect.x - 32,
                     event.pos[1] - player.rect.y - 32, pg, pv)
                player.potron -= 1
                
    if movev != 0 or moveg != 0 and flag:
        xod.stop()
        xod.play()
        player.update(moveg * v / fps, movev * v / fps)
    elif flag:
        player.image = player.stoy[player.nap]
        player.n = 2
    if flag:
        for i in puly_group:
            i.update()
        for i in zombi_group:
            i.update(player.rect.x, player.rect.y)
        screen.fill((0, 0, 0))
        camera.update(player)
        for sprite in all_sprites:
            camera.apply(sprite)
        potron_group.update()
        tiles_group.draw(screen)
        puly_group.draw(screen)
        potron_group.draw(screen)
        player_group.draw(screen)
        zombi_group.draw(screen)
        font = pygame.font.Font(None, 50)
        text = font.render(str(player.potron), 1, (100, 255, 100))
        text_x = 0
        text_y = 0
        text_w = text.get_width()
        text_h = text.get_height()
        screen.blit(text, (text_x, text_y))
        pygame.display.flip()
        clock.tick(fps)
