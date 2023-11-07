import pygame
from pygame import mixer
import sys
import random

pygame.init()

# MUSIC
mixer.music.load("snakecharmer.mp3")
mixer.music.play(-1)                                                    # -1 permet de jouer la musique en boucle
pygame.mixer.music.set_volume(0.3)                                      # gère le volume du son

class Block:
    def __init__(self, x_pos, y_pos):
        self.x = x_pos
        self.y = y_pos


class Food:
    def __init__(self):
        x = random.randint(0, NB_COL-1)
        y = random.randint(0, NB_ROW-1)
        self.block = Block(x, y)

    def draw_food(self):
        rect = pygame.Rect(self.block.x * CELL_SIZE, self.block.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, (26, 148, 19), rect)


class Snake:
    def __init__(self):
        self.body = [Block(2, 6), Block(3, 6), Block(4, 6)]
        self.direction = "RIGHT"

    def draw_snake(self):
        for block in self.body:
            x_coord = block.x * CELL_SIZE
            y_coord = block.y * CELL_SIZE
            block_rect = pygame.Rect(x_coord, y_coord, CELL_SIZE, CELL_SIZE )
            pygame.draw.rect(screen, (143, 21, 46), block_rect)

    def move_snake(self):
        snake_block_count = len(self.body)
        old_head = self.body[snake_block_count - 1]

        if self.direction == "RIGHT":
            new_head = Block(old_head.x + 1, old_head.y)

        elif self.direction == "LEFT":
            new_head = Block(old_head.x - 1, old_head.y)

        elif self.direction == "TOP":
            new_head = Block(old_head.x, old_head.y - 1)

        else:
            new_head = Block(old_head.x, old_head.y + 1)

        self.body.append(new_head)

    def reset_snake(self):
        self.body = [Block(2, 6), Block(3, 6), Block(4, 6)]
        self.direction = "RIGHT"



class Game:
    def __init__(self):
        self.snake = Snake()
        self.food = Food()
        self.generate_food()

    def update(self):
        self.snake.move_snake()
        self.check_head_on_food()
        self.game_over()

    def draw_game_element(self):
        self.food.draw_food()
        self.snake.draw_snake()

    def check_head_on_food(self):
        snake_length = len(self.snake.body)
        snake_head_block = self.snake.body[snake_length - 1]
        food_block = self.food.block
        if snake_head_block.x == food_block.x and snake_head_block.y == food_block.y:
            self.generate_food()
        else:
            self.snake.body.pop(0)

    def generate_food(self):
        should_generate_food = True
        while should_generate_food:
            count = 0
            for block in self.snake.body:
                if block.x == self.food.block.x and block.y == self.food.block.y:
                    count += 1
                    foodSfx = mixer.Sound("apple_bite.ogg")
                    foodSfx.play()
                    foodSfx.set_volume(0.6)
            if count == 0:
                should_generate_food = False
            else:
                self.food = Food()

    def game_over(self):
        snake_length = len(self.snake.body)
        snake_head_block = self.snake.body[snake_length - 1]
        if (snake_head_block.x not in range(0, NB_COL)) or (snake_head_block.y not in range(0, NB_ROW)):
            self.snake.reset_snake()
            gOverSfx = mixer.Sound("GameOver.ogg")
            gOverSfx.play()
            gOverSfx.set_volume(0.3)
        for block in self.snake.body[0:snake_length - 1]:
            if block.x == snake_head_block.x and block.y == snake_head_block.y:
                self.snake.reset_snake()
                gOverSfx = mixer.Sound("GameOver.ogg")
                gOverSfx.play()
                gOverSfx.set_volume(0.3)



NB_COL = 10                                 # Nom des Variables en majuscule pr indiquer que c des constantes et qu'elles ne seront pas modifier
NB_ROW = 15
CELL_SIZE = 40

screen = pygame.display.set_mode(size=(NB_COL * CELL_SIZE, NB_ROW * CELL_SIZE))

pygame.display.set_caption("Snake")
windowIcon = pygame.image.load("voadi-snake-cyan-portrait.png")
pygame.display.set_icon(windowIcon)

timer = pygame.time.Clock()


game_on = True
game = Game()

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 400)                                                       # Event déclenché tt les 200 millisecondes


def show_grid():
    for i in range(0, NB_COL):
        for j in range(0, NB_ROW):
            rect = pygame.Rect(i * CELL_SIZE, j * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, (pygame.Color("black")), rect, width=1)                      # widht=0 ça sera tt noir, widht>0 ça créer une bordure, widht<0 on ne voit plus le noir


while game_on:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == SCREEN_UPDATE:
            game.update()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if game.snake.direction != "DOWN":
                    game.snake.direction = "TOP"
            if event.key == pygame.K_DOWN:
                if game.snake.direction != "UP":
                    game.snake.direction = "DOWN"
            if event.key == pygame.K_RIGHT:
                if game.snake.direction != "LEFT":
                    game.snake.direction = "RIGHT"
            if event.key == pygame.K_LEFT:
                if game.snake.direction != "RIGHT":
                    game.snake.direction = "LEFT"

    screen.fill(pygame.Color(227, 224,220))
    #show_grid()
    game.draw_game_element()
    pygame.display.update()
    timer.tick(60)

