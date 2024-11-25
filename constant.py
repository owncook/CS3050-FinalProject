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

# --- Trapezoid ---
TRAPEZOID_SPEED = 1 # Need this number to divide evenly into 848 and 152 so the amount of steps taken will be 0 at some point
# if u wanna mess around, 1,2,4, and 8 work


# --- Enemies --- 
"""For jason mode have an if statement and change the sprite width,
but the enemy needs to be 48 px for the spacing to be the same as before"""
ENEMY_SCALE = 1.5
SPRTIE_WIDTH = 32 # Got from the image
ENEMY_WIDTH = ENEMY_SCALE * SPRTIE_WIDTH # Needs to be 48 for trapezoid to look the same
ENEMY_SPACING_X = 25  # Horizontal spacing between enemies
ENEMY_SPACING_Y = 50  # Vertical spacing between rows
ENEMY_SPAWN_INTERVAL = 3
ATTACK_INTERVAL = 4
MARGIN_X = 100
MARGIN_Y = 100
ENEMY_OFFSCREEN_MARGIN = 30
ENEMY_SPEED = 5
ENEMY_BULLET_SPEED = 8
SWOOPING_ENEMY_SPEED = 1

# Constants for Bézier curve calculations
MAX_SWOOP_DURATION = 3  # Maximum time for swoop progression
BEZIER_POWER = 2        # Power for quadratic Bézier curve calculation
BEZIER_T_PARAMETER = 1

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

# --- Explosions ---
# How fast the particle will accelerate down. 
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
# Start scale of smoke, and how fast is scales up
SMOKE_START_SCALE = 0.25
SMOKE_EXPANSION_RATE = 0.03

# Rate smoke fades, and rises
SMOKE_FADE_RATE = 7
SMOKE_RISE_RATE = 0.5

# Chance we leave smoke trail
SMOKE_CHANCE = 0.25



