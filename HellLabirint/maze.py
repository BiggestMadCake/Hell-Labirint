from pygame import*
'''Классы'''
#класс-родитель для спрайтов
class GameSprite(sprite.Sprite):
    #конструктор класса
    def __init__(self, player_image, player_x, player_y, player_w, player_h, player_speed):
        super().__init__()
        #Каждый спрайт должен хранить свойство image - изображение
        self.image = transform.scale(image.load(player_image), (player_w, player_h))
        self.speed = player_speed
        #Каждый спрайт должен хранить свойство rect - прямоугольник в который он вписан
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    #метод отрисовки спрайта
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

#Классы наследники
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < win_height - 80:
            self.rect.y += self.speed    

class Enemy(GameSprite):
    direction = 'left'
    def update(self):
        if self.rect.x <= 500:
            self.direction = 'right'
        if self.rect.x >= win_width - 85:
            self.direction = 'left'
        
        if self.direction == 'left':
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed

class Enemy2(GameSprite):
    direction = 'up'
    def update(self):
        if self.rect.y <= 40:
            self.direction = 'down'
        if self.rect.y >= win_height - 80:
            self.direction = 'up'
        
        if self.direction == 'up':
            self.rect.y -= self.speed
        else:
            self.rect.y +=self.speed

#класс для спрайтов припятсвия
class Wall(sprite.Sprite):
    def __init__(self, red, green, blue, wall_x, wall_y, wall_width,wall_height):
        super().__init__()
        self.red = red
        self.green = green
        self.blue = blue
        self.width = wall_width
        self.height = wall_height
        # картинка стены - прямоугольник нужныхразмеров и цвета
        self.image = Surface((self.width, self.height))
        self.image.fill((red,green,blue))
        #каждый спрайт должен хранить свойство rect - прямоугольник
        self.rect = self.image.get_rect()
        self.rect.x = wall_x
        self.rect.y = wall_y
    def draw_wall(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


#Игровая сцена:
win_width = 700
win_height = 500
window = display.set_mode((win_width,win_height))
display.set_caption('MAZE')
background =  transform.scale(image.load("background.jpg"), (win_width, win_height))

#Персонажи игры:
'''Персонажи игры'''
player = Player('hero.png',5, win_height -80, 80, 80, 4 )
monster = Enemy('cyborg.png', win_width - 80, 280, 65, 65, 2)
final = GameSprite('treasure.png', win_width - 120, win_height - 80, 80, 80, 0)
enemy2 = Enemy2('cyborg.png',120,100,65,65,5)
#стены
w1 = Wall(30, 59, 116, 100, 20 , 450, 10)
w2 = Wall(30, 59, 116, 100, 480, 450, 10)
w3 = Wall(30, 59, 116, 100, 20 , 10, 370)
w4 = Wall(30, 59, 116, 385, 30, 10 , 360)
w5 = Wall(30, 59, 116, 285, 120, 10, 360)
w6 = Wall(30, 59, 116, 185, 30, 10 , 360)
w7 = Wall(30, 59, 116, 485, 120, 10, 360)


'''Игровой цикл'''
game = True
finish = False
clock = time.Clock()
FPS = 60

font.init()
font = font.SysFont('Comic sans Ms', 70)
win = font.render('Molodec!', True, (255, 215, 0))
lose = font.render('Noobik', True, (180, 0, 0))

#Музыка
mixer.init()
#mixer.music.load('jungles.ogg')
#mixer.music.play()

money = mixer.Sound('money.ogg')
kick = mixer.Sound('kick.ogg')

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
  
    if finish != True:
        window.blit(background,(0, 0))
        player.update()
        monster.update()
        enemy2.update()
        player.reset()
        monster.reset()
        final.reset()
        enemy2.reset()
        w1.draw_wall()
        w2.draw_wall()
        w3.draw_wall()
        w4.draw_wall()
        w5.draw_wall()
        w6.draw_wall()
        w7.draw_wall()



        #ситуация "проигрыш"
        if sprite.collide_rect(player, monster) or sprite.collide_rect(player, w1) or sprite.collide_rect(player, w2) or sprite.collide_rect(player,w3) or sprite.collide_rect(player,w4) or sprite.collide_rect(player,w5) or sprite.collide_rect(player, w6) or sprite.collide_rect(player, w7) or sprite.collide_rect(player, enemy2):
            finish = True
            window.blit(lose, (200, 200))
            kick.play()

        #ситуация "вигрыш"
        if sprite.collide_rect(player, final):
            finish = True
            window.blit(win, (200, 200))
            money.play()

    display.update()
    clock.tick(FPS)