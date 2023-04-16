#импортируем pygame
from pygame import *
import os

#устанавливаем размер экрана и устанавливаем текст приложения
window =  display.set_mode((500, 500))
display.set_caption('пинг-понг')

#получаем нашу папку с игрой
dir = os.path.dirname(os.path.realpath(__file__))

#обьявляем логические переменные
#game - работает ли игра
#over - кто-то проиграл ли
game = True
over = False


#класс GameSprite
#передаём путь к картинку, координаты, скорость и размер картинки
class GameSprite(sprite.Sprite):
    def __init__(self, image_str, x, y, speed, wh):
        #получаем картинку
        self.image = transform.scale(image.load(image_str), wh)
        #получаем rect картинки
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
    #метод для отрисовки картинки
    def reset(self):    window.blit(self.image, (self.rect.x, self.rect.y))


#класс для создание игроков, наследник класа GameSprite
#передаём те же данные что и GameSprite только добавляем какие клавишы используем для передвижение
class Player(GameSprite):
    def __init__(self,image_str, x,y, speed, wh, up, down):
        super().__init__(image_str, x,y, speed, wh)
        self.up = up
        self.down = down
        self.score = 0

    def update(self):
        self.reset()
        #получаем нажатиае клавиш
        k = key.get_pressed()
        global over
        #если нажата клавиша для поднятие верх
        #и координаты игрока больше нуля и не кто ещё не проиграл
        if k[self.up] and self.rect.y>0 and over!=True:
            self.rect.y-=self.speed
        #если нажата клавиша чтобы опустится вниз
        #и координаты игрока больше 385 и не кто ещё не проиграл
        if k[self.down] and self.rect.y<385 and over!=True:
            self.rect.y+=self.speed
        #если кто-то проиграл при нажатие пробела устанавливаем over на False
        if k[K_SPACE] and over:
            over = False

#класс для обьекта мяча, так же наследника класса GameSprite
#передаём те же данные что и GameSprite только добавляем скорость для перемещение по оси y
class Circle(GameSprite):
    def __init__(self,image_str, x,y, speed, wh):
        super().__init__(image_str, x,y, speed, wh)
        self.speed_y = 1
    def update(self):
        #если кто-то проиграл то мяч нечего не делает(не отрисовывается и не двигается)
        if (over==True): return
        #отрисовка и перемещения мяча
        self.reset()
        self.rect.x-=self.speed
        self.rect.y-= self.speed_y
        #если игрок столкунлся с одним из игроков меняем его направление по оси x в обратную сторонку
        if (sprite.collide_rect(player_1, self) or sprite.collide_rect(player_2, self)):
            self.speed*=-1
        #если игрок выше или ниже экрана по y то меняем его направление по оси y
        if (self.rect.y<0 or self.rect.y>465):
            self.speed_y*=-1
    
    #метод для респавна мяч(перемещение его обратно в цент экрана)
    def respawn(self):
        self.rect.x = 250
        self.rect.y = 250
            


#кол-во фпс
clock = time.Clock()
FPS = 60
#создаём игроков, мяч и получаем картинку фона
#ps: dir - наша папку, dir+"/file_name" добавляем к нашему пути названиме текстуры
bakcground = transform.scale(image.load(dir+"/background.png"), (500, 500))
player_1 = Player(dir+"/player.png", 10,210, 5,(32, 120), K_w, K_s)
player_2 = Player(dir+"/player.png", 455,210, 5,(32, 120), K_UP, K_DOWN)
circle = Circle(dir+'/circle.png', 250, 250, 8, (32,32))

#иницилизируем возможности font и создаёт свой шрифт с размером 50
font.init()
font1 = font.Font(None, 50)
#создаём текст GAME OVER
over_t = font1.render('GAME OVER', True, (255,1,1))

#цикл, пока переменная game=True игра работает
while game:
    #перебираем ивенты 
    for e in event.get():
        #в случаем нажатия крестика устанавливаем game на False
        if e.type==QUIT:
            game = False

    #создаём тексты со счётчиками
    score_1 = font1.render('1 PLAYER: '+str(player_2.score), True, (255, 255, 255))
    score_2 = font1.render('2 PLAYER: '+str(player_1.score), True, (255, 255,255))

    #отрисовываем задний фон
    #отрисовываем счётчики (score_1, score_2)
    #отрисовываем игроков(player_1, player_2)
    #отрисовываем мяч(circle)
    window.blit(bakcground, (0,0))
    window.blit(score_1, (0, 0))
    window.blit(score_2, (300, 0))
    player_1.update()
    player_2.update()
    circle.update()

    #если кто-то проиграл отрисовываем надпись GAME OVER
    if (over):
        window.blit(over_t, (125, 250))


    #если мяч пропустил первый игрок(слева)
    # over = True, значит кто-то пропустил мяч
    # circle.respawn, спавни мяч снова по середине экрана
    # добавляем к счётчику второго игрока + 1
    if (circle.rect.x<0):
        over = True
        circle.respawn()
        player_1.score+=1

    #если мяч пропустил второй игрок(справа)
    # over = True, значит кто-то пропустил мяч
    # circle.respawn, спавни мяч снова по середине экрана
    # добавляем к счётчику первого игрока + 1
    if (circle.rect.x>485):
        over = True
        circle.respawn()
        player_2.score+=1

    #устанавливаем кол-во фпс, обновляем экран
    clock.tick(FPS)
    display.update()
