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
BLACK = (0, 0, 0)
RED = (255, 0, 0)

input_rect1 = pygame.Rect(695, 555, 200, 40)
active1 = False

input_rect2 = pygame.Rect(695, 490, 200, 40)
active2 = False

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
text_font = pygame.font.Font(None, 24)
font = pygame.font.Font(None, 36)
text = text_font.render(f"Швидкість гри: {time//5}", True, BLACK) #швидкість гри
text_rect = text.get_rect(center=(800,460)) #росташування

pause="Pause.png"

pause_image=pygame.image.load(pause)
pause_image=pygame.transform.scale(pause_image,(100,80))
input_text1 = ""
input_text2 = ""
text1="Виживання клітини"
text2="Народження клітинки"

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
    screen.blit(pause_image,(-20,530))
    color1 = RED if active1 else BLACK
    color2 = RED if active2 else BLACK

    pygame.draw.rect(screen, color1, input_rect1, 2)
    pygame.draw.rect(screen, color2, input_rect2, 2)

    text_surface1 = font.render(input_text1, True, BLACK)
    screen.blit(text_surface1, (input_rect1.x + 10, input_rect1.y + 10))

    text_surface2 = font.render(input_text2, True, BLACK)
    screen.blit(text_surface2, (input_rect2.x + 10, input_rect2.y + 10))

    text_1 = text_font.render(text1, True, BLACK)
    screen.blit(text_1, (715, 535))
    text_2 = text_font.render(text2, True, BLACK)
    screen.blit(text_2, (705, 470))
    pygame.display.flip()  # Відображення тексту
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running_simulation = False
        
        elif event.type == pygame.MOUSEBUTTONDOWN:# Перемикання клітинки
            if input_rect1.collidepoint(event.pos):
                active1 = True
                active2 = False
            elif input_rect2.collidepoint(event.pos):
                active2 = True
                active1 = False
            else:
                active1 = False
                active2 = False
            
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
                if pause=="Pause.png":
                    pause="play.png"
                elif pause=="play.png":
                    pause="Pause.png"
                pause_image=pygame.image.load(pause)
                pause_image=pygame.transform.scale(pause_image,(100,80))
            elif event.key == pygame.K_r:
                grid = np.random.choice([0, 1], size=(ROWS, COLS))  # Рандомне поле
            elif event.key == pygame.K_e:
                grid = np.zeros((ROWS, COLS), dtype=int)  # Очистити поле
            elif event.key == pygame.K_w and time!=40:
                time*=2
                text = text_font.render(f"Швидкість гри: {time//5}", True, BLACK)
            elif event.key == pygame.K_s and time!= 5:
                time//=2
                text = text_font.render(f"Швидкість гри: {time//5}", True, BLACK)
        
            elif active1:
                if event.key == pygame.K_RETURN:
                    BIRTH_RULES = set(int(x) for x in input_text1.split(",") if x.strip().isdigit())
                    input_text1 = ""
                elif event.key == pygame.K_BACKSPACE:
                    input_text1 = input_text1[:-1]
                elif event.unicode.isprintable():
                    input_text1 += event.unicode

            elif active2:
                if event.key == pygame.K_RETURN:
                    SURVIVAL_RULES = set(int(x) for x in input_text2.split(",") if x.strip().isdigit())
                    input_text2 = ""
                elif event.key == pygame.K_BACKSPACE:
                    input_text2 = input_text2[:-1]
                elif event.unicode.isprintable():
                    input_text2 += event.unicode

    if running:
        update_grid()
        clock.tick(time)
pygame.quit()
#pyinstaller --onefile --noconsole game_of_life.py