import pygame
import numpy as np

# Налаштування гри
WIDTH, HEIGHT = 900, 600
ROWS, COLS = 100, 100  # Розмір сітки
CELL_SIZE = WIDTH // COLS  # Розмір однієї клітинки

# Кольори
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRID_COLOR = (200, 200, 200)
BLUE= (0, 0, 255)

# Ініціалізація
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game of Life")
clock = pygame.time.Clock()

# Створення пустого поля
grid = np.zeros((ROWS, COLS), dtype=int)
running = False  # Чи йде симуляція
random_start = False  # Чи заповнювати поле випадково
time=5
font = pygame.font.Font(None, 36)
text = font.render(f"{time//5}", True, (255, 0, 0)) #швидкість гри
text_rect = text.get_rect(center=(890,590)) #росташування

# pause_image=pygame.image.load("Pause.png")
pause_image=pygame.image.load("play_button.png")
pygame.transform.scale(pause_image,(1,1))

#правила
SURVIVAL_RULES = {2,3}  # {2,3} При яких сусідах клітина виживає
BIRTH_RULES = {3}  #{3} При яких сусідах народжується нова клітина

def draw_grid():
    """Малює сітку та клітинки."""
    screen.fill(WHITE)
    
    for row in range(ROWS):
        for col in range(COLS):
            rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if grid[row, col] == 1:
                pygame.draw.rect(screen, BLACK, rect)
            if grid[row, col] == 2:
                pygame.draw.rect(screen, BLUE, rect)
            pygame.draw.rect(screen, GRID_COLOR, rect, 1)

def get_cell_from_mouse(pos):
    """Отримує індекси клітинки, по якій клікнули."""
    x, y = pos
    col = x // CELL_SIZE
    row = y // CELL_SIZE
    return row, col

def count_neighbors(grid, row, col):
    """Підраховує кількість живих сусідів клітини."""
    neighbors = 0
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue  # Пропустити саму клітину
            r, c = row + dr, col + dc
            if 0 <= r < ROWS and 0 <= c < COLS and grid[r, c] == 1:
                neighbors += 1
    return neighbors

def update_grid():
    """Оновлює поле згідно з правилами гри."""
    global grid
    new_grid = grid.copy()
    
    for row in range(ROWS):
        for col in range(COLS):
            neighbors = count_neighbors(grid, row, col)
            
            if grid[row, col] == 1 and neighbors not in SURVIVAL_RULES:
                new_grid[row, col] = 0  # Смерть від перенаселення або самотності
            elif grid[row, col] == 0 and neighbors in BIRTH_RULES:
                new_grid[row, col] = 1  # Народження клітинки

    grid = new_grid

# Головний цикл
running_simulation = True
while running_simulation:
    draw_grid()
    screen.blit(text, text_rect)
    screen.blit(pause_image,(100,100))
    pygame.display.flip()  # Відображення тексту
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running_simulation = False
        
        elif event.type == pygame.MOUSEBUTTONDOWN:# Перемикання клітинки
            if event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                row, col = get_cell_from_mouse(mouse_pos)
            
                if 0 <= row < ROWS and 0 <= col < COLS:
                    if grid[row, col] == 0:
                        grid[row, col] = 1  # Біле → Чорне
                    elif grid[row, col] == 1:
                        grid[row, col] = 0  # Чорне → Біле
                    elif grid[row, col] == 2:
                        grid[row, col] = 1  # Синє → Біле
                    draw_grid()
                    pygame.display.flip()

            elif event.button == 3:
                mouse_pos = pygame.mouse.get_pos()
                row, col = get_cell_from_mouse(mouse_pos)
            
                if 0 <= row < ROWS and 0 <= col < COLS:
                    if grid[row, col] == 0:
                        grid[row, col] = 2  # Біле → Синє
                    elif grid[row, col] == 2:
                        grid[row, col] = 0  # Синє → Біле
                    elif grid[row, col] == 1:
                        grid[row, col] = 2  # Чорне → Синє
                    draw_grid()
                    pygame.display.flip()
            

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                running = not running  # Запуск/зупинка симуляції
            elif event.key == pygame.K_r:
                grid = np.random.choice([0, 1], size=(ROWS, COLS))  # Рандомне поле
            elif event.key == pygame.K_e:
                grid = np.zeros((ROWS, COLS), dtype=int)  # Очистити поле
            elif event.key == pygame.K_w and time!=40:
                time*=2
                text = font.render(f"{time//5}", True, (255, 0, 0))
            elif event.key == pygame.K_s and time!= 5:
                time//=2
                text = font.render(f"{time//5}", True, (255, 0, 0))
            elif event.key == pygame.K_1: #звичайний режим
                SURVIVAL_RULES = {2,3}
                BIRTH_RULES = {3}
            elif event.key == pygame.K_2: #візерунок
                SURVIVAL_RULES = {0,1,2,3,4,5,6,7,8}
                BIRTH_RULES = {1}
            elif event.key == pygame.K_3: #візерунок
                SURVIVAL_RULES = {1,2,3,4}
                BIRTH_RULES = {1,2}
            elif event.key == pygame.K_4: #візерунок
                SURVIVAL_RULES = {1,2,3,4}
                BIRTH_RULES = {1,2,3}
            elif event.key == pygame.K_5: #генерація печер
                SURVIVAL_RULES = {5,6,7,8}
                BIRTH_RULES = {4,5,6,7,8}
                grid = np.random.choice([0, 1], size=(ROWS, COLS))

    if running:
        update_grid()
        clock.tick(time)
pygame.quit()