#! /usr/bin/env python
import pygame
import sys

from random import randint

## Globals:
BLOCK_SIZE = 10
GRID_SIZE = 30
FPS = 10

class Registry():
    snakes = []
    food = None

    @classmethod
    def get_snakes(cls):
        return cls.snakes

    @classmethod
    def add_snake(cls, snake):
        cls.snakes.append(snake)

    @classmethod
    def add_food(cls, food):
        cls.food = food

    @classmethod
    def get_food(cls):
        if cls.food == None:
            cls.food = Food()
        return cls.food


class Food():
    pos_x = 0
    pos_y = 0
    def new(self, surface):
        pygame.draw.rect(surface, (0, 0, 0), (self.pos_x * BLOCK_SIZE, self.pos_y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
        self.pos_x = randint(0, GRID_SIZE - 2)
        self.pos_y = randint(0, GRID_SIZE - 2)
        pygame.draw.rect(surface, (0, 255, 0), (self.pos_x * BLOCK_SIZE, self.pos_y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))


    def get_pos(self):
        return (self.pos_x, self.pos_y)

class Snake():
    def __init__(self, ai=True, color=(255, 0, 0)):
        self.pos_x = randint(1, GRID_SIZE - 2)
        self.pos_y = randint(1, GRID_SIZE - 2)
        self.positions = [self.get_head()]
        self.dir = 0
        self.ai = ai
        self.color = color

    def next_dir(self):
        food = Registry.get_food()
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
        food = Registry.get_food()
        if self.get_head() != food.get_pos():
            (x, y) = self.positions.pop(0)
            pygame.draw.rect(surface, (0, 0, 0), (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
        else:
            food.new(surface)

        for (x, y) in self.positions:
            pygame.draw.rect(surface, self.color, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

    def change_dir(self, direction):
        if (self.dir + direction) % 2 == 1:
            self.dir = direction


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


def main():
    pygame.init()

    ## Initialization
    running = True

    window = pygame.display.set_mode((GRID_SIZE * BLOCK_SIZE, GRID_SIZE * BLOCK_SIZE))
    pygame.display.set_caption("Snake")
    window.fill(0)

    clock = pygame.time.Clock()

    ## Initialize game objects (snake)
    snake = Snake(ai=False)
    Registry.add_snake(snake)
    Registry.add_snake(Snake(color=(0,0,255)))
    food = Food()
    Registry.add_food(food)
    food.new(window)


    ## Game loop
    while running:
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                handle_keypress(event.key)

        for snake in Registry.get_snakes():
            snake.update(window)
        clock.tick(FPS)



if __name__ == "__main__":
    main()
