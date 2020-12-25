import pygame
import sys
from pygame.math import Vector2
import random


class SNAKE:
    def __init__(self):
        self.body = [Vector2(7, 18), Vector2(6, 18), Vector2(5, 18)]
        self.direction = Vector2(1, 0)
        self.new_block = False

        # head_graphics
        self.head_up = pygame.image.load(
            'Graphics/head_up.png').convert_alpha()
        self.head_down = pygame.image.load(
            'Graphics/head_down.png').convert_alpha()
        self.head_left = pygame.image.load(
            'Graphics/head_left.png').convert_alpha()
        self.head_right = pygame.image.load(
            'Graphics/head_right.png').convert_alpha()
        # tail_graphics
        self.tail_right = pygame.image.load(
            'Graphics/tail_right.png').convert_alpha()
        self.tail_left = pygame.image.load(
            'Graphics/tail_left.png').convert_alpha()
        self.tail_up = pygame.image.load(
            'Graphics/tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load(
            'Graphics/tail_down.png').convert_alpha()

        # body_turn & back left, right:
        self.body_tl = pygame.image.load(
            'Graphics/body_tl.png').convert_alpha()
        self.body_tr = pygame.image.load(
            'Graphics/body_tr.png').convert_alpha()
        self.body_bl = pygame.image.load(
            'Graphics/body_bl.png').convert_alpha()
        self.body_br = pygame.image.load(
            'Graphics/body_br.png').convert_alpha()

        # body vertical and body horizontal:
        self.body_vertical = pygame.image.load(
            'Graphics/body_vertical.png').convert_alpha()
        self.body_horizontal = pygame.image.load(
            'Graphics/body_horizontal.png').convert_alpha()

    def draw_snake(self):
        self.head = self.update_head_graphic()
        self.tail = self.update_tail_graphic()
        self.body_graphic = self.update_body_graphic()
        for index, block in enumerate(self.body):
            if index == 0:
                x_pos = int(block.x*cell_size)
                y_pos = int(block.y*cell_size)
                block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)
                screen.blit(self.head, block_rect)
            elif block == self.body[-1]:
                x_pos = int(block.x*cell_size)
                y_pos = int(block.y*cell_size)
                block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)
                screen.blit(self.tail, block_rect)
            elif index in self.body_graphic:
                x_pos = int(block.x*cell_size)
                y_pos = int(block.y*cell_size)
                block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)
                screen.blit(self.body_graphic[index], block_rect)

    def update_head_graphic(self):
        head_relation = self.body[0] - self.body[1]
        if head_relation == Vector2(1, 0):
            return self.head_right
        if head_relation == Vector2(-1, 0):
            return self.head_left
        if head_relation == Vector2(0, 1):
            return self.head_down
        if head_relation == Vector2(0, -1):
            return self.head_up

    def update_tail_graphic(self):
        tail_relation = self.body[-1] - self.body[-2]
        if tail_relation == Vector2(1, 0):
            return self.tail_right
        if tail_relation == Vector2(-1, 0):
            return self.tail_left
        if tail_relation == Vector2(0, 1):
            return self.tail_down
        if tail_relation == Vector2(0, -1):
            return self.tail_up

    def update_body_graphic(self):
        self.snake_len = len(self.body)
        # print(self.snake_len)

        body_directions_list = []
        for index in range(self.snake_len - 1):
            body_relation = self.body[index] - self.body[index + 1]
            body_directions_list.append(body_relation)
        # print(body_directions_list)

        body_tb_tracing_list = []
        for index in range(len(body_directions_list)-1):
            body_tracing = body_directions_list[index] - \
                body_directions_list[index + 1]
            body_tb_tracing_list.append(body_tracing)
        # print(body_tb_tracing_list)

        self.body_dict = dict()
        for index, body_trace in enumerate(body_tb_tracing_list):
            if body_trace == Vector2(1, -1):
                body_tb_index = index + 1
                self.body_dict[body_tb_index] = self.body_tr
            elif body_trace == Vector2(-1, -1):
                body_tb_index = index + 1
                self.body_dict[body_tb_index] = self.body_tl
            elif body_trace == Vector2(1, 1):
                body_tb_index = index + 1
                self.body_dict[body_tb_index] = self.body_br
            elif body_trace == Vector2(-1, 1):
                body_tb_index = index + 1
                self.body_dict[body_tb_index] = self.body_bl
        # print(self.body_dict.keys())
        for index, body_relation in enumerate(body_directions_list):
            if index in self.body_dict.keys() or index == 0:
                continue
            else:
                if body_relation == Vector2(-1, 0) or body_relation == Vector2(1, 0):
                    self.body_dict[index] = self.body_horizontal
                elif body_relation == Vector2(0, 1) or body_relation == Vector2(0, -1):
                    self.body_dict[index] = self.body_vertical

        return self.body_dict

    def move_snake(self):
        if self.new_block == True:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]

    def add_block(self):
        self.new_block = True


class FRUIT:
    def __init__(self):
        self.randomize()
        self.apple = pygame.image.load('Graphics/apple.png').convert_alpha()
        #apple = pygame.transform.scale(my_food, (cell_size, cell_size))

    def draw_fruit(self):
        fruit_rect = pygame.Rect(
            (int(self.pos.x*cell_size), int(self.pos.y*cell_size), cell_size, cell_size))
        screen.blit(self.apple, fruit_rect)
        #pygame.draw.rect(screen, (100, 200, 100), fruit_rect)

    def randomize(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = pygame.math.Vector2(self.x, self.y)


class MAIN:
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()

    def update(self):
        self.snake.move_snake()
        self.check_fail()

    def draw_elements(self):
        self.fruit.draw_fruit()
        self.snake.draw_snake()

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.add_block()

    def check_fail(self):
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()

        if not 0 <= self.snake.body[0].y < cell_number or not 0 <= self.snake.body[0].x < cell_number:
            self.game_over()

    def game_over(self):
        pygame.quit()
        sys.exit()


pygame.init()
cell_size = 30
cell_number = 20
screen = pygame.display.set_mode(
    (cell_number*cell_size, cell_number*cell_size))
clock = pygame.time.Clock()


main_game = MAIN()

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            main_game.game_over()
        if event.type == SCREEN_UPDATE:
            main_game.update()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if main_game.snake.direction.y != 1:
                    main_game.snake.direction = Vector2(0, -1)
            if event.key == pygame.K_DOWN:
                if main_game.snake.direction.y != -1:
                    main_game.snake.direction = Vector2(0, 1)
            if event.key == pygame.K_LEFT:
                if main_game.snake.direction.x != 1:
                    main_game.snake.direction = Vector2(-1, 0)
            if event.key == pygame.K_RIGHT:
                if main_game.snake.direction.x != -1:
                    main_game.snake.direction = Vector2(1, 0)
        main_game.check_collision()
    screen.fill((150, 250, 150))
    main_game.draw_elements()
    pygame.display.update()
    clock.tick(40)
