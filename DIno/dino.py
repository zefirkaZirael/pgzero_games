import random
import pgzrun

# устанавливаем константы
WIDTH = 900
HEIGHT = 550
TITLE = "Dino"


class Dino(Actor):
    def __init__(self, images, pos):
        super().__init__(images[0], pos)
        self.image_index = 0
        self.frame_rate = 10
        self.frame_counter = 0
        self.images = images
        self.jump_speed = 0
        self.change_x = 10

    def update(self, keyboard):
        if keyboard.space and self.jumping == False:
            self.jump_speed = 14
            self.jumping = True
        self.y -= self.jump_speed
        self.jump_speed -= 0.3
        if self.y > HEIGHT - 100:
            self.y = HEIGHT - 100
            self.jumping = False
        if keyboard.right and self.x <= WIDTH / 2:
            self.x += self.change_x
        elif keyboard.left and self.x >= 0:
            self.x -= self.change_x

    def animate(self):
        self.frame_counter += 1
        if self.frame_counter % self.frame_rate == 0:
            self.image_index += 1
            if self.image_index >= len(self.images):
                self.image_index = 0
            # self.image_index = (self.image_index +1) %len(self.images)
            self.image = self.images[self.image_index]


class Cactus(Actor):
    def __init__(self, images, pos):
        super().__init__(images[0], pos)
        self.iamges = images
        self.speed = 6

    def update(self):
        self.x -= self.speed
        for cactus in cactuses:
            if cactus.x < 0:
                global score
                score += 1
                cactus.image = self.iamges[random.randint(0, 1)]
                cactus.x = random.randint(200, 900) + WIDTH


def draw():
    if game_start:
        screen.blit("desert.png", (0, 0))
        dino.draw()
        for cactus in cactuses:
            cactus.draw()
        screen.draw.text(f"Score: {score}", (10, 20), fontsize=40, color="black")
    else:
        screen.blit("desert_end", (0, 0))


def update():
    global game_start
    if game_start:
        dino.animate()
        dino.update(keyboard)
        for cactus in cactuses:
            cactus.update()
            if cactus.colliderect(dino):
                game_start = False


score = 0

game_start = True
dino_anime = ["dino1", "dino2", "dino3"]
dino = Dino(dino_anime, (100, HEIGHT - 100))
cactus_img = ["cactus2", "cactus3"]
cactuses = []
for i in range(3):
    x = random.randint(200, 900) + WIDTH
    cactus = Cactus(cactus_img, (x, HEIGHT - 50))
    cactuses.append(cactus)
pgzrun.go()
