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

y = height-20
dt = clock.tick(FPS) / 1000

pygame.mixer.init()
pygame.mixer.music.set_volume(1)


class Cactus(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.width=30
        self.height=60
        self.image=pygame.transform.scale(pygame.image.load("data/image/cactus.png"), (self.width, self.height))
        self.rect = self.image.get_rect()  # Get rect of some size as 'image'.
        self.rect.left=width
        self.rect.top=y-self.height
    def update(self):
        self.rect.left-=2
        
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.size = 64
        self.image = pygame.Surface((self.size,self.size))
#        self.image.fill(WHITE)
        self.image_jump=pygame.transform.scale(pygame.image.load("data/image/dino_jump.png"), (self.size, self.size))
        self.image_run0=pygame.transform.scale(pygame.image.load("data/image/dino_run0.png"), (self.size, self.size))
        self.image_run1=pygame.transform.scale(pygame.image.load("data/image/dino_run1.png"), (self.size, self.size))
        self.rect = self.image.get_rect()  # Get rect of some size as 'image'.
        self.rect.left=20
        self.rect.top=y-self.size
        self.velocity = [0, 0]
        self.jump_top = self.rect.top-self.size*2
        self.no_jump_top = self.rect.top
        self.is_jump=False
        self.step=0
        self.image = self.image_run0
    def update(self):
        if self.is_jump:
            self.image = self.image_jump
        else:
            self.step+=1
            if self.step%10==0:
                self.image = self.image_run0
            if self.step%20==0:
                self.image = self.image_run1
        if self.rect.top<=self.jump_top:
            self.velocity[1] = self.no_jump_top * dt
        self.rect.move_ip(*self.velocity)
        if self.rect.top>=self.no_jump_top:
            self.velocity[1] = 0
            game.player.is_jump=False

class Game():
    def __init__(self):
        self.restart()
    def restart(self):
        self.player=Player()
        self.loop=True
        self.gameover=False
        self.cactus_list=[]
        self.km=0

game = Game()
running = True


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
        if game.km%150==0:
            game.cactus_list.append(Cactus())
        game.km+=1
        game.player.update()
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
        pygame.display.update()

print("Exited the game loop. Game will quit...")
quit()
