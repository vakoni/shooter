from pygame import *
from random import randint
from time import time as timer

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))  

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x< 620:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)

lost = 0
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > 500:
            self.rect.x = randint(80, 620)
            self.rect.y = 0
            lost = lost + 1            
class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

         

window = display.set_mode((700, 500))
display.set_caption("Shooter Game")
Clock = time.Clock()
background = transform.scale(image.load("galaxy.jpg"), (700, 500))
FPS = 40
player = Player('rocket.png', 5, 420, 80, 100, 10)
score = 0
goal = 10
max_lost = 10
life = 3
num_fire = 0
rel_time = False

monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy('ufo.png', randint(80, 620), -40, 80, 50, randint(1, 5))
    monsters.add(monster)
asteroids = sprite.Group()
for i in range(1, 3):
    asteroid = Enemy('asteroid.png', randint(80, 620), -40, 80, 50, randint(1, 4))
    asteroids.add(asteroid) 
bullets = sprite.Group()      
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')
font.init()
font1 = font.SysFont('Arial', 80)
font2 = font.SysFont('Arial', 36)
win = font1.render("YOU WIN!" , True, (154, 205, 50)) 
lose = font1.render("YOU LOSE!", True, (180, 0, 0))
game = True
finish = False
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    fire_sound.play()
                    player.fire()
                    num_fire = num_fire + 1
                if num_fire >= 5 and rel_time == False:
                    lost_time = timer()   
                    rel_time = True
       
    if finish != True:
        window.blit(background,(0, 0))
        player.update()
        monsters.update()
        asteroids.update()
        bullets.update()
        player.reset()   
        monsters.draw(window)
        asteroids.draw(window)
        bullets.draw(window)
        if rel_time == True:
            now_time = timer()
            if now_time - lost_time < 3:
                timing = font2.render("Перезарядка:", 1, (150, 0, 0))
                window.blit(timing, (260, 460))
            else:
                num_fire = 0
                rel_time = False 
        collides = sprite.groupcollide(monsters, bullets, True, True)        
        for c in collides:
            score += 1
            monster = Enemy('ufo.png', randint(80, 620), -40, 80, 50, randint(1, 5))
            monsters.add(monster)
        if sprite.spritecollide(player, monsters, False) or sprite.spritecollide(player, asteroids, False):
            sprite.spritecollide(player, monsters, True)
            sprite.spritecollide(player, asteroids, True)
            life = life - 1
        if life == 0 or lost >= max_lost:
            finish = True  
            window.blit(lose, (200, 200))  
        if score >= goal:
            finish = True
            window.blit(win, (200, 200)) 
        text = font2.render("Score:" + str(score), 1, (255, 255, 255))  
        window.blit(text, (10, 20))
        text_lose = font2.render("Lose:" + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))       
        if life == 3:
            life_color = (0, 150, 0)
        if life == 2:
            life_color = (150, 150, 0)
        if life == 1:
            life_color = (150, 0, 0)

        text_life = font1.render(str(life), 1, life_color)
        window.blit(text_life, (650, 10))

        
        display.update()

    else:
        finish = False
        score = 0
        lost = 0
        num_fire = 0
        life = 3
        for b in bullets:
            b.kill()
        for a in asteroids:
            a.kill()

        time.delay(3000)
        for i in range(1, 6):
            monster = Enemy('ufo.png', randint(80, 620), -40, 80, 50, randint(1, 5))
            monsters.add(monster)
        for i in range(1, 3):
            asteroid = Enemy('asteroid.png', randint(80, 620), -40, 80, 50, randint(1, 4))
            asteroids.add(asteroid)   
    time.delay(50)          


#Clock.tick(FPS)   
      
      
