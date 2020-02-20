import pygame
import random
successes, failures = pygame.init()
print("Initializing pygame: {0} successes and {1} failures.".format(successes, failures))

width=720
height=280

screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
FPS = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

y = height-10


pygame.mixer.init()
pygame.mixer.music.set_volume(1)


class Cactus(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        if random.randint(0,1)==0:
            self.width=35
            self.height=70
            self.image=pygame.transform.scale(pygame.image.load("data/image/cactus.png"), (self.width, self.height))
        else:
            self.width=70
            self.height=70
            self.image=pygame.transform.scale(pygame.image.load("data/image/cactusbig.png"), (self.width, self.height))
        self.rect = self.image.get_rect()  # Get rect of some size as 'image'.
        self.rect.left=width+random.randint(0,200)
        self.rect.top=y-self.height
    def update(self):
        self.rect.left-=2
        
class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.width=90
        self.height=27
        self.image=pygame.transform.scale(pygame.image.load("data/image/cloud.png"), (self.width, self.height))
        self.rect = self.image.get_rect()  # Get rect of some size as 'image'.
        self.rect.left=width
        self.rect.top=20
    def update(self):
        self.rect.left-=1
class Bg(pygame.sprite.Sprite):
    def __init__(self,left):
        super().__init__()
        self.width=410
        self.height=28
        self.image=pygame.transform.scale(pygame.image.load("data/image/bg.png"), (self.width, self.height))
        self.rect = self.image.get_rect()  # Get rect of some size as 'image'.
        self.rect.left=left
        self.rect.top=y-self.height
    def update(self):
        if self.rect.left==-1*self.width:
            self.rect.left=width
        self.rect.left-=2
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.size = 80
        self.image = pygame.Surface((self.size,self.size))
#        self.image.fill(WHITE)
        self.image_jump=pygame.transform.scale(pygame.image.load("data/image/dino_jump.png"), (self.size, self.size))
        self.image_run0=pygame.transform.scale(pygame.image.load("data/image/dino_run0.png"), (self.size, self.size))
        self.image_run1=pygame.transform.scale(pygame.image.load("data/image/dino_run1.png"), (self.size, self.size))
        self.rect = self.image.get_rect()  # Get rect of some size as 'image'.
        self.rect.left=50
        self.rect.top=y-self.size
        self.velocity = [0, 0]
        self.jump_top = self.rect.top-self.size*1.5
        self.no_jump_top = self.rect.top
        self.is_jump=False
        self.step=0
        self.image = self.image_run0
        self.jump_speed=2
    def update(self):
        
        if self.is_jump:
            self.image = self.image_jump
            self.rect.top-=self.jump_speed
            if abs(self.rect.top-self.jump_top)<self.jump_speed:
                self.jump_speed*=-1
            if self.rect.top==self.no_jump_top:
                self.jump_speed*=-1
                self.is_jump=False
        else:
            self.step+=1
            if self.step%10==0:
                self.image = self.image_run0
            if self.step%20==0:
                self.image = self.image_run1

class Game():
    def __init__(self):
        self.restart()
    def restart(self):
        self.player=Player()
        self.loop=True
        self.gameover=False
        self.cactus_list=[]
        self.clouds=[]
        self.km=0

game = Game()
running = True

bg1=Bg(0)
bg2=Bg(410)
bg3=Bg(820)



while running:
    dt = clock.tick(FPS) / 1000  # Returns milliseconds between each call to 'tick'. The convert time to seconds.
    

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if game.loop:
                    if not game.player.is_jump:
                        pygame.mixer.music.load('data/sound/jump.wav')
                        pygame.mixer.music.play(0)
                        game.player.velocity[1] = -200 *dt
                        game.player.is_jump=True
                if game.gameover:
                    game.restart()

    if game.loop:
        screen.fill(WHITE)  # Fill the screen with background color.
        if game.km%200==0:
            game.cactus_list.append(Cactus())
        if game.km%600==0:
            game.clouds.append(Cloud())
        game.km+=1
        game.player.update()
        for cloud in game.clouds:
            cloud.update()
            screen.blit(cloud.image, cloud.rect)
            if cloud.rect.left<-100:
                game.clouds.remove(cloud)
        for cactus in game.cactus_list:
            if cactus.rect.left<-100:
                game.cactus_list.remove(cactus)
            else:
                cactus.update()
                screen.blit(cactus.image, cactus.rect)
                if pygame.sprite.collide_rect(cactus, game.player):
                    if abs(cactus.rect.left-game.player.rect.left)<game.player.size/2:
                        if abs(cactus.rect.top-game.player.rect.top)<game.player.size/2:
                            print("game over\n")
                            font=pygame.font.Font(None,56)
                            text=font.render("GAME OVER",1,(10,10,10))
                            center=(screen.get_width()/2,screen.get_height()/2)
                            textpos = text.get_rect(center=center)
                            screen.blit(text,textpos)
                            game.loop=False
                            game.gameover=True
                            pygame.mixer.music.load('data/sound/die.wav')
                            if not pygame.mixer.music.get_busy():
                                pygame.mixer.music.play(0)
        
        font=pygame.font.Font(None,30)
        text=font.render("{} km".format(game.km/100),1,(0,0,0))
        center=(screen.get_width()/2,screen.get_height()/2)
        screen.blit(text,(10,10))
        screen.blit(game.player.image, game.player.rect)
        bg1.update()
        bg2.update()
        bg3.update()
        screen.blit(bg1.image, bg1.rect)
        screen.blit(bg2.image, bg2.rect) 
        screen.blit(bg3.image, bg3.rect)
        pygame.display.update()

print("Exited the game loop. Game will quit...")
quit()
