import pygame
import sys
import random

# Initialize the game and set the window
pygame.init()
width = 1280
height = 720
screen = pygame.display.set_mode((width, height))

# Define colors and other variables
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLOCK_SIZE = 25
SPEED = 10
DIRECTIONS = {
    pygame.K_UP: (0, -1),
    pygame.K_DOWN: (0, 1),
    pygame.K_LEFT: (-1, 0),
    pygame.K_RIGHT: (1, 0)
}


# Create the snake with methods
class Snake:
    def __init__(self):
        self.length = 1
        self.segments = [pygame.Rect(width / 2, height / 2, BLOCK_SIZE, BLOCK_SIZE)]
        self.direction = random.choice(list(DIRECTIONS.values()))

    def move(self):
        dx, dy = self.direction
        head = pygame.Rect(self.segments[0].x + dx * BLOCK_SIZE, self.segments[0].y + dy * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
        
        # Check for boundary collision
        if head.left < 0 or head.right > width or head.top < 0 or head.bottom > height:
            game_over()
        
        self.segments.insert(0, head)
        if len(self.segments) > self.length:
            self.segments.pop()

    def change_direction(self, key):
        new_direction = DIRECTIONS.get(key)
        if new_direction and (new_direction[0] != -self.direction[0] or new_direction[1] != -self.direction[1]):
            self.direction = new_direction

    def draw(self, surface):
        for segment in self.segments:
            pygame.draw.rect(surface, BLUE, segment)


# Create the fruit and methods
class Fruit:
    def __init__(self):
        self.rect = pygame.Rect(0, 0, BLOCK_SIZE, BLOCK_SIZE)
        self.color = RED
        self.randomize_position()

    def randomize_position(self):
        x = random.randint(0, (width - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        y = random.randint(0, (height - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        self.rect.topleft = (x, y)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)


# Game over function
def game_over():
    pygame.quit()
    sys.exit()


# Main game logic and loop
def main():
    clock = pygame.time.Clock()
    snake = Snake()
    fruit = Fruit()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over()
            elif event.type == pygame.KEYDOWN:
                snake.change_direction(event.key)

        snake.move()

        # Check for collision with fruit
        if snake.segments[0].colliderect(fruit.rect):
            snake.length += 1
            fruit.randomize_position()

        screen.fill(BLACK)  # Clear the screen

        snake.draw(screen)
        fruit.draw(screen)

        pygame.display.update()
        clock.tick(SPEED)


if __name__ == "__main__":
    main()
