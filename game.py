import pygame, random,  pygame.mixer, time, requests
from pygame.locals import *
from scripts.player import Player, Shot
from scripts.enemy import Enemy

class Game():
    def __init__(self):

        pygame.init()

        self.game_start = True

        self.window_width = 1200 
        self.window_height = 600
        self.window = pygame.display.set_mode((self.window_width, self.window_height))

        self.background = pygame.image.load("img/background.jpg")
        self.background = pygame.transform.scale(self.background, (self.window_width, self.window_height))

        self.player_group = pygame.sprite.Group()
        self.player = Player()
        self.player_group.add(self.player)
        self.player_right = False
        self.player_left = False

        self.shoot_group = pygame.sprite.Group()

        self.create_enemy = True
        self.enemy_group = pygame.sprite.Group()


        #PONTOS E NIVEL
        self.player_points = self.player.points
        self.font = pygame.font.Font("font/8bit.ttf", 30)
        self.points_text = self.font.render("SCORE: " + str(self.player_points), 1, (255,255,255))
        self.level = 0
        self.enemy_in_window = 5
        self.level_text = self.font.render("LEVEL: "+ str(self.level),1,(255,255,255))
        self.mensagem = self.font.render("Pressione S para salvar e sair", 1, (255,255,255))


        #MUSIQUINHA
        pygame.mixer.init()
        pygame.mixer.set_reserved(0)
        self.game_music = pygame.mixer.Sound("sounds/ambiente.wav")
        pygame.mixer.Channel(0).play(self.game_music,-1)


       
        self.fps = pygame.time.Clock()

##
        self.game_init = True
        while self.game_init:
            self.fps.tick(30)
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()

                if event.type == KEYDOWN:
                    if event.key == K_RIGHT:
                        self.player_right = True
                    if event.key == K_LEFT:
                        self.player_left = True
                    if event.key == K_SPACE:
                        self.player_shot = Shot() 
                        self.player_shot.rect[0] = self.player.rect[0]+23 
                        self.player_shot.rect[1] = self.player.rect[1] 
                        self.shoot_group.add(self.player_shot)
                        pygame.mixer.Channel(1).play(pygame.mixer.Sound("sounds/tiro.wav")) 

                    #bd
                    if event.key == K_s:
                        URL = "http://localhost:5000/incluir/Rank"
                        dados = {"score": self.player_points}
                        enviar_dados = requests.post(URL, json=dados)
                        pygame.quit()

                if event.type == KEYUP: 
                    if event.key == K_RIGHT:
                        self.player_right = False
                    if event.key == K_LEFT:
                        self.player_left = False

            if self.player_right: 
                self.player.rect[0] += self.player.speed
            if self.player_left: 
                self.player.rect[0] -= self.player.speed

            self.window.fill("black")
            self.window.blit(self.background,(0,0))
            self.window.blit(self.points_text,(850,10))
            self.window.blit(self.level_text,(650,10))
            self.window.blit(self.mensagem,(0,10))
            self.shoot_group.update()
            self.player_group.update()
            self.player_group.draw(self.window)
            self.enemy_group.update()
            self.enemy_group.draw(self.window)


            if len(self.enemy_group) < 5:
                for i in range(3):
                    self.enemy = Enemy()
                    self.enemy_group.add(self.enemy)

            if self.enemy.rect[1] > 100:
                self.enemy_group.remove(self.enemy)
                print("saiu da tela")


            if self.player_points > 200:
                self.enemy.speed  = 2
                self.level = 1
                self.level_text = self.font.render("LEVEL: "+ str(self.level),1,(255,255,255))
            if self.player_points > 500:
                self.enemy.speed  = 10
                self.level = "FINAL"
                self.level_text = self.font.render("LEVEL: "+ str(self.level),1,(255,255,255))


            for bullet in self.shoot_group:
                self.shoot_group.draw(self.window)
                if self.player_shot.rect[1]< -20: 
                    self.shoot_group.remove(self.player_shot)


            if (pygame.sprite.groupcollide(self.shoot_group, self.enemy_group, True, True)):
                self.player_points += random.randint(1,10)
                self.points_text = self.font.render("SCORE: " + str(self.player_points), 1, (255,255,255))
                pygame.mixer.Channel(2).play(pygame.mixer.Sound("sounds/borboletinha.wav")) 


            if (pygame.sprite.groupcollide(self.player_group, self.enemy_group, True, False)):
                    Game()
                    self.game_init = False

            pygame.display.update()
Game()