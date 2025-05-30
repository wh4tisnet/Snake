import pygame
import random
import sys

pygame.init()
pygame.font.init() 

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // GRID_SIZE

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

class Snake:
    def __init__(self):
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = (1, 0)
        self.grow = False
    
    def move(self):
        head_x, head_y = self.positions[0]
        dir_x, dir_y = self.direction
        new_head = (head_x + dir_x, head_y + dir_y)

        if new_head in self.positions or new_head[0] < 0 or new_head[0] >= GRID_WIDTH or new_head[1] < 0 or new_head[1] >= GRID_HEIGHT:
            return False

        self.positions.insert(0, new_head)
        if not self.grow:
            self.positions.pop()
        else:
            self.grow = False
        return True
    
    def change_direction(self, direction):
        if (direction[0] * -1, direction[1] * -1) != self.direction:
            self.direction = direction
    
    def grow_snake(self):
        self.grow = True
    
    def draw(self, screen):
        for position in self.positions:
            rect = pygame.Rect(position[0] * GRID_SIZE, position[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(screen, GREEN, rect)
            pygame.draw.rect(screen, BLACK, rect, 1)

class Food:
    def __init__(self):
        self.position = self.randomize_position()
    
    def randomize_position(self):
        while True:
            new_position = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
            if new_position not in game.snake.positions:
                return new_position
    
    def draw(self, screen):
        rect = pygame.Rect(self.position[0] * GRID_SIZE, self.position[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(screen, RED, rect)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Snake Game")
        self.clock = pygame.time.Clock()
        self.snake = Snake()
        self.food = Food()
        self.score = 0
        self.font = pygame.font.Font(None, 36)
        self.game_over = False
    
    def reset_game(self):
        self.__init__()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if self.game_over and event.key == pygame.K_SPACE:
                    self.reset_game()
                elif event.key == pygame.K_UP:
                    self.snake.change_direction((0, -1))
                elif event.key == pygame.K_DOWN:
                    self.snake.change_direction((0, 1))
                elif event.key == pygame.K_LEFT:
                    self.snake.change_direction((-1, 0))
                elif event.key == pygame.K_RIGHT:
                    self.snake.change_direction((1, 0))
        return True
    
    def update(self):
        if not self.game_over:
            if not self.snake.move():
                self.game_over = True
                return
            
            if self.snake.positions[0] == self.food.position:
                self.snake.grow_snake()
                self.score += 10
                self.food.position = self.food.randomize_position()
    
    def draw(self):
        self.screen.fill(BLACK)
        
        if not self.game_over:
            self.snake.draw(self.screen)
            self.food.draw(self.screen)
        
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        
        if self.game_over:
            game_over_text = self.font.render("GAME OVER!", True, WHITE)
            restart_text = self.font.render("Press SPACE to restart", True, WHITE)
            
            go_rect = game_over_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 - 20))
            restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 20))
            
            self.screen.blit(game_over_text, go_rect)
            self.screen.blit(restart_text, restart_rect)
        
        pygame.display.flip()
    
    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(10)
        
        pygame.quit()
        sys.exit()

print("=== SNAKE GAME ===")
print("Controls:")
print("- Use arrow keys to move")
print("- Eat red food to grow and score points")
print("- Don't hit walls or yourself!")
print("- Press SPACE to restart when game over")
print("\nStarting game...")

if __name__ == "__main__":
    game = Game()
    game.run()
