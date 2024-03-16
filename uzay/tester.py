import pygame
import random

# Ekran boyutları
WIDTH = 800
HEIGHT = 800

# Renkler
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Uzay Gemisi sınıfı
class SpaceShip(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("spaceship.png")  # Uzay Gemisi resmi
        self.image = pygame.transform.scale(self.image, (self.image.get_width() // 2, self.image.get_height() // 2))  # Uzay gemisinin boyutunu 1/2 oranında küçült
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 10
        self.speed_y = 0  # Y eksenindeki hareket hızı
        self.speed_x = 0  # X eksenindeki hareket hızı
        self.last_shot_time = pygame.time.get_ticks()  # Son ateş zamanını takip et
        self.shoot_delay = 200  # Ateş etme gecikmesi (ms)
        self.lives = 3  # Can sayısı
        self.score = 0  # Skor

    def update(self):
        self.rect.y += self.speed_y  # Y eksenindeki hareketi güncelle
        self.rect.x += self.speed_x  # X eksenindeki hareketi güncelle
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom > HEIGHT:  # Eğer alt kenara çarparsa
            self.rect.bottom = HEIGHT  # Kenara yapıştır
        if self.rect.top < 0:  # Eğer üst kenara çarparsa
            self.rect.top = 0  # Kenara yapıştır

    def shoot(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time >= self.shoot_delay:
            bullet = Bullet(self.rect.centerx, self.rect.top)
            all_sprites.add(bullet)
            bullets.add(bullet)
            self.last_shot_time = current_time

# Uzaylı sınıfı
class Alien(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("alien.png").convert_alpha()  # Beyaz arka planı kaldır
        self.image = pygame.transform.scale(self.image, (self.image.get_width() // 2, self.image.get_height() // 2))  # Uzaylı pikselini 2 kat küçült
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.speed_y = random.randint(1, 2)

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.y > HEIGHT + 10:
            self.rect.x = random.randint(0, WIDTH - self.rect.width)
            self.rect.y = random.randint(-100, -40)
            self.speed_y = random.randint(1, 2)

# Mermi sınıfı
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 10))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed_y = -10

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.bottom < 0:
            self.kill()

# Oyun başlatma
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Uzay Savaşı")
clock = pygame.time.Clock()

# Başlangıç platformu ve start buttonu
start_platform = pygame.Surface((200, 50))
start_platform.fill(WHITE)
start_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 25, 200, 50)

# Oyun durumu
game_over = False
game_started = True

# Tuş basma durumları
left_pressed = False
right_pressed = False
space_pressed = False

def reset_game():
    all_sprites.empty()
    aliens.empty()
    bullets.empty()

    player.rect.centerx = WIDTH // 2
    player.rect.bottom = HEIGHT - 10
    player.lives = 3
    player.score = 0
    all_sprites.add(player)

    for _ in range(8):
        alien = Alien()
        all_sprites.add(alien)
        aliens.add(alien)

def draw_start_screen():
    # Başlangıç ekranı çizimi
    screen.fill(RED)
    screen.blit(start_platform, (WIDTH // 2 - 100, HEIGHT // 2 - 25))
    pygame.draw.rect(screen, BLACK, start_button)
    start_text = font.render("START", True, WHITE)
    start_text_rect = start_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(start_text, start_text_rect)
    pygame.display.flip()

def draw_game_over_screen():
    # Oyun döngüsünden çıktıktan sonra oyun sonu ekranını çizme
    game_over_text = font.render("GAME OVER", True, WHITE)
    game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    
    screen.fill(BLACK)
    screen.blit(game_over_text, game_over_rect)
    pygame.display.flip()

# Font
font = pygame.font.Font(None, 36)

# Uzay Gemisi oluşturma
player = SpaceShip()

# Sprite grupları
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

aliens = pygame.sprite.Group()
bullets = pygame.sprite.Group()

# Uzaylıları oluşturma
for _ in range(8):
    alien = Alien()
    all_sprites.add(alien)
    aliens.add(alien)

draw_start_screen()

# Oyun döngüsü
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and start_button.collidepoint(event.pos) and not game_started:
                game_started = True
                reset_game()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                left_pressed = True
            elif event.key == pygame.K_RIGHT:
                right_pressed = True
            elif event.key == pygame.K_SPACE:
                space_pressed = True
            elif event.key == pygame.K_UP:
                player.speed_y = -7  # Y ekseninde yukarı doğru hareket et
            elif event.key == pygame.K_DOWN:
                player.speed_y = 7  # Y ekseninde aşağı doğru hareket et
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                left_pressed = False
            elif event.key == pygame.K_RIGHT:
                right_pressed = False
            elif event.key == pygame.K_SPACE:
                space_pressed = False
            elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                player.speed_y = 0  # Y eksenindeki hareketi durdur

    if not game_started:
        draw_start_screen()
        continue

    # Uzay gemisi hareketi
    if left_pressed:
        player.speed_x = -10
    elif right_pressed:
        player.speed_x = 10
    else:
        player.speed_x = 0

    # Ateş etme
    if space_pressed:
        player.shoot()

    # Oyun güncelleme ve çizim
    all_sprites.update()
    bullets.update()
    aliens.update()

    # Uzay gemisi ile uzaylı çarpışması
    hits = pygame.sprite.spritecollide(player, aliens, True)
    if hits:
        player.lives -= len(hits)
        if player.lives <= 0:
            game_over = True

    # Mermi ile uzaylı çarpışması
    for alien in aliens:
        hits = pygame.sprite.spritecollide(alien, bullets, True)
        if hits:
            player.score += 10
            alien.rect.x = random.randint(0, WIDTH - alien.rect.width)
            alien.rect.y = random.randint(-100, -40)
            alien.speed_y = random.randint(1, 2)
        if player.score >= 100 and player.score % 100 == 1:
            player.lives += 1
            
    
            
    

    # Uzaylıların en aşağı inip inmediğini kontrol etme
    for alien in aliens:
        if alien.rect.y >= HEIGHT:
            player.lives -= 1
            aliens.remove(alien)

    # Ekran temizleme ve çizim
    screen.fill(BLACK)
    all_sprites.draw(screen)

    # Skor yazdırma
    score_text = font.render("SCORE: " + str(player.score), True, WHITE)
    screen.blit(score_text, (10, 10))

    # Canları çiz
    lives_text = font.render("Lives: " + str(player.lives), True, WHITE)
    screen.blit(lives_text, (WIDTH - 120, 10))
    if player.lives <= 0:
        game_over = True
    
    


    pygame.display.flip()
    clock.tick(60)

draw_game_over_screen()

# Oyun döngüsünden çıkıldığında tekrar başlatmak için gereken kod
while game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                reset_game()
                game_over = False

    # Başlatma butonunun koordinatları ve boyutları
    restart_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 50, 200, 50)
    
    # Başlatma butonunun çizimi
    pygame.draw.rect(screen, WHITE, restart_button)
    restart_text = font.render("Quit", True, BLACK)
    restart_text_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 75))
    screen.blit(restart_text, restart_text_rect)

    pygame.display.flip()

    # Yeniden başlatma butonuna tıklama kontrolü
    if restart_button.collidepoint(pygame.mouse.get_pos()):
        if pygame.mouse.get_pressed()[0] == 1:
            reset_game()
            game_over = False

pygame.quit()

