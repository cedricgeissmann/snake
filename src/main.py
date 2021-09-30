#! /usr/bin/env python
import pygame
import sys

from random import randint

## Globals:
BLOCK_SIZE = 20
GRID_SIZE = 60
FPS = 10

class Registry():
    snakes = []
    foods = []

    @classmethod
    def get_snakes(cls):
        return cls.snakes

    @classmethod
    def add_snake(cls, snake):
        cls.snakes.append(snake)

    @classmethod
    def add_food(cls, food):
        cls.foods.append(food)

    @classmethod
    def get_foods(cls):
        return cls.foods


class Food():
    pos_x = 0
    pos_y = 0
    grow = 1
    def new(self):
        self.pos_x = randint(0, GRID_SIZE - 2)
        self.pos_y = randint(0, GRID_SIZE - 2)
        self.grow = randint(1, 3)


    def get_pos(self):
        return (self.pos_x, self.pos_y)

    def draw(self, surface):
        color = (0, 255, 0)
        pygame.draw.rect(surface, color, (self.pos_x * BLOCK_SIZE, self.pos_y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

class Snake():
    def __init__(self, ai=True, color=(255, 0, 0), num=1):
        self.pos_x = randint(1, GRID_SIZE - 10)
        self.pos_y = randint(1, GRID_SIZE - 2)
        self.positions = [self.get_head()]
        self.dir = 0
        self.ai = ai
        self.color = color
        self.num = num
        self.growing = 3

    def next_dir(self):
        food = Registry.get_foods()[0]
        (food_x, food_y) = food.get_pos()
        field = [[abs(x-food_x) + abs(y-food_y) for y in range(GRID_SIZE)] for x in range(GRID_SIZE)]
        for snake in Registry.get_snakes():
            for (x, y) in snake.positions:
                field[x][y] += 1000

        if self.dir % 2 == 0:
            update_dir = 1 if self.dir == 0 else - 1
            try:
                heur = field[self.pos_x + update_dir][self.pos_y]
            except(IndexError):
                heur = 10000
            heur_top = field[self.pos_x][self.pos_y - 1]
            heur_bot = field[self.pos_x][self.pos_y + 1]
            if heur_top < heur or heur_bot < heur:
                self.dir = 1 if heur_top < heur_bot else 3
        else:
            update_dir = 1 if self.dir == 3 else - 1
            try:
                heur = field[self.pos_x][self.pos_y + update_dir]
            except(IndexError):
                heur = 10000
            heur_left = field[self.pos_x - 1][self.pos_y]
            heur_right = field[self.pos_x + 1][self.pos_y]
            if heur_left < heur or heur_right < heur:
                self.dir = 2 if heur_left < heur_right else 0

        if self.pos_x == 0 and self.dir == 2:
            self.dir = 3
        elif self.pos_x == GRID_SIZE - 1 and self.dir == 0:
            self.dir = 1
        elif self.pos_y == 0 and self.dir == 1:
            self.dir = 2
        elif self.pos_y == GRID_SIZE - 1 and self.dir == 3:
            self.dir = 0

    def get_head(self):
        return (self.pos_x, self.pos_y)

    def update(self, surface):
        if self.ai:
            self.next_dir()

        if self.dir == 0:
            self.pos_x += 1
        elif self.dir == 1:
            self.pos_y -= 1
        elif self.dir == 2:
            self.pos_x -= 1
        elif self.dir == 3:
            self.pos_y += 1

        self.positions.append(self.get_head())
        if self.growing <= 0:
            (x, y) = self.positions.pop(0)
            pygame.draw.rect(surface, (0, 0, 0), (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
        else:
            self.growing -= 1

        for (x, y) in self.positions:
            pygame.draw.rect(surface, self.color, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

    def change_dir(self, direction):
        if (self.dir + direction) % 2 == 1:
            self.dir = direction

    def check(self):
        (head_x, head_y) = self.get_head()
        if head_x > GRID_SIZE or head_y > GRID_SIZE or head_x < 0 or head_y < 0:
            player_lost(self.num)
        for snake in Registry.get_snakes():
            for (x, y) in snake.positions[:-1]:
                if (x == head_x and y == head_y):
                    player_lost(self.num)

        for food in Registry.get_foods():
            if head_x == food.pos_x and head_y == food.pos_y:
                self.growing = food.grow
                food.new()


def player_lost(num):
    print(f"Spieler {num} hat verloren!")
    pygame.quit()
    sys.exit()



def handle_keypress(key):
    snakes = Registry.get_snakes()
    if key == pygame.K_ESCAPE:
        pygame.quit()
        sys.exit()
    elif key == pygame.K_RIGHT:
        snakes[0].change_dir(0)
    elif key == pygame.K_UP:
        snakes[0].change_dir(1)
    elif key == pygame.K_LEFT:
        snakes[0].change_dir(2)
    elif key == pygame.K_DOWN:
        snakes[0].change_dir(3)

    elif key == pygame.K_d:
        snakes[1].change_dir(0)
    elif key == pygame.K_w:
        snakes[1].change_dir(1)
    elif key == pygame.K_a:
        snakes[1].change_dir(2)
    elif key == pygame.K_s:
        snakes[1].change_dir(3)


def main():
    pygame.init()

    ## Initialization
    running = True

    window = pygame.display.set_mode((GRID_SIZE * BLOCK_SIZE, GRID_SIZE * BLOCK_SIZE))
    pygame.display.set_caption("Snake")
    window.fill(0)

    clock = pygame.time.Clock()

    ## Initialize game objects (snake)
    snake = Snake(ai=False, num=1)
    Registry.add_snake(snake)
    Registry.add_snake(Snake(ai=True, color=(0,0,255), num=2))
    food = Food()
    Registry.add_food(food)
    food.new()


    ## Game loop
    while running:
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                handle_keypress(event.key)
        for x in range(GRID_SIZE):
            for y in range(GRID_SIZE):
                color = (0, 0, 0) if (x + y) % 2 == 0 else (32, 32, 32)
                pygame.draw.rect(window, color, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

        for snake in Registry.get_snakes():
            snake.update(window)
        for food in Registry.get_foods():
            food.draw(window)

        for snake in Registry.get_snakes():
            snake.check()
        clock.tick(FPS)



if __name__ == "__main__":
    main()
