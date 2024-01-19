import pygame
import time
import threading
import random

WIDTH, HEIGHT = 600, 480
GRID_SIZE = 20
SNAKE_SIZE = 20

GRAY = (255, 255, 255)
RED = (255, 0, 0)
WHITE = (150, 150, 150)
BLACK = (0,0,0)

class SnakeGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Snake Game")
        self.clock = pygame.time.Clock()
        self.running = True
        self.snake = [(100, 100), (80, 100), (60, 100)]
        self.direction = "RIGHT"
        self.food = self.spawn_food()
        self.score = 0

        self.wall_thread = threading.Thread(target=self.check_wall)

        self.self_thread = threading.Thread(target=self.check_self)
        self.handle_game_thread = threading.Thread(target=self.handle_game)

    def spawn_food(self):
        while True:
            food = (random.randrange(1,(WIDTH//GRID_SIZE))* GRID_SIZE,random.randrange(1,(HEIGHT//GRID_SIZE))* GRID_SIZE)
            if food not in self.snake:
                return food

    def draw_snake(self):
        pygame.draw.rect(self.screen,GRAY,(self.snake[0][0],self.snake[0][1],SNAKE_SIZE,SNAKE_SIZE),border_radius=5)

        for part in self.snake[1:]:
            pygame.draw.rect(self.screen,WHITE,(part[0],part[1],SNAKE_SIZE,SNAKE_SIZE),border_radius=5)

        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))

    def draw_food(self):
        pygame.draw.rect(self.screen,RED,(self.food[0],self.food[1],SNAKE_SIZE,SNAKE_SIZE),border_radius=50)

    def move_snake(self):
        head = list(self.snake[0])

        if self.direction == "RIGHT":
            head[0] += GRID_SIZE
        elif self.direction == "LEFT":
            head[0] -= GRID_SIZE
        elif self.direction == "UP":
            head[1] -= GRID_SIZE
        elif self.direction == "DOWN":
            head[1] += GRID_SIZE

        self.snake.insert(0,tuple(head))

        if self.snake[0]== self.food:
            self.food= self.spawn_food()
            self.score += 1
        else:
            self.snake.pop()

    def check_wall(self):
        while self.running:
            head_x, head_y = self.snake[0]
            if head_x < 0 or head_x >= WIDTH or head_y < 0 or head_y >= HEIGHT:
                self.running = False
            time.sleep(0.1)


    def check_self(self):
        while self.running:
            if self.snake[0] in self.snake[1:]:
                self.running = False
            time.sleep(0.1)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and self.direction != "DOWN":
                    self.direction = "UP"
                elif event.key == pygame.K_DOWN and self.direction != "UP":
                    self.direction = "DOWN"
                elif event.key == pygame.K_LEFT and self.direction != "RIGHT":
                    self.direction = "LEFT"
                elif event.key == pygame.K_RIGHT and self.direction != "LEFT":
                    self.direction = "RIGHT"
                    
    def handle_game(self):
        while self.running:
            self.handle_events()
            self.move_snake()
            self.screen.fill(BLACK)
            self.draw_snake()
            self.draw_food()
            pygame.display.flip()
            self.clock.tick(15)

    def run(self):
        self.wall_thread.start()
        self.self_thread.start()
        self.handle_game_thread.start()

        
        self.wall_thread.join()
        self.self_thread.join()
        self.handle_game_thread.join()


        pygame.quit()


if __name__ == "__main__":
    game = SnakeGame()
    game.run()