import random
import pgzrun

# устанавливаем константы
WIDTH = 800
HEIGHT = 600
TITLE = "Star Wars"


class SpaceShip(Actor):
    def __init__(self, image, pos):
        super().__init__(image, pos)

    def update(self):
        if self.right > WIDTH:
            self.right = WIDTH
        if self.left < 0:
            self.left = 0


class Bullet(Actor):
    def __init__(self, image, pos):
        super().__init__(image, pos)
        self.speed = 5

    def update(self):
        self.y -= self.speed
        if self.y > HEIGHT:
            bullets.remove(self)


class Enemy(Actor):
    def __init__(self, images, pos):
        super().__init__(images[0], pos)
        self.images = images
        self.image_index = 0
        self.speed = 2
        self.direction = 1
        self.amplitude = 50
        self.start_x = self.x

    def update(self):
        global lives
        self.speed_x = random.randint(1, 4)
        self.y += self.speed
        self.x += self.direction * self.speed_x
        if abs(self.x - self.start_x) >= self.amplitude:
            self.direction *= -1
        if self.top > HEIGHT:
            lives -=1
            enemies.remove(self)

    def animate(self, ):
        self.image_index += 1
        if self.image_index >= len(self.images):
            self.image_index = 0
        self.image = self.images[self.image_index]

    # класс с игрой


def draw():
    screen.fill((255, 153, 0))
    screen.blit("space_background.png", (0, 0))
    spaceship.draw()
    for bullet in bullets:
        bullet.draw()
    for enemy in enemies:
        enemy.draw()
    screen.draw.text(f"Score: {score}", (10, 20), fontsize=40, color="black")
    screen.draw.text(f"Lives: {lives}", (680, 20), fontsize=40, color="black")
    if not game_start:
        screen.draw.text(f"{label}", (WIDTH / 2 - 100, HEIGHT / 2), fontsize=100, color="black")

    # начальные значения


def update():
    global game_start, score, lives, label
    if game_start:
        spaceship.update()
        for bullet in bullets:
            bullet.update()
        for enemy in enemies:
            enemy.update()
            enemy.animate()
            if spaceship.colliderect(enemy):
                lives -= 1
                enemies.remove(enemy)
        for bullet in bullets:
            for enemy in enemies:
                if bullet.colliderect(enemy):
                    bullets.remove(bullet)
                    enemies.remove(enemy)
                    score += 1
        if len(enemies) == 0 and lives > 0:
            label = "Win"
            game_start = False
        if lives <= 0:
            label = "Loose"
            game_start = False


def on_mouse_move(pos):
    if game_start:
        spaceship.x = pos[0]


def on_mouse_down(pos):
    if game_start:
        bullet = Bullet("laser", (spaceship.x, spaceship.top))
        bullets.append(bullet)
        sounds.laser.play()


spaceship = SpaceShip("x-wing.png", (WIDTH // 2, HEIGHT - 100))
bullets = []
enemy_images = ["tie_fighter", "tie_fighter2"]
enemies = []
for i in range(10):
    x = random.randint(50, WIDTH - 50)
    y = -50 * i
    enemy = Enemy(enemy_images, (x, y))
    enemies.append(enemy)
score = 0
lives = 3
game_start = True
pgzrun.go()
