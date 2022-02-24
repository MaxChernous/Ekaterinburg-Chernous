import os
import sys

import pygame


def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print("Error: No file named ", name)
        raise SystemExit(message)
    image = image.convert_alpha()
    if color_key:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    return image


pygame.init()
size = width, height = 700, 700
screen = pygame.display.set_mode(size)
sprite_group = pygame.sprite.Group()
hero_group = pygame.sprite.Group()

tile_image = {'wall': load_image('box.png'),
              'empty': load_image('grass.png')}
player_image = load_image('mar.png')

tile_width = tile_height = 50


class ScreenFrame(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.rect = (0, 0, 500, 500)


class SpriteGroup(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

    def get_event(self, event):
        for sp in self:
            sp.get_event(event)


class Sprite(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.rect = None

    def get_event(self, event):
        pass


class Tile(Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(sprite_group)
        self.image = tile_image[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class Player(Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(hero_group)
        self.image = player_image
        self.rect = self.image.get_rect().move(tile_width * pos_x + 15, tile_height * pos_y + 5)
        self.pos = (pos_x, pos_y)

    def move(self, x, y):
        self.pos = (x, y)
        self.rect = self.image.get_rect().move(tile_width * self.pos[0] + 15,
                                               tile_height * self.pos[1] + 5)


def start_screen():
    fon = pygame.transform.scale(load_image('fon.jpg'), size)
    screen.blit(fon, (0, 0))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()


def load_level(filename):
    filename = 'data/' + filename
    with open(filename, 'r') as mapFile:
        labyrinth = [line.strip() for line in mapFile]
    max_width = max(map(len, labyrinth))
    return list(map(lambda x: list(x.ljust(max_width, '.')), labyrinth))


def generate_level(level):
    new_player = None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
                level[y][x] = '.'
    if level and new_player:
        return new_player, x, y


if __name__ == '__main__':
    pygame.display.set_caption('Mario')
    player = None
    running = True
    start_screen()
    labyrinth = load_level("map.txt")
    hero, max_x, max_y = generate_level(labyrinth)
    size = width, height = 500, 500
    screen = pygame.display.set_mode(size)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                x, y = hero.pos
                dx, dy = 0, 0
                if event.key == pygame.K_w:
                    if y > 0 and labyrinth[y - 1][x] == '.':
                        hero.move(x, y - 1)
                if event.key == pygame.K_s:
                    if y < max_y - 1 and labyrinth[y + 1][x] == '.':
                        hero.move(x, y + 1)
                if event.key == pygame.K_a:
                    if x > 0 and labyrinth[y][x - 1] == '.':
                        hero.move(x - 1, y)
                if event.key == pygame.K_d:
                    if x < max_x - 1 and labyrinth[y][x + 1] == '.':
                        hero.move(x + 1, y)

        screen.fill(pygame.Color('black'))
        sprite_group.draw(screen)
        hero_group.draw(screen)
        pygame.display.flip()
    pygame.quit()
