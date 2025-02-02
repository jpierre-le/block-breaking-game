import pygame
import sys
import math
import random

# Pygameの初期化
pygame.init()
pygame.mixer.init()  # 音声機能の初期化

# 画面サイズとFPS設定
WIDTH, HEIGHT = 800, 600
FPS = 60

# 色の定義
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY  = (200, 200, 200)
RED   = (255, 0, 0)
BLUE  = (0, 0, 255)

# 定数設定
BALL_SPEED = 5.66  # ボールの一定速度

# Paddleの設定
PADDLE_WIDTH  = 100
PADDLE_HEIGHT = 15
PADDLE_SPEED  = 7

# Ballの設定
BALL_RADIUS = 10

# ブロックレイアウトの設定（全体で12個のブロック）
BLOCK_ROWS    = 3   # 行数
BLOCK_COLS    = 8   # 列数（3 x 4 = 12個）
BLOCK_WIDTH   = 80
BLOCK_HEIGHT  = 20
BLOCK_PADDING = 10
BLOCK_OFFSET_TOP  = 50
BLOCK_OFFSET_LEFT = 35

# 得点設定
POINTS_PER_BLOCK = 10

# サウンドファイルの読み込み（ファイル名をmp3に変更）
try:
    collision_sound = pygame.mixer.Sound("hit.mp3")
except (pygame.error, FileNotFoundError):
    collision_sound = None
    print("衝突音ファイル 'hit.mp3' が見つかりません。")

try:
    celebratory_sound = pygame.mixer.Sound("fanfare.mp3")
except (pygame.error, FileNotFoundError):
    celebratory_sound = None
    print("ファンファーレ音声ファイル 'fanfare.mp3' が見つかりません。")

def circle_rect_collision(cx, cy, radius, rect):
    """
    円（中心(cx, cy)と半径）と矩形(pygame.Rectオブジェクト)の衝突判定
    """
    closest_x = max(rect.left, min(cx, rect.right))
    closest_y = max(rect.top,  min(cy, rect.bottom))
    distance_x = cx - closest_x
    distance_y = cy - closest_y
    return (distance_x ** 2 + distance_y ** 2) < (radius ** 2)

def create_blocks():
    """
    ブロックのグリッドを作成し、pygame.Rectオブジェクトのリストとして返す
    （全体で12個）
    """
    blocks = []
    for row in range(BLOCK_ROWS):
        for col in range(BLOCK_COLS):
            x = BLOCK_OFFSET_LEFT + col * (BLOCK_WIDTH + BLOCK_PADDING)
            y = BLOCK_OFFSET_TOP + row * (BLOCK_HEIGHT + BLOCK_PADDING)
            block = pygame.Rect(x, y, BLOCK_WIDTH, BLOCK_HEIGHT)
            blocks.append(block)
    return blocks

def reset_game():
    """
    新しいラウンドのためにゲーム状態をリセットする
    """
    paddle = pygame.Rect((WIDTH - PADDLE_WIDTH) // 2, HEIGHT - 50, PADDLE_WIDTH, PADDLE_HEIGHT)
    ball = {
        'x': WIDTH / 2,
        'y': HEIGHT / 2,
        'vx': 4,
        'vy': -4
    }
    blocks = create_blocks()
    normalize_velocity(ball)
    score = 0
    return paddle, ball, blocks, score

def normalize_velocity(ball):
    """
    ballの速度ベクトルの大きさを常にBALL_SPEEDに調整する
    """
    speed = math.sqrt(ball['vx'] ** 2 + ball['vy'] ** 2)
    if speed != 0:
        ball['vx'] = ball['vx'] / speed * BALL_SPEED
        ball['vy'] = ball['vy'] / speed * BALL_SPEED

def show_confetti(screen, duration_ms=3000):
    """
    ゲームクリア時に紙吹雪アニメーションを表示する関数
    """
    confetti = []
    num_particles = 100
    colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255),
              (255, 255, 0), (255, 0, 255), (0, 255, 255)]
    # ランダムな紙吹雪パーティクルを生成
    for _ in range(num_particles):
        particle = {
            'x': random.randint(0, WIDTH),
            'y': random.randint(-50, 0),
            'vx': random.uniform(-3, 3),
            'vy': random.uniform(2, 5),
            'color': random.choice(colors),
            'size': random.randint(2, 5)
        }
        confetti.append(particle)
    
    start_time = pygame.time.get_ticks()
    clock = pygame.time.Clock()
    while pygame.time.get_ticks() - start_time < duration_ms:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        # 紙吹雪パーティクルの更新
        for particle in confetti:
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            if particle['y'] > HEIGHT:
                particle['y'] = random.randint(-50, 0)
                particle['x'] = random.randint(0, WIDTH)
        
        screen.fill(BLACK)
        for particle in confetti:
            pygame.draw.rect(screen, particle['color'],
                             (int(particle['x']), int(particle['y']), particle['size'], particle['size']))
        pygame.display.flip()

def draw_start_screen(screen, font):
    """
    スタート画面を描画する関数。中央に「Start」ボタンを表示する。
    """
    screen.fill(BLACK)
    title_text = font.render("Block Breaking Game", True, WHITE)
    title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))
    screen.blit(title_text, title_rect)
    
    # ボタンの設定
    button_width, button_height = 200, 60
    button_rect = pygame.Rect(0, 0, button_width, button_height)
    button_rect.center = (WIDTH // 2, HEIGHT // 2)
    
    # ボタンの描画
    pygame.draw.rect(screen, BLUE, button_rect)
    button_text = font.render("Start", True, WHITE)
    button_text_rect = button_text.get_rect(center=button_rect.center)
    screen.blit(button_text, button_text_rect)
    
    pygame.display.flip()
    return button_rect

def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("ブロック崩し")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 48)
    small_font = pygame.font.SysFont(None, 32)

    game_started = False
    # 初期状態の変数（ゲーム開始前は未設定）
    paddle, ball, blocks, score = None, None, None, 0

    while True:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if not game_started and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                # スタート画面のボタンがクリックされたか確認
                if start_button.collidepoint(mouse_pos):
                    # ゲーム開始
                    game_started = True
                    paddle, ball, blocks, score = reset_game()

        # スタート画面の表示（ゲーム未開始の場合）
        if not game_started:
            start_button = draw_start_screen(screen, font)
            continue

        # --- パドル操作 ---
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            paddle.x -= PADDLE_SPEED
        if keys[pygame.K_RIGHT]:
            paddle.x += PADDLE_SPEED
        if paddle.left < 0:
            paddle.left = 0
        if paddle.right > WIDTH:
            paddle.right = WIDTH

        # --- ボールの更新（速度一定） ---
        ball['x'] += ball['vx']
        ball['y'] += ball['vy']

        # --- 画面端での衝突処理 ---
        if ball['x'] - BALL_RADIUS < 0:
            ball['x'] = BALL_RADIUS
            ball['vx'] = -ball['vx']
            if collision_sound:
                collision_sound.play()
        if ball['x'] + BALL_RADIUS > WIDTH:
            ball['x'] = WIDTH - BALL_RADIUS
            ball['vx'] = -ball['vx']
            if collision_sound:
                collision_sound.play()
        if ball['y'] - BALL_RADIUS < 0:
            ball['y'] = BALL_RADIUS
            ball['vy'] = -ball['vy']
            if collision_sound:
                collision_sound.play()

        # --- パドルとの衝突 ---
        if circle_rect_collision(ball['x'], ball['y'], BALL_RADIUS, paddle):
            ball['y'] = paddle.top - BALL_RADIUS
            ball['vy'] = -abs(ball['vy'])
            if collision_sound:
                collision_sound.play()
            offset = (ball['x'] - paddle.centerx) / (PADDLE_WIDTH / 2)
            ball['vx'] += offset * 2

        # --- ブロックとの衝突 ---
        for block in blocks[:]:
            if circle_rect_collision(ball['x'], ball['y'], BALL_RADIUS, block):
                blocks.remove(block)
                ball['vy'] = -ball['vy']
                if collision_sound:
                    collision_sound.play()
                score += POINTS_PER_BLOCK
                break

        # --- ボールの速度を一定に保つ ---
        normalize_velocity(ball)

        # --- ゲームクリア条件 ---
        if not blocks:
            clear_text = font.render("Game Clear!", True, RED)
            screen.fill(BLACK)
            screen.blit(clear_text, ((WIDTH - clear_text.get_width()) // 2,
                                     (HEIGHT - clear_text.get_height()) // 2))
            pygame.display.flip()
            if celebratory_sound:
                celebratory_sound.play()
            show_confetti(screen, 3000)  # 3秒間紙吹雪を表示
            game_started = False  # ゲーム終了後、スタート画面に戻る
            continue

        # --- ゲームオーバー条件 ---
        if ball['y'] - BALL_RADIUS > HEIGHT:
            game_over_text = font.render("Game Over!", True, RED)
            screen.fill(BLACK)
            screen.blit(game_over_text, ((WIDTH - game_over_text.get_width()) // 2,
                                         (HEIGHT - game_over_text.get_height()) // 2))
            pygame.display.flip()
            pygame.time.wait(2000)
            game_started = False  # ゲーム終了後、スタート画面に戻る
            continue

        # --- 描画 ---
        screen.fill(BLACK)
        pygame.draw.rect(screen, BLUE, paddle)
        pygame.draw.circle(screen, WHITE, (int(ball['x']), int(ball['y'])), BALL_RADIUS)
        for block in blocks:
            pygame.draw.rect(screen, GRAY, block)
        score_text = small_font.render(f"Score: {score}", True, WHITE)
        score_rect = score_text.get_rect(topright=(WIDTH - 10, 10))
        screen.blit(score_text, score_rect)

        pygame.display.flip()

if __name__ == "__main__":
    main()
