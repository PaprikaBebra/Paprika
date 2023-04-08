from pygame import *

#создай окно игры
window_width = 1000
window_height = 1000
window = display.set_mode((window_width,window_height))

#задай фон сцены
display.set_caption('Егор Какашка')
background = transform.scale(image.load('general.png'),(window_width,window_height))

clock = time.Clock()
FPS = 60

speed = 10

game = True

class GameSprite(sprite.Sprite):
    def __init__(self,player_image,player_x,player_y,player_speed):
      super().__init__()
      self.image = transform.scale(image.load(player_image),(65,65))
      self.speed = player_speed
      self.rect = self.image.get_rect()
      self.rect.x = player_x
      self.rect.y = player_y

    def reset(self):
      window.blit(self.image, (self.rect.x,self.rect.y))

class Wall(sprite.Sprite):
  def __init__(self,color_1,color_2,color_3,wall_width,wall_height,wall_x,wall_y):
    super().__init__()
    self.image = Surface((wall_width,wall_height))
    self.image.fill((color_1,color_2,color_3))
    self.rect = self.image.get_rect()
    self.rect.x = wall_x
    self.rect.y = wall_y
  def draw_wall(self):
    window.blit(self.image,(self.rect.x, self.rect.y))


class Player(GameSprite):

  def update(self):
    keys_pressed = key.get_pressed()

    if keys_pressed[K_LEFT] and self.rect.x>5:
      self.rect.x -= self.speed
      
    if keys_pressed[K_RIGHT] and self.rect.x<920:
      self.rect.x += self.speed
    if keys_pressed[K_UP] and self.rect.y>5:
      self.rect.y -= self.speed
    if keys_pressed[K_DOWN] and self.rect.y<920:
      self.rect.y += self.speed

class Enemy(GameSprite):
  def __init__(self,player_image,player_x,player_y,player_speed):
    super().__init__(player_image,player_x,player_y,player_speed)
    self.direction = 'left'

  def update(self):
    if self.rect.x <=600:
      self.direction = 'right'

    if self.rect.x >=920:
      self.direction = 'left'

    if self.direction=='left':
      self.rect.x-=self.speed
    else:
      self.rect.x+=self.speed
    
x1 = 500
y1 =250

x2 = 400
y2 = 200

player = Player("sonic.png", 400, 200, 10)
NPC = Enemy("exesonic.png", 200, 450, 10)
treasure = GameSprite("zoloto.png", 100, 100, 0)

wall1 = Wall(100,200,190,50,100,500,600)
wall2 = Wall(200,1,50,50,100,200,700)
wall3 = Wall(100,100,100,50,100,550,200)

mixer.init()
mixer.music.load('gachifiksiki.mp3')
mixer.music.play()

font.init()
font = font.Font(None,70)

win = font.render('УРА ПОБЕДА',True,(255,215,0))
lose = font.render('ПРОСТО ДАЙТЕ МНЕ ПУЛЬТ...',True,(200,100,2))

finish = False 

money = mixer.Sound('money.ogg')
kick = mixer.Sound('kick.ogg')

while game:

  for e in event.get():
    if e.type == QUIT:
      game = False

  if finish !=True:

    window.blit(background,(0,0))

    NPC.update()
    player.update()

    wall1.draw_wall()
    wall2.draw_wall()
    wall3.draw_wall()

    player.reset()
    NPC.reset()
    treasure.reset()

    if sprite.collide_rect(player, NPC) or sprite.collide_rect(player, wall1) or sprite.collide_rect(player, wall2)or sprite.collide_rect(player, wall3):
      finish = True
      window.blit(lose, (200, 200))
      kick.play()

    if sprite.collide_rect(player, treasure):
      finish = True
      window.blit(win, (200, 200))
      money.play()

  clock.tick(FPS)
  display.update()