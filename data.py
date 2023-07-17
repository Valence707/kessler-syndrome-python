import pygame, os

CONSTS = {
    'WIN_RES': (1200, 800),
    'T_FPS': 60,
}

options = {
    'sound_enabled': True,
    'soundfx_volume': 0.15,
    'music_enabled': True,
    'music_volume': 0.25,
    'particles_enabled': True,
}

gamevars = {
    'american_colors': [(255, 0, 0), (255, 255, 255), (0, 0, 255)],
    'wave_timer': 0,
    'game_state': 'startScreen'
}

# Fonts
fonts = {
    '8bit_48px': pygame.font.Font('res/fonts/8bitOperatorPlus8-Bold.ttf', 48),
    '8bit_24px': pygame.font.Font('res/fonts/8bitOperatorPlus8-Bold.ttf', 24),
    '8bit_20px': pygame.font.Font('res/fonts/8bitOperatorPlus8-Bold.ttf', 20),
    '8bit_16px': pygame.font.Font('res/fonts/8bitOperatorPlus8-Bold.ttf', 16),
    '8bit_regular_12px': pygame.font.Font('res/fonts/8bitOperatorPlusSC-Regular.ttf', 12),
    '8bit_regular_20px': pygame.font.Font('res/fonts/8bitOperatorPlusSC-Regular.ttf', 20),
    '8bit_regular_14px': pygame.font.Font('res/fonts/8bitOperatorPlusSC-Regular.ttf', 14),
    '8bit_regular_16px': pygame.font.Font('res/fonts/8bitOperatorPlusSC-Regular.ttf', 16),
    '8bit_regular_18px': pygame.font.Font('res/fonts/8bitOperatorPlusSC-Regular.ttf', 18),
}

# Sprites and textures
sprites = {
    'asteroids': [pygame.image.load(f'res/images/asteroid_{x+1}.png').convert() for x in range(5)],
    'bullet': pygame.image.load('res/images/bullet.png').convert(),
    'player_ship': pygame.image.load('res/images/ship.png').convert(),
    'background': pygame.image.load('res/images/background.png').convert(),
    'projectile_blaster': pygame.image.load('res/images/projectile_blaster.png').convert(),
    'projectile_shotgun': pygame.image.load('res/images/projectile_shotgun.png').convert(),
    'projectile_machinegun': pygame.image.load('res/images/projectile_machinegun.png').convert(),
    'projectile_photongun': pygame.image.load('res/images/projectile_photongun.png').convert(),
    'projectile_americanpride': pygame.image.load('res/images/projectile_americanpride.png').convert()
}

for x in range(2):
    sprites[F"cursor{x+1}"] = pygame.image.load(f'res/images/cursor{x+1}.png').convert()

# Sounds and music
soundfx = {
    'blaster_shot': pygame.mixer.Sound('res/sounds/shoot.wav'),
    'shotgun_shot': pygame.mixer.Sound('res/sounds/shotgun_shoot.wav'),
    'photon_gun_shot': pygame.mixer.Sound('res/sounds/photon_rifle_shoot.wav'),
    'machine_gun_shot': pygame.mixer.Sound('res/sounds/automatic_cannon.wav'),
    'frag_cannon_shot': pygame.mixer.Sound('res/sounds/frag_cannon.wav'),
    'frag_cannon_burst': pygame.mixer.Sound('res/sounds/frag_explosion.wav'),
}

# Load explosions
for i in range(10):
    soundfx[f'explosion_{i+1}'] = pygame.mixer.Sound(f'res/sounds/explosion_{i+1}.wav')

for i in sprites['asteroids']:
    i.set_colorkey((0, 0, 0))

for key in sprites:
    if not key == 'asteroids' and not key == 'background':
        sprites[key].set_colorkey((0, 0, 0))

# Load music
music = os.listdir(path='res/sounds/music')

# Change music volume
pygame.mixer.music.set_volume(options['music_volume'])

# Change volume of sounds
for sound in soundfx:
    soundfx[sound].set_volume(options['soundfx_volume'])