import pygame
import pygame_gui
import sys
from pygame.math import Vector2
import random


class SNAKE:
    def __init__(self):
        self.body = [Vector2(7, 18), Vector2(6, 18), Vector2(5, 18)]
        self.direction = Vector2(1, 0)
        self.new_block = False

        # head_graphics
        re_head_up = pygame.image.load(
            'Graphics/head_up.png').convert_alpha()
        self.head_up = pygame.transform.scale(
            re_head_up, (cell_size, cell_size))

        re_head_down = pygame.image.load(
            'Graphics/head_down.png').convert_alpha()
        self.head_down = pygame.transform.scale(
            re_head_down, (cell_size, cell_size))

        re_head_left = pygame.image.load(
            'Graphics/head_left.png').convert_alpha()
        self.head_left = pygame.transform.scale(
            re_head_left, (cell_size, cell_size))

        re_head_right = pygame.image.load(
            'Graphics/head_right.png').convert_alpha()
        self.head_right = pygame.transform.scale(
            re_head_right, (cell_size, cell_size))

        # tail_graphics
        re_tail_right = pygame.image.load(
            'Graphics/tail_right.png').convert_alpha()
        self.tail_right = pygame.transform.scale(
            re_tail_right, (cell_size, cell_size))

        re_tail_left = pygame.image.load(
            'Graphics/tail_left.png').convert_alpha()
        self.tail_left = pygame.transform.scale(
            re_tail_left, (cell_size, cell_size))

        re_tail_up = pygame.image.load(
            'Graphics/tail_up.png').convert_alpha()
        self.tail_up = pygame.transform.scale(
            re_tail_up, (cell_size, cell_size))

        re_tail_down = pygame.image.load(
            'Graphics/tail_down.png').convert_alpha()
        self.tail_down = pygame.transform.scale(
            re_tail_down, (cell_size, cell_size))

        # body_turn & back left, right:
        re_body_tl = pygame.image.load(
            'Graphics/body_tl.png').convert_alpha()
        self.body_tl = pygame.transform.scale(
            re_body_tl, (cell_size, cell_size))

        re_body_tr = pygame.image.load(
            'Graphics/body_tr.png').convert_alpha()
        self.body_tr = pygame.transform.scale(
            re_body_tr, (cell_size, cell_size))

        re_body_bl = pygame.image.load(
            'Graphics/body_bl.png').convert_alpha()
        self.body_bl = pygame.transform.scale(
            re_body_bl, (cell_size, cell_size))

        re_body_br = pygame.image.load(
            'Graphics/body_br.png').convert_alpha()
        self.body_br = pygame.transform.scale(
            re_body_br, (cell_size, cell_size))

        # body vertical and body horizontal:
        re_body_vertical = pygame.image.load(
            'Graphics/body_vertical.png').convert_alpha()
        self.body_vertical = pygame.transform.scale(
            re_body_vertical, (cell_size, cell_size))

        re_body_horizontal = pygame.image.load(
            'Graphics/body_horizontal.png').convert_alpha()
        self.body_horizontal = pygame.transform.scale(
            re_body_horizontal, (cell_size, cell_size))

        self.crunch_sound = pygame.mixer.Sound('Sound/crunch.wav')

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

    def play_crunch_sound(self):
        self.crunch_sound.play()

    def reset(self):
        self.body = [Vector2(7, 18), Vector2(6, 18), Vector2(5, 18)]
        self.direction = Vector2(0, 0)


class FRUIT:
    def __init__(self):
        self.randomize()
        # re_apple = pygame.image.load('Graphics/apple.png').convert_alpha()
        # pygame.transform.scale(re_apple, (cell_size, cell_size))
        self.apple = apple

    def draw_fruit(self):
        fruit_rect = pygame.Rect(
            (int(self.pos.x*cell_size), int(self.pos.y*cell_size), cell_size, cell_size))
        screen.blit(self.apple, fruit_rect)
        # pygame.draw.rect(screen, (100, 200, 100), fruit_rect)

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
        self.draw_grass()
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.draw_score()

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.add_block()
            self.snake.play_crunch_sound()
        for block in self.snake.body[1:]:
            if block == self.fruit.pos:
                self.fruit.randomize()

    def check_fail(self):
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()

        if not 0 <= self.snake.body[0].y < cell_number or not 0 <= self.snake.body[0].x < cell_number:
            self.game_over()

    def game_over(self):
        self.snake.reset()
        # pygame.quit()
        # sys.exit()

    def draw_grass(self):
        grass_color = (201, 228, 214)
        for row in range(cell_number):
            if row % 2 == 0:
                for col in range(cell_number):
                    if col % 2 == 0:
                        grass_rect = pygame.Rect(
                            col*cell_size, row*cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)
            else:
                for col in range(cell_number):
                    if col % 2 != 0:
                        grass_rect = pygame.Rect(
                            col*cell_size, row*cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)

    def draw_score(self):
        score_text = str((len(self.snake.body)-3))
        score_surface = game_font.render(score_text, True, (0, 0, 0))
        score_x = int(cell_number*cell_size - 40)
        score_y = int(cell_number*cell_size - 30)
        score_rect = score_surface.get_rect(center=(score_x, score_y))

        apple_rect = apple.get_rect(
            midright=(score_rect.left, score_rect.centery))

        bg_rect = pygame.Rect(apple_rect.left, apple_rect.top,
                              apple_rect.width + score_rect.width + 5, apple_rect.height)
        # pygame.draw.rect(screen, (130, 115, 176), bg_rect)
        screen.blit(score_surface, score_rect)
        screen.blit(apple, apple_rect)
        pygame.draw.rect(screen, (0, 0, 0), bg_rect, 2)


pygame.init()
cell_size = 30
cell_number = 20
score_size = 20
game_font = pygame.font.Font('Font/PoetsenOne-Regular.ttf', score_size)

pygame.display.set_caption("Snake Game by L_My")
screen = pygame.display.set_mode(
    (cell_number*cell_size, cell_number*cell_size))

re_apple = pygame.image.load('Graphics/apple.png').convert_alpha()
apple = pygame.transform.scale(re_apple, (cell_size, cell_size))

manager = pygame_gui.UIManager((cell_number*cell_size, cell_number*cell_size))
clock = pygame.time.Clock()

main_game = MAIN()

SCREEN_UPDATE = pygame.USEREVENT
# pygame.time.set_timer(SCREEN_UPDATE, 120)

hello_rect = pygame.Rect(cell_number*cell_size/2,
                         cell_number*cell_size/2, cell_size*3, cell_size)
hello_button = pygame_gui.elements.UIButton(
    relative_rect=hello_rect, text='Say Hello', manager=manager)


is_running = True
while is_running:
    time_delta = clock.tick(40)/1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
        elif event.type == SCREEN_UPDATE:
            print("thien", event.user_type)
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == hello_button:
                    print('Hello World!')
            # main_game.update()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if main_game.snake.direction.y != 1:
                    main_game.snake.direction = Vector2(0, -1)
            elif event.key == pygame.K_DOWN:
                if main_game.snake.direction.y != -1:
                    main_game.snake.direction = Vector2(0, 1)
            elif event.key == pygame.K_LEFT:
                if main_game.snake.direction.x != 1:
                    main_game.snake.direction = Vector2(-1, 0)
            elif event.key == pygame.K_RIGHT:
                if main_game.snake.direction.x != -1:
                    main_game.snake.direction = Vector2(1, 0)
        main_game.check_collision()
        manager.process_events(event)
    manager.update(time_delta)
    screen.fill((102, 208, 185))
    main_game.draw_elements()
    manager.draw_ui(screen)
    pygame.display.update()
