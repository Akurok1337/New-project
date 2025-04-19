from pygame import *
from random import randint
window = display.set_mode((700, 500))
display.set_caption('Шутер')
background = transform.scale(image.load('galaxy.jpg'), (700,500))

class GameSprite(sprite.Sprite):
    def __init__(self, player_x, player_y, player_image, player_speed, size):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), size)        
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))



class Player(GameSprite):
    def __init__(self, player_x, player_y, player_image, player_speed, size):
        super().__init__(player_x, player_y, player_image, player_speed, size)
        self.can_fire = True
        self.cur_reload = 0
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_a] and self.rect.x > 0:
            self.rect.x -= 10
        if keys_pressed[K_d] and self.rect.x < 650:
            self.rect.x += 10
    def fire(self):
        if self.can_fire:
            keys = key.get_pressed()
            if keys[K_SPACE]:
                bullets.add(Bullet(self.rect.centerx, self.rect.top, 'bullet.png', 5, (10, 10)))
            self.can_fire = False
        else:
            global FPS
            self.cur_reload += 1/FPS
            print(self.cur_reload)
            if self.cur_reload > 0.3:
                self.can_fire = True
                self.cur_reload = 0 

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > 500:
            self.rect.y = 0
            self.rect.x = randint(30, 630)
            global alive
            alive += 1
            global skip
            skip = font.render('Skipped: ' + str(alive), True, (255, 215, 0))




class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            bullet.kill() 
        


    

rocket = Player(50, 400, "rocket.png", 10, size = (65, 65))
ufo = Enemy(300, 100, "ufo.png", 5, size = (65, 65))
ufo2 = Enemy(400, 100, "ufo.png", 5, size = (65, 65))
ufo3 = Enemy(200, 100, "ufo.png", 5, size = (65, 65))
ufo4 = Enemy(500, 100, "ufo.png", 5, size = (65, 65))
ufo5 = Enemy(600, 100, "ufo.png", 5, size = (65, 65))
ufo6 = Enemy(650, 100, "ufo.png", 5, size = (65, 65))
ufo7 = Enemy(250, 100, "ufo.png", 5, size = (65, 65))
ufo8 = Enemy(350, 100, "ufo.png", 5, size = (65, 65))
ufo9 = Enemy(450, 100, "ufo.png", 5, size = (65, 65))
ufo10 = Enemy(550, 100, "ufo.png", 5, size = (65, 65))
bullet = Bullet(50, 400, 'bullet.png', 5, size = (10,10))



ufos = sprite.Group()
ufos.add(ufo)
ufos.add(ufo2)
ufos.add(ufo3)
ufos.add(ufo4)
ufos.add(ufo5)
ufos.add(ufo6)
ufos.add(ufo7)
ufos.add(ufo8)
ufos.add(ufo9)
ufos.add(ufo10)


bullets = sprite.Group()
bullets.add(bullet)



clock = time.Clock()
FPS = 60

mixer.init()
mixer.music.load("space.ogg")
mixer.music.play()

font.init()
font = font.SysFont('Arial', 70)
score = font.render('Score: 0', True, (255, 215, 0))
skip = font.render('Skipped: 0', True, (255, 215, 0)) 
win = font.render('Win!', True, (255, 215, 0))
fail = font.render('Fail!', True, (255, 215, 0))

killed = 0
alive = 0

game = True
finish = False
while game:
    clock.tick(FPS)
    if not finish:
        window.blit(background, (0,0))
        rocket.reset()
        rocket.update()
        ufos.update()
        ufos.draw(window)
        bullets.draw(window)
        bullets.update()
        rocket.fire()
        window.blit(score, (0,0))
        window.blit(skip, (0,50))
        


        if sprite.groupcollide(ufos, bullets, True, False):
            ufo = Enemy(randint(20, 650), 100, "ufo.png", 5, size = (65, 65))
            ufos.add(ufo)
            killed += 1
            score = font.render('Score: ' + str(killed), True, (255, 215, 0))
        
        if killed > 10:
            window.blit(win, (200, 250))
            finish = True

        if alive > 20:
            window.blit(fail, (200,250))
            finish = True
        
        display.update()

    for e in event.get():
        if e.type == QUIT:
            game = False
    
  