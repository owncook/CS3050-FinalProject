import arcade
# --- Constants ---

# --- Screen ---
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Galaga Game Window"

# --- Player ---
PLAYER_SCALE = 2
BULLET_SPEED = 5
MAX_BULLETS = 2

# --- Enemies --- 
ENEMY_SCALE = 1.5 # 32*1.5 = 48
ENEMY_SPACING_X = 25  # Horizontal spacing between enemies (previously 40)
ENEMY_SPACING_Y = 50  # Vertical spacing between rows
ENEMY_SPAWN_INTERVAL = 3
ATTACK_INTERVAL = 4
MARGIN_X = 100
MARGIN_Y = 100
ENEMY_OFFSCREEN_MARGIN = 30
ENEMY_SPEED = 5
ENEMY_BULLET_SPEED = 8

# --- Game --- 
SCORE = 10

# --- Stars ---
STAR_COUNT = 100
STAR_SPEED = 2
TWINKLE_SPEED = 0.1

# --- Planets ---
PLANET_SPEED = STAR_SPEED
PLANET_SCALE = 2

# --- Database ---
NUM_HIGHSCORES = 5

# --- Explosions
# How fast the particle will accelerate down. Make 0 if not desired
PARTICLE_GRAVITY = 0.05

# How fast to fade the particle
PARTICLE_FADE_RATE = 8

# How fast the particle moves. Range is from 2.5 <--> 5 with 2.5 and 2.5 set.
PARTICLE_MIN_SPEED = 2.5
PARTICLE_SPEED_RANGE = 2.5

# How many particles per explosion
PARTICLE_COUNT = 20

# How big the particle
PARTICLE_RADIUS = 3

# Possible particle colors
PARTICLE_COLORS = [arcade.color.ALIZARIN_CRIMSON,
                   arcade.color.COQUELICOT,
                   arcade.color.LAVA,
                   arcade.color.KU_CRIMSON,
                   arcade.color.DARK_TANGERINE]

# Chance we'll flip the texture to white and make it 'sparkle'
PARTICLE_SPARKLE_CHANCE = 0.02

# --- Smoke
# Note: Adding smoke trails makes for a lot of sprites and can slow things
# down. If you want a lot, it will be necessary to move processing to GPU
# using transform feedback. If to slow, just get rid of smoke.

# Start scale of smoke, and how fast is scales up
SMOKE_START_SCALE = 0.25
SMOKE_EXPANSION_RATE = 0.03

# Rate smoke fades, and rises
SMOKE_FADE_RATE = 7
SMOKE_RISE_RATE = 0.5

# Chance we leave smoke trail
SMOKE_CHANCE = 0.25



