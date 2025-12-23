import pygame
import random
from typing import List, Tuple

# --- Константы ---
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
GRID_SIZE = 20

GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

BOARD_BACKGROUND_COLOR = (0, 0, 0)
SNAKE_COLOR = (0, 255, 0)
APPLE_COLOR = (255, 0, 0)

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

DIRECTIONS = [UP, DOWN, LEFT, RIGHT]


class GameObject:
    """Базовый класс игровых объектов."""

    def __init__(self, position: Tuple[int, int]):
        """Инициализирует объект."""
        self.position = position
        self.body_color = None

    def draw(self, screen: pygame.Surface):
        """Отрисовывает объект на экране."""
        pass


class Apple(GameObject):
    """Класс яблока."""

    def __init__(self):
        """Создаёт яблоко со случайной позицией."""
        self.body_color = APPLE_COLOR
        self.position = (0, 0)
        self.randomize_position()

    def randomize_position(self):
        """Задаёт случайную позицию яблока."""
        self.position = (
            random.randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        )

    def draw(self, screen: pygame.Surface):
        """Отрисовывает яблоко."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)


class Snake(GameObject):
    """Класс змейки."""

    def __init__(self):
        """Инициализирует змейку."""
        center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.length = 1
        self.positions: List[Tuple[int, int]] = [center]
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = SNAKE_COLOR
        self.last = None

    def get_head_position(self) -> Tuple[int, int]:
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def update_direction(self):
        """Обновляет направление движения."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Перемещает змейку."""
        head_x, head_y = self.get_head_position()
        dx, dy = self.direction

        new_head = (
            (head_x + dx * GRID_SIZE) % SCREEN_WIDTH,
            (head_y + dy * GRID_SIZE) % SCREEN_HEIGHT
        )

        if new_head in self.positions[2:]:
            self.reset()
            return

        self.positions.insert(0, new_head)

        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None

    def reset(self):
        """Сбрасывает змейку в начальное состояние."""
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = random.choice(DIRECTIONS)
        self.next_direction = None
        self.last = None

    def draw(self, screen: pygame.Surface):
        """Отрисовывает змейку."""
        for position in self.positions:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)

        if self.last:
            rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, rect)


def handle_keys(snake: Snake):
    """Обрабатывает нажатия клавиш."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake.direction != DOWN:
                snake.next_direction = UP
            elif event.key == pygame.K_DOWN and snake.direction != UP:
                snake.next_direction = DOWN
            elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                snake.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                snake.next_direction = RIGHT


def main():
    """Основной игровой цикл."""
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Изгиб Питона")
    clock = pygame.time.Clock()

    snake = Snake()
    apple = Apple()

    screen.fill(BOARD_BACKGROUND_COLOR)

    while True:
        clock.tick(20)
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()

        snake.draw(screen)
        apple.draw(screen)
        pygame.display.update()


if __name__ == "__main__":
    main()
