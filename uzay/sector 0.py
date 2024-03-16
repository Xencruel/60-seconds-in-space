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
        if current_time - self.last_shot_time > self.shoot_delay:
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

def draw_start_screen():
    screen.fill(BLACK)
    start_text = font.render("Başlamak için tıklayın", True, WHITE)
    start_text_rect = start_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(start_text, start_text_rect)

def draw_game_over_screen():
    screen.fill(BLACK)
    game_over_text = font.render("Oyun Bitti", True, WHITE)
    game_over_text_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    screen.blit(game_over_text, game_over_text_rect)
    score_text = font.render("Skor: {}".format(player.score), True, WHITE)
    score_text_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(score_text, score_text_rect)
    restart_text = font.render("Yeniden Başlatmak için ENTER tuşuna basın", True, WHITE)
    restart_text_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
    screen.blit(restart_text, restart_text_rect)

def reset_game():
    player.lives = 3
    player.score = 0
    player.rect.centerx = WIDTH // 2
    player.rect.bottom = HEIGHT - 10
    all_sprites.empty()
    bullets.empty()
    aliens.empty()
    all_sprites.add(player)
    for _ in range(8):
        alien = Alien()
        all_sprites.add(alien)
        aliens.add(alien)
    game_over = False

# Oyun başlatma
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Uzay Savaşı")
clock = pygame.time.Clock()

# Başlangıç ekranı ve başlangıç buttonu
start_platform = pygame.Surface((200, 50))
start_platform.fill(WHITE)
start_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 25, 200, 50)

# Oyun durumu
game_over = False
game_started = False

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
            if event.key == pygame.K_RETURN and game_over:
                reset_game()
                game_over = False

    if game_started:
        # Oyuncu hareketleri
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.speed_x = -5
        elif keys[pygame.K_RIGHT]:
            player.speed_x = 5
        else:
            player.speed_x = 0
        if keys[pygame.K_UP]:
            player.speed_y = -5
        elif keys[pygame.K_DOWN]:
            player.speed_y = 5
        else:
            player.speed_y = 0

        # Mermi atma
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            player.shoot()

        # Sprite güncelleme
        all_sprites.update()

        # Uzay gemisi ve uzaylı çarpışması
        hits = pygame.sprite.spritecollide(player, aliens, True)
        for hit in hits:
            player.lives -= 1
            if player.lives == 0:
                game_over = True
            else:
                alien = Alien()
                all_sprites.add(alien)
                aliens.add(alien)

        # Mermi ve uzaylı çarpışması
        hits = pygame.sprite.groupcollide(aliens, bullets, True, True)
        for hit in hits:
            player.score += 1
            alien = Alien()
            all_sprites.add(alien)
            aliens.add(alien)

        # Oyun ekranı temizleme
        screen.fill(BLACK)

        # Sprite'ları çizme
        all_sprites.draw(screen)

        # Can sayısını ve skoru gösterme
        lives_text = font.render("Can: {}".format(player.lives), True, WHITE)
        score_text = font.render("Skor: {}".format(player.score), True, WHITE)
        screen.blit(lives_text, (10, 10))
        screen.blit(score_text, (WIDTH - score_text.get_width() - 10, 10))

        # Oyun sonu kontrolü
        if game_over:
            draw_game_over_screen()

    else:
        draw_start_screen()

    # Ekranı güncelleme
    pygame.display.flip()

    # FPS ayarlama
    clock.tick(60)
    

pygame.quit()
