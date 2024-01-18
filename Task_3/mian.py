import pygame
import sys
import random

class SnakeGame:
    def __init__(self):
        pygame.init()

        # Initialize game window and properties
        self.width = 400
        self.height = 400
        self.grid_size = 20
        self.window = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Snake Game')

        # Initialize clock for controlling the game's frame rate
        self.clock = pygame.time.Clock()

        # Create snake, food, and score variables
        self.snake = Snake(self)
        self.food = Food(self)
        self.score = 0
        self.game_over = False

    def run_game(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if self.game_over:
                        if event.key == pygame.K_RETURN:
                            self.reset_game()
                        elif event.key == pygame.K_ESCAPE:
                            pygame.quit()
                            sys.exit()

            if not self.game_over:
                # Handle user input, move snake, and update game state
                self.snake.handle_keys()
                self.snake.move()
                self.check_collision()
                self.update_display()

                self.clock.tick(10)

    def check_collision(self):
        # Check if snake eats the food
        if self.snake.body[0].position == self.food.position:
            self.snake.add_segment()
            self.food.randomize_position()
            self.score += 1

        # Check if the snake collides with itself
        for segment in self.snake.body[1:]:
            if self.snake.body[0].position == segment.position:
                self.game_over = True

        # Check if the snake is out of bounds
        if (
            self.snake.body[0].x < 0
            or self.snake.body[0].x >= self.width
            or self.snake.body[0].y < 0
            or self.snake.body[0].y >= self.height
        ):
            self.game_over = True

    def reset_game(self):
        # Reset game state for a new game
        self.snake = Snake(self)
        self.food = Food(self)
        self.score = 0
        self.game_over = False

    def update_display(self):
        self.window.fill((0, 0, 0))

        # Draw grid lines
        for x in range(0, self.width, self.grid_size):
            pygame.draw.line(self.window, (255, 255, 255), (x, 0), (x, self.height))
        for y in range(0, self.height, self.grid_size):
            pygame.draw.line(self.window, (255, 255, 255), (0, y), (self.width, y))

        # Draw snake, food, and display score
        for segment in self.snake.body:
            pygame.draw.rect(self.window, (255, 255, 255), segment.position + (self.grid_size, self.grid_size))

        pygame.draw.rect(self.window, (255, 0, 0), self.food.position + (self.grid_size, self.grid_size))

        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.window.blit(score_text, (10, 10))

        if self.game_over:
            # Display game over message
            game_over_text = font.render("Game Over!", True, (255, 255, 255))
            text_rect = game_over_text.get_rect(topleft=(self.width // 2.4 - game_over_text.get_width() // 2.4, self.height // 2.4 - game_over_text.get_height() // 2.4))
            self.window.blit(game_over_text, text_rect.topleft)

            game_over_text1 = font.render("Press Enter to Restart", True, (255, 255, 255))
            text_rect1 = game_over_text1.get_rect(center=(self.width // 2, self.height // 2 + game_over_text.get_height() // 2))
            self.window.blit(game_over_text1, text_rect1.topleft)

            game_over_text2 = font.render("Escape to Exit", True, (255, 255, 255))
            text_rect2 = game_over_text2.get_rect(topleft=(self.width // 2.1 - game_over_text2.get_width() // 2.1, self.height // 2.1 + game_over_text.get_height() + game_over_text1.get_height()))
            self.window.blit(game_over_text2, text_rect2.topleft)

        pygame.display.flip()

class Snake:
    def __init__(self, game):
        self.game = game
        self.body = [Segment(100, 100), Segment(90, 100), Segment(80, 100)]
        self.direction = 'RIGHT'

    def handle_keys(self):
        # Handle user input to change snake direction
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP] and self.direction != 'DOWN':
            self.direction = 'UP'
        elif keys[pygame.K_DOWN] and self.direction != 'UP':
            self.direction = 'DOWN'
        elif keys[pygame.K_LEFT] and self.direction != 'RIGHT':
            self.direction = 'LEFT'
        elif keys[pygame.K_RIGHT] and self.direction != 'LEFT':
            self.direction = 'RIGHT'

    def move(self):
        # Move the snake in the current direction
        head = self.body[0]
        new_head = Segment(head.x, head.y)

        if self.direction == 'UP':
            new_head.y -= self.game.grid_size
        elif self.direction == 'DOWN':
            new_head.y += self.game.grid_size
        elif self.direction == 'LEFT':
            new_head.x -= self.game.grid_size
        elif self.direction == 'RIGHT':
            new_head.x += self.game.grid_size

        self.body.insert(0, new_head)
        if len(self.body) > 1:
            self.body.pop()

    def add_segment(self):
        # Add a new segment to the snake when it eats the food
        tail = self.body[-1]
        if self.direction == 'UP':
            self.body.append(Segment(tail.x, tail.y + self.game.grid_size))
        elif self.direction == 'DOWN':
            self.body.append(Segment(tail.x, tail.y - self.game.grid_size))
        elif self.direction == 'LEFT':
            self.body.append(Segment(tail.x + self.game.grid_size, tail.y))
        elif self.direction == 'RIGHT':
            self.body.append(Segment(tail.x - self.game.grid_size, tail.y))

class Segment:
    def __init__(self, x, y):
        # Represents a segment of the snake's body
        self.x = x
        self.y = y

    @property
    def position(self):
        # Return the position of the segment
        return self.x, self.y

class Food:
    def __init__(self, game):
        # Represents the food that the snake can eat
        self.game = game
        self.position = (
            random.randrange(0, game.width, game.grid_size),
            random.randrange(0, game.height, game.grid_size),
        )

    def randomize_position(self):
        # Randomly reposition the food when eaten by the snake
        self.position = (
            random.randrange(0, self.game.width, self.game.grid_size),
            random.randrange(0, self.game.height, self.game.grid_size),
        )

if __name__ == "__main__":
    game = SnakeGame()
    game.run_game()
