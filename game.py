import pygame
import random

# Constants
WIDTH, HEIGHT = 600, 400
BLOCK_SIZE = 20
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BORDER_THICKNESS = 2  # Thickness of the red border

class SnakeGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Voice Controlled Snake 🐍")
        self.clock = pygame.time.Clock()
        
        self.font = pygame.font.Font(None, 36)  # Font for displaying score
        self.small_font = pygame.font.Font(None, 24)  # Small font for command
        self.score = 0  # Track the score

        self.snake = [(100, 100)]
        self.direction = "RIGHT"
        self.food = self.spawn_food()
        self.running = True
        self.game_over = False
        self.last_command = "Waiting..."  # Stores last voice command

    def spawn_food(self):
        return (random.randint(0, WIDTH - BLOCK_SIZE) // BLOCK_SIZE * BLOCK_SIZE,
                random.randint(0, HEIGHT - BLOCK_SIZE) // BLOCK_SIZE * BLOCK_SIZE)

    def change_direction(self, new_direction):
        """Change direction only if it's a valid move."""
        new_direction = new_direction.upper()
        if new_direction == "UP" and self.direction != "DOWN":
            self.direction = "UP"
        elif new_direction == "DOWN" and self.direction != "UP":
            self.direction = "DOWN"
        elif new_direction == "LEFT" and self.direction != "RIGHT":
            self.direction = "LEFT"
        elif new_direction == "RIGHT" and self.direction != "LEFT":
            self.direction = "RIGHT"
        
        # Update last command display
        self.last_command = f"Command: {new_direction}"

    def update(self):
        """Update snake position and check collisions."""
        if self.snake[0][0] < BORDER_THICKNESS or self.snake[0][0] >= WIDTH - BORDER_THICKNESS or \
           self.snake[0][1] < BORDER_THICKNESS or self.snake[0][1] >= HEIGHT - BORDER_THICKNESS:
            self.running = False  # Stop the game if the snake hits the wall
        if not self.running:
            return

        x, y = self.snake[0]
        if self.direction == "UP":
            y -= BLOCK_SIZE
        elif self.direction == "DOWN":
            y += BLOCK_SIZE
        elif self.direction == "LEFT":
            x -= BLOCK_SIZE
        elif self.direction == "RIGHT":
            x += BLOCK_SIZE

        self.snake.insert(0, (x, y))

        if self.snake[0] == self.food:
            self.food = self.spawn_food()
            self.score += 10  # Increase score when food is eaten
        else:
            self.snake.pop()

    def render(self):
        """Draw game objects and UI elements."""
        self.screen.fill((0, 0, 0))
        
        # Draw the red border
        pygame.draw.rect(self.screen, RED, (0, 0, WIDTH, HEIGHT), BORDER_THICKNESS)

        # Draw the snake
        for segment in self.snake:
            pygame.draw.rect(self.screen, GREEN, (segment[0], segment[1], BLOCK_SIZE, BLOCK_SIZE))
        
        # Draw the food
        pygame.draw.rect(self.screen, RED, (self.food[0], self.food[1], BLOCK_SIZE, BLOCK_SIZE))
        
        # Render the score
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))  # Position at top-left

        # Render the last voice command at the top-right corner
        command_text = self.small_font.render(self.last_command, True, WHITE)
        self.screen.blit(command_text, (WIDTH - command_text.get_width() - 10, 10))

        pygame.display.flip()

    def quit(self):
        pygame.quit()
