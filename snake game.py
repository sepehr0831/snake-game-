from ast import keyword
from asyncio import events
from cProfile import run
import imp
from logging import exception
from multiprocessing import Event
import re
from turtle import pu
import pygame
from pygame.locals import *
import time
import random


class Apple ():
    def __init__(self,parent_screen) -> None:
        self.parent_screen = parent_screen
        self.image = pygame.image.load("apple.jpg").convert()
        self.x = size*3                           
        self.y = size*3
    def draw(self):
        self.parent_screen.blit(self.image,(self.x,self.y))
        pygame.display.flip()
    def move(self):
        self.x = random.randint(0,24)* size
        self.y = random.randint(0,19)* size
        

size = 40
class Snake():
    def __init__(self,parent_screen,length) -> None: 
        self.length = length
        self.parent_screen = parent_screen
        self.block = pygame.image.load("block.jpg").convert()
        self.x =[size]* length
        self.y =[size]* length
        self.direction = "right"

    def increase_length(self):
        self.length+= 1 
        self.x.append(-1)
        self.y.append(-1)

    
    def move_up(self):
        self.direction ="up"
    def move_down(self):
        self.direction = "down"
    def move_left(self):
       self.direction = "left"
    def move_right(self):
        self.direction ="right"

    

    def walk(self):

        for i in range(self.length-1, 0, -1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]




        if self.direction == 'left':
            self.x[0] -= size
        if self.direction == 'right':
            self.x[0] += size
        if self.direction == 'up':
            self.y[0] -= size
        if self.direction == 'down':
            self.y[0] += size

        self.draw()

    
    def draw(self):
        for i in range(self.length):
            self.parent_screen.blit(self.block,(self.x[i],self.y[i]))
        pygame.display.flip()




class Game:
    def __init__(self):
        pygame.init()
        self.play_background()
        self.surface = pygame.display.set_mode((1000, 800))
        self.snake = Snake(self.surface,1)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()
        pygame.mixer.init()

    def is_collision(self,x1,y1,x2,y2):
        if x1 >= x2 and x1 < x2 + size :
            if y1 >= y2 and y1 < y2 + size:
                return True
        return False


    def play_background(self):
        pygame.mixer.music.load("bg_music_1.mp3")
        pygame.mixer.music.play()



    def play_sound(self,sound):
        sound =  pygame.mixer.Sound(f"1_snake_game_resources_{sound}.mp3")
        pygame.mixer.Sound.play(sound)

    def play(self):
        self.render_bg()
        self.snake.walk()
        self.apple.draw()
        self.score_display()
        pygame.display.flip()
        if self.is_collision(self.snake.x[0],self.snake.y[0],self.apple.x,self.apple.y):
            self.snake.increase_length()
            self.apple.move()
            self.play_sound("ding")

        for i in range(3,self.snake.length):
            if self.is_collision(self.snake.x[0],self.snake.y[0],self.snake.x[i],self.snake.y[i]):
                self.play_sound("crash")
                raise "game over"


    def score_display(self):
        font = pygame.font.SysFont("arial", 30)
        score= font.render(f"score = {self.snake.length}", True, (250,250,250))
        self.surface.blit(score ,(850,10))

    def render_bg(self):
        bg = pygame.image.load("background.jpg")
        self.surface.blit(bg,(0,0))


    
    def show_game_over(self):
        self.render_bg()
        font = pygame.font.SysFont("arial",30)
        line1 = font.render(f"your game is over . your score is {self.snake.length}", True, (250,250,250))
        self.surface.blit(line1,(200,300))
        line2 = font.render("for exit press ESCAPE and for paly again press ENTER", True , (250,250,250))
        self.surface.blit(line2,(200,400))
        pygame.display.flip()
        pygame.mixer.music.pause()

    def reset(self):
        self.snake = Snake(self.surface,1)
        self.apple = Apple(self.surface)
        


    def run(self):
        running = True
        pause = False

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    
                    
                    if event.key == K_RETURN:
                        pygame.mixer.music.unpause()
                        pause = False

                    if not pause :
                        if event.key == K_LEFT:
                            self.snake.move_left()

                        if event.key == K_RIGHT:
                            self.snake.move_right()

                        if event.key == K_UP:
                            self.snake.move_up()

                        if event.key == K_DOWN:
                            self.snake.move_down()

                    elif event.type == QUIT:
                        running = False
            try:
                if  pause == False:
                    self.play()
            except:
                self.show_game_over()
                pause = True
                self.reset()

            time.sleep(.2)
        








if __name__ == "__main__":
    game = Game()
    game.run()


    
        

    