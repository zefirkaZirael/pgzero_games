import pgzrun
import random

WIDTH = 950
HEIGHT = 550
TITLE = "Platformer"

game_running = False
music_on = True
game_over = False
music.play('background_music')

## MENU ACTOR
lifes_button = Actor('hud/lifes', (WIDTH - 100, 50))
start_button = Actor('double/button_brown', (WIDTH // 2, HEIGHT // 2 - 100))
sound_button = Actor('double/button_brown', (WIDTH // 2, HEIGHT // 2))
exit_button = Actor('double/button_red', (WIDTH // 2, HEIGHT // 2 + 100))
pause_button = Actor('double/button_red', (50, 50))
end_icon = Actor('double/end', (WIDTH // 2, HEIGHT // 2))

## GAME ACTOR
bg = Actor("background/bg_layer4", center=(WIDTH / 2, 0))
bg2 = Actor("background/bg_layer3", center=(WIDTH, 250))

platform_images = ['environment/ground_cake', 'environment/ground_cake_broken',
                   'environment/ground_cake_small', 'environment/ground_cake_small_broken']
platforms = []
enemies = []
player_speed = 10
platform_number = 10

pause = False


class Character(Actor):
    def __init__(self, image, pos):
        super().__init__(image, pos)
        self.animation_frames1 = ['players/bunny1_ready', 'players/bunny1_stand']
        self.animation_right_f = ['players/bunny1_walk1', 'players/bunny1_walk2']
        self.animation_left_f = ['players/left1', 'players/left']
        self.current_frame = 0
        self.frame_counter = 0
        self.frame_rate_stay = 20
        self.frame_rate_move = 10
        self.health = 3
        self.player_jump = 0
        self.landed = False
        self.jumping = False

    def animation_stay(self):
        self.frame_counter += 1
        if self.frame_counter % self.frame_rate_stay == 0:
            self.image = self.animation_frames1[self.current_frame]
            self.current_frame = (self.current_frame + 1) % len(self.animation_frames1)

    def animation_right(self):
        self.frame_counter += 1
        if self.frame_counter % self.frame_rate_move == 0:
            self.image = self.animation_right_f[self.current_frame]
            self.current_frame = (self.current_frame + 1) % len(self.animation_right_f)

    def animation_left(self):
        self.frame_counter += 1
        if self.frame_counter % self.frame_rate_move == 0:
            self.image = self.animation_left_f[self.current_frame]
            self.current_frame = (self.current_frame + 1) % len(self.animation_left_f)

    ## JUMPS
    def on_platform(self, platforms):
        for platform in platforms:
            if (self.colliderect(platform)) and platform.top + 20 >= self.bottom >= platform.top > self.y:
                return platform
        return None

    def gravity_check(self, platforms):
        if not self.on_platform(platforms) and self.bottom < HEIGHT:
            return True
        return False

    def jump_check(self, platforms):
        self.y -= self.player_jump
        if self.gravity_check(platforms):
            self.player_jump -= 0.4
            self.landed = False
        else:
            if not self.landed and self.jumping:
                sounds.footstep_grass_001.play()
                self.landed = True
            self.player_jump = 0
            self.jumping = False
            platform = self.on_platform(platforms)
            if platform:
                self.bottom = platform.top

    def move(self, direction, player_speed):
        if direction == 'left':
            self.animation_left()
            self.x -= player_speed
            if self.left < 0:
                self.left = 0
        elif direction == 'right':
            self.animation_right()
            if self.right < WIDTH // 2:
                self.x += player_speed
            else:
                move_backgrounds()
                move_platforms(-player_speed)
        else:
            self.animation_stay()

    def jump(self):
        if not self.jumping:
            self.player_jump = 15
            self.jumping = True

    def check_for_collison(self, enemies):
        for enemy in enemies:
            if self.colliderect(enemy):
                self.health -= 1
                sounds.impactglass_heavy_003.play()
                self.x = 100
                self.y = HEIGHT - 100
                if self.health <= 0:
                    global game_over, game_running
                    game_over = True
                    game_running = False
                break

    def update(self, player_speed, keyboard):
        if keyboard.up:
            self.jump()
        if keyboard.left:
            self.move('left', player_speed)
        elif keyboard.right:
            self.move('right', player_speed)
        else:
            self.move('None', player_speed)


class Enemy(Actor):
    def __init__(self, image, pos):
        super().__init__(image, pos)
        self.animation_f = ['enemies/wingman1', 'enemies/wingman2', 'enemies/wingman3', 'enemies/wingman4',
                            'enemies/wingman5', 'enemies/wingman4', 'enemies/wingman3', 'enemies/wingman2']
        self.current_frame = 0
        self.frame_counter = 0
        self.frame_rate = 10
        self.speed = 2

    def animation(self):
        self.frame_counter += 1
        if self.frame_counter % self.frame_rate == 0:
            self.image = self.animation_f[self.current_frame]
            self.current_frame = (self.current_frame + 1) % len(self.animation_f)

    def move(self, platform):
        self.x += self.speed
        if self.left < platform.left or self.right > platform.right:
            self.speed = - self.speed

        ## MENU


def on_mouse_down(pos):
    sounds.switch19.play()
    global game_running, music_on, pause
    if not game_over and not game_running:
        if start_button.collidepoint(pos):
            game_running = True
        elif sound_button.collidepoint(pos):
            music_on = not music_on
            if music_on:
                music.play('background_music')
            else:
                music.stop()
        elif exit_button.collidepoint(pos):
            exit()
    if game_running:
        if pause_button.collidepoint(pos):
            game_running = False
            pause = True
    if game_over:
        if end_icon.collidepoint(pos):
            exit()



## PLATFORMS
def spawn_platform():
    for i in range(platform_number):
        img = random.choice(platform_images)
        y = random.randint(200, HEIGHT - 50)
        x = 500 * i + WIDTH
        plat_change_x = 0
        platform = Actor(img, (x, y))
        platforms.append(platform)

        if random.random() < 0.4:
            enemy = Enemy('enemies/wingman1', (x, platform.top - 60))  # Adjust the enemy's y-position
            enemies.append(enemy)
    while len(enemies) <= 3:
        enemy = Enemy('enemies/wingman1', (x, platform.top - 60))  # Adjust the enemy's y-position
        enemies.append(enemy)


spawn_platform()


def move_platforms(change_x):
    for enemy in enemies:
        enemy.x += change_x
    for i in range(platform_number):
        platforms[i].x += change_x
        if platforms[i].right <= 0:
            platforms[i].left = platforms[i - 1].right + 300
            platforms[i].y = random.randint(200, HEIGHT - 50)
            for enemy in enemies:
                if random.random() < 0.3 and enemy.right <= 0:
                    enemy.x = platforms[i].x
                    enemy.y = platforms[i].top - 60


## BACKGROUND

def move_backgrounds():
    global player_speed
    bg.x -= player_speed
    bg2.x -= player_speed
    if bg.right <= 0:
        bg.left = bg2.right
    if bg2.right <= 0:
        bg2.left = bg.right


### SYSTEM
def draw():
    if game_running:
        screen.fill((224, 254, 255))
        bg.draw()
        bg2.draw()
        hero.draw()
        pause_button.draw()
        lifes_button.draw()
        screen.draw.text("Пауза", center=pause_button.center, fontsize=40, color="black")
        screen.draw.text(f'{hero.health}', center=(lifes_button.right + 10, lifes_button.centery + 10), fontsize=40,
                         color="black")

        for platform in platforms:
            platform.draw()
        for enemy in enemies:
            enemy.draw()
    elif game_over:
        screen.fill((224, 254, 255))
        end_icon.draw()
        screen.draw.text("Game over", center=end_icon.center, fontsize=40, color="black")

    else:
        screen.fill((224, 254, 255))
        start_button.draw()
        sound_button.draw()
        exit_button.draw()
        if pause:
            screen.draw.text("Продолжить", center=start_button.center, fontsize=40, color="black")
        else:
            screen.draw.text("Начать игру", center=start_button.center, fontsize=40, color="black")
        screen.draw.text("Музыка", center=sound_button.center, fontsize=40, color="black")
        screen.draw.text("Выход", center=exit_button.center, fontsize=40, color="black")


def update():
    if game_running:
        hero.update(player_speed, keyboard)
        for enemy in enemies:
            enemy.animation()
            for platform in platforms:
                if platform.left <= enemy.x <= platform.right:
                    enemy.move(platform)
        hero.jump_check(platforms)
        hero.check_for_collison(enemies)


hero = Character("players/bunny1_stand", (100, HEIGHT - 100))
pgzrun.go()
