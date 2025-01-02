import pygame
from pygame import sprite, Rect, Surface, Color, QUIT, KEYDOWN, KEYUP, K_a, K_d, K_w

# Константы для окна
WIN_WIDTH = 800
WIN_HEIGHT = 640
BACKGROUND_COLOR = "#004400"

# Константы для платформ
PLATFORM_WIDTH = 32
PLATFORM_HEIGHT = 32

# Уровни с различными спавнами
levels = [
    {
        "layout": [
            "-------------------------",
            "-00000000000000000000000-",
            "-00000000000000000000000-",
            "-000000000000++000000000-",
            "-00000000000000000000000-",
            "-+0000000000000000000000-",
            "-00000000000000000000000-",
            "-00000000000000000000+++-",
            "-00000000000000000000000-",
            "-00000000000000000000000-",
            "-000000+++00000000000000-",
            "-000000000000=0000000000-",
            "-000++++++++++++0000000 -",
            "-00000000000000000000000-",
            "-0000000000000000+000000-",
            "-0000000000000000000++00-",
            "-00000000000000000000000-",
            "-00000000000000000000000-",
            "-------------------------"
        ],
        "spawn": (55, 55)
    },
    {
        "layout": [
            "-------------------------",
            "-00000000000000000000000-",
            "-00000000000000000000000-",
            "-0000000000000=000000000-",
            "-000000000000++000000000-",
            "-00000000000000000000000-",
            "-+0000000000000000000000-",
            "-00000000000000000000000-",
            "-00000000000000000000+++-",
            "-00000000000000000000000-",
            "-00000000000000000000000-",
            "-000000+++00000000000000-",
            "-00000000000000000000000-",
            "-000++++++++++++0000000 -",
            "-00000000000000000000000-",
            "-0000000000000000+000000-",
            "-0000000000000000000++00-",
            "-00000000000000000000000-",
            "-00000000000000000000000-",
            "-------------------------"
        ],
        "spawn": (100, 100)
    },
]

class Player(sprite.Sprite):
    MOVE_SPEED = 7
    WIDTH = 22
    HEIGHT = 32
    COLOR = "#888888"
    JUMP_POWER = 10
    GRAVITY = 0.35

    def __init__(self, x, y):
        super().__init__()
        self.start_pos = (x, y)
        self.xvel = 0
        self.yvel = 0
        self.onGround = False
        self.image = Surface((self.WIDTH, self.HEIGHT))
        self.image.fill(Color(self.COLOR))
        self.rect = Rect(x, y, self.WIDTH, self.HEIGHT)
        self.current_level = 0

    def update(self, left, right, up, platforms):
        # Обработка движения
        self.xvel = -self.MOVE_SPEED if left else self.MOVE_SPEED if right else 0
        if up and self.onGround:
            self.yvel = -self.JUMP_POWER

        # Применение гравитации
        if not self.onGround:
            self.yvel += self.GRAVITY

        self.onGround = False

        # Проверка столкновений по вертикали
        self.rect.y += self.yvel
        self.collide(0, self.yvel, platforms)

        # Проверка столкновений по горизонтали
        self.rect.x += self.xvel
        self.collide(self.xvel, 0, platforms)

    def collide(self, xvel, yvel, platforms):
        for p in platforms:
            if sprite.collide_rect(self, p):
                if p.color == "#FF6262":  # Если платформа - красная
                    self.rect.topleft = self.start_pos
                elif p.color == "#ffff00":  # Если платформа - желтая
                    self.current_level += 1
                    if self.current_level < len(levels):
                        load_level(self.current_level)
                else:  # Если платформа - синяя
                    if xvel > 0:
                        self.rect.right = p.rect.left
                    if xvel < 0:
                        self.rect.left = p.rect.right
                    if yvel > 0:  # Если игрок падает
                        self.rect.bottom = p.rect.top
                        self.onGround = True
                        self.yvel = 0
                    if yvel < 0:
                        self.rect.top = p.rect.bottom
                        self.yvel = 0

class Platform(sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__()
        self.image = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.image.fill(Color(color))
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)
        self.color = color

def load_level(level_index):
    platforms.clear()
    entities.empty()
    spawn_x, spawn_y = levels[level_index]["spawn"]
    hero = Player(spawn_x, spawn_y)
    entities.add(hero)

    for y, row in enumerate(levels[level_index]["layout"]):
        for x, col in enumerate(row):
            color = "#FF6262" if col == "-" else "#0000ff" if col == "+" else "#ffff00" if col == "=" else None
            if color:
                pf = Platform(x * PLATFORM_WIDTH, y * PLATFORM_HEIGHT, color)
                entities.add(pf)
                platforms.append(pf)

    hero.rect.topleft = (spawn_x, spawn_y)
    return hero

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    pygame.display.set_caption("Платформер")
    bg = Surface((WIN_WIDTH, WIN_HEIGHT))
    bg.fill(Color(BACKGROUND_COLOR))

    global entities, platforms
    entities = pygame.sprite.Group()
    platforms = []

    if not levels:
        print("No levels defined!")
        return

    hero = load_level(0)  # Получаем героя из загрузки уровня
    left = right = up = False
    timer = pygame.time.Clock()

    while True:
        for e in pygame.event.get():
            if e.type == QUIT:
                pygame.quit()
                return
            if e.type == KEYDOWN:
                if e.key == K_a: left = True
                if e.key == K_d: right = True
                if e.key == K_w: up = True
            if e.type == KEYUP:
                if e.key == K_a: left = False
                if e.key == K_d: right = False
                if e.key == K_w: up = False

        hero.update(left, right, up, platforms)  # Теперь hero определен
        screen.blit(bg, (0, 0))
        entities.draw(screen)
        pygame.display.update()
        timer.tick(60)

if __name__ == "__main__":
    main()
