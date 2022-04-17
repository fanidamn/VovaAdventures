"""
 __   __                _      _             _                                     __   _                         _      _         
 \ \ / /____ ____ _    /_\  __| |_ _____ _ _| |_ _  _ _ _ ___ ___  __ _____ _ _   /  \ / |  _ __ _ _ ___ ___ __ _| |_ __| |_  __ _ 
  \ V / _ \ V / _` |  / _ \/ _` \ V / -_) ' \  _| || | '_/ -_|_-<  \ V / -_) '_| | () || | | '_ \ '_/ -_)___/ _` | | '_ \ ' \/ _` |
   \_/\___/\_/\__,_| /_/ \_\__,_|\_/\___|_||_\__|\_,_|_| \___/__/   \_/\___|_|    \__(_)_| | .__/_| \___|   \__,_|_| .__/_||_\__,_|
                                                                                           |_|                     |_|             

"""

import pygame, random
import tkinter as tk
from tkinter import *
from tkinter.ttk import *

# COLORs BLOCK
WHITE =     (255, 255, 255)
BLACK =     (0, 0, 0)
RED =       (255, 0, 0)
GREEN =     (0, 255, 0)
BLUE =      (0, 0, 255)
YELLOW =    (255, 255, 0)
WIDTH = 1920
HEIGHT = 1080
# launcher window
window = Tk()

# win sett
window.title("VA 0.1")
window.geometry('230x70')  

def GAME_INITIALIZE():
    window.destroy()
    # icon set
    icon = pygame.image.load("resources/rc.png")
    pygame.display.set_icon(icon)

    # game initialize
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((1920, 1080))
    pygame.display.set_caption(f"Vova Adventures [1920x1080]")
    pygame.font.init()
    pygame.mixer.music.load("resources/ost.mp3")
    pygame.mixer.music.set_volume(0.25)
    pygame.mixer.music.play(-1)

    # res-cs
    bullet_img = pygame.image.load("resources/bullet.png")
    bullet_img = pygame.transform.scale(bullet_img, (70, 50))

    vova_shooter = pygame.image.load("resources/vova.png")
    vova_shooter = pygame.transform.scale(vova_shooter, (130, 95))

    agent_mobs = pygame.image.load("resources/agent.png")
    agent_mobs = pygame.transform.scale(agent_mobs, (70, 110))

    background = pygame.image.load("resources/bg.png")
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))

    bg = pygame.image.load("resources/gameover.png")
    bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))

    bg_boss = pygame.image.load("resources/bg_boss.png")
    bg_boss = pygame.transform.scale(bg_boss, (WIDTH, HEIGHT))

    tarelka_img = pygame.image.load("resources/tarelka.png")
    tarelka_img = pygame.transform.scale(tarelka_img, (100, 70))

    boss_img = pygame.image.load("resources/boss.png")
    boss_img = pygame.transform.scale(boss_img, (300, 150))

    win_bg = pygame.image.load("resources/win.png")
    win_bg = pygame.transform.scale(win_bg, (WIDTH, HEIGHT))

    now = 0
    last = 0

    myfont = pygame.font.SysFont('Arial', 30)
    clock = pygame.time.Clock()

    # class block
    class Player(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image = vova_shooter
            self.rect = self.image.get_rect()
            self.rect.centerx = WIDTH / 2
            self.rect.bottom = HEIGHT - 10
            self.speedx = 0

        def update(self):
            self.speedx = 0
            keystate = pygame.key.get_pressed()
            if keystate[pygame.K_LEFT]:
                self.speedx = -8
            if keystate[pygame.K_RIGHT]:
                self.speedx = 8
            self.rect.x += self.speedx
            if self.rect.right > WIDTH:
                self.rect.right = WIDTH
            if self.rect.left < 0:
                self.rect.left = 0

        def shoot(self):
            bullet = Bullet(self.rect.centerx, self.rect.top)
            all_sprites.add(bullet)
            bullets.add(bullet)

    class Mob(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image = agent_mobs
            self.rect = self.image.get_rect()
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(3, 10)
            self.speedx = random.randrange(-1, 5)

        def update(self):
            self.rect.x += self.speedx
            self.rect.y += self.speedy
            if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
                self.rect.x = random.randrange(WIDTH - self.rect.width)
                self.rect.y = random.randrange(-100, -40)
                self.speedy = random.randrange(4, 18)

    class Boss(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image = boss_img
            self.rect = self.image.get_rect()
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(100, 300)
            self.speedy = 0
            self.speedx = random.randrange(-13, 13)
            if self.speedx > -3 and self.speedx < 3:
                    self.speedx += 4

        def update(self):
            self.rect.x += self.speedx
            self.rect.y += 0
            if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
                self.rect.x = random.randrange(0, 1920)
                self.rect.y = 300
                self.speedy = 0
                self.speedx = random.randrange(-13, 13)
                if self.speedx > -3 and self.speedx < 3:
                    self.speedx += 4

        def shoot(self):
            tarelka = Tarelka(self.rect.centerx, self.rect.top)
            all_sprites.add(tarelka)
            tarelki.add(tarelka)

    class Tarelka(pygame.sprite.Sprite):
        def __init__(self, x, y):
            pygame.sprite.Sprite.__init__(self)
            self.image = tarelka_img
            self.rect = self.image.get_rect()
            self.rect.bottom = y
            self.rect.centerx = x
            self.speedy = -10

        def update(self):
            self.rect.y -= self.speedy
            if self.rect.top < 0:
                self.kill()

    class Bullet(pygame.sprite.Sprite):
        def __init__(self, x, y):
            pygame.sprite.Sprite.__init__(self)
            self.image = bullet_img
            self.rect = self.image.get_rect()
            self.rect.bottom = y
            self.rect.centerx = x
            self.speedy = -10

        def update(self):
            self.rect.y += self.speedy
            if self.rect.bottom < 0:
                self.kill()

    all_sprites = pygame.sprite.Group()
    mobs = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    tarelki = pygame.sprite.Group()
    PLAYERHEALTH = 100
    GAME_STATE = "1"
    SHOOTS = 0
    KILLED = 0
    BOSSHEALTH = 300
    player = Player()
    all_sprites.add(player)
    for i in range(70):
        m = Mob()
        all_sprites.add(m)
        mobs.add(m)


    # game cycle
    running = True
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:
                    if GAME_STATE == "PRE_BOSS":
                        GAME_STATE = "BOSS"
                        for i in mobs:
                            mobs.remove(i)
                            all_sprites.remove(i)
                        boss = Boss()
                        all_sprites.add(boss)
                        PLAYERHEALTH = 300  
                        KILLED = 0
                    elif GAME_STATE == "OVER":
                        GAME_STATE = "1"
                        SHOOTS = 0
                        PLAYERHEALTH = 100
                        KILLED = 0
                    else:
                        player.shoot()
                        SHOOTS += 1

        screen.fill(BLACK)  
        screen.blit(background, (0, 0))

        if GAME_STATE != "OVER":
            # Обновление
            all_sprites.update()

            if GAME_STATE == "1":

                hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
                for hit in hits:
                    KILLED += 1
                    m = Mob()
                    all_sprites.add(m)
                    mobs.add(m)

                textsurface = myfont.render(f'HP: {PLAYERHEALTH} S: {SHOOTS} K: {KILLED}', False, (255, 255, 255))
                screen.blit(textsurface, (WIDTH/1.20, HEIGHT/1.05))

                # Проверка, не ударил ли моб игрока
                hits = pygame.sprite.spritecollide(player, mobs, True)
                if hits:
                    PLAYERHEALTH -= 2

                # проверка на здоровье
                if PLAYERHEALTH <= 0:
                    GAME_STATE = "OVER"

                if KILLED >= 150:
                    GAME_STATE = "PRE_BOSS"

            elif GAME_STATE == "BOSS":
                # BOSS STATE
                if last == 0:
                    boss.shoot()
                    now = pygame.time.get_ticks()
                if last > now + 200:
                    now = pygame.time.get_ticks()
                    boss.shoot()

                screen.blit(background, (0, 0))
                textsurface = myfont.render(f'HP: {PLAYERHEALTH} S: {SHOOTS}  BOSS: {BOSSHEALTH} HP', False, (255, 255, 255))
                screen.blit(textsurface,(WIDTH/1.3, HEIGHT/1.2))

                # проверка на попадание в босса
                BOSS_HITS = pygame.sprite.spritecollide(boss, bullets, True)
                for HIT in BOSS_HITS:
                    BOSSHEALTH -= 1

                # проверка, не попала ли тарелка по голове
                tarelka_hits = pygame.sprite.spritecollide(player, tarelki, True)
                if tarelka_hits:
                    PLAYERHEALTH -= 5

                # проверка на здоровье
                if PLAYERHEALTH <= 0:
                    GAME_STATE = "OVER"

                # проверка здоровья босса
                if BOSSHEALTH <= 0:
                    GAME_STATE = "WIN"

        if GAME_STATE == "PRE_BOSS":
            screen.blit(bg_boss, (0, 0))
            textsurface = myfont.render('! BOSS FIGHT | Press SPACE!', False, (255, 255, 255))
            screen.blit(textsurface,(WIDTH/2, HEIGHT/2))

        elif GAME_STATE == "OVER":
            if len(mobs) == 0:
                for i in range(30):
                    m = Mob()
                    all_sprites.add(m)
                    mobs.add(m)
                all_sprites.remove(boss)
                for i in tarelki:
                    all_sprites.remove(i)
            screen.blit(bg, (0, 0))
            textsurface = myfont.render('Game Over! Press SPACE to restart.', False, (0, 0, 0))
            screen.blit(textsurface,(WIDTH/2, HEIGHT/2))

        elif GAME_STATE == "WIN":
            screen.blit(win_bg, (0, 0))
            textsurface = myfont.render('YOU WIN! Escape to leave.', False, (255, 255, 255))
            screen.blit(textsurface,(WIDTH/2, HEIGHT/2))

        else:
            # Рендеринг
            all_sprites.draw(screen)
        last = pygame.time.get_ticks()
        # После отрисовки всего, переворачиваем экран
        pygame.display.flip()
    pygame.quit()

res_text = Label(window, text="Разрешение: 1920x1080")  
res_text.grid(column=0, row=0)  

def START_GAME():
    GAME_INITIALIZE()

def EXIT_GAME():
    exit()

# start game
start_btn = Button(window, text="Запуск", command=START_GAME)
start_btn.grid(column=0, row=1)  

exit_btn = Button(window, text="Выйти", command=EXIT_GAME)
exit_btn.grid(column=1, row=1)  

author = Label(window, text="куда я попал")  
author.grid(column=0, row=2)

ver_text = Label(window, text="v0.1 pre-alpha")  
ver_text.grid(column=1, row=2)

window.iconphoto(False, tk.PhotoImage(file='resources/rc.png'))
window.mainloop()