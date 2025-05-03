import pygame

# Ініціалізація
pygame.init()
WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Input Field in Pygame")

# Кольори
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)

# Шрифт
font = pygame.font.Font(None, 36)

# Поле для введення
input_text = ""  # Введений текст
input_rect = pygame.Rect(300, 250, 200, 40)  # Прямокутник для вводу
active = False  # Чи активне поле

running = True
while running:
    screen.fill(WHITE)

    # Малюємо поле для вводу
    color = RED if active else GRAY
    pygame.draw.rect(screen, color, input_rect, 2)
    
    # Відображаємо введений текст
    text_surface = font.render(input_text, True, BLACK)
    screen.blit(text_surface, (input_rect.x + 10, input_rect.y + 10))

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Клік у поле вводу → активуємо його
            if input_rect.collidepoint(event.pos):
                active = True 
            else:
                active = False
        
        elif event.type == pygame.KEYDOWN and active:
            if event.key == pygame.K_RETURN:
                print("Введене число:", input_text)  # Використовуй число тут
                input_text = ""  # Очищення після вводу
            
            elif event.key == pygame.K_BACKSPACE:
                input_text = input_text[:-1]  # Видалення останнього символу
            
            elif event.unicode.isdigit():  # Дозволяємо вводити тільки цифри
                input_text += event.unicode

pygame.quit()