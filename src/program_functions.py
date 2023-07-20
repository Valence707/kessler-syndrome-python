import pygame, random, pygame_widgets
from data import *
from entities import *
from pygame_widgets.button import Button

def create_all_widgets():
    start_wi = gvrs['start_screen_widgets']
    game_wi = gvrs['game_widgets']
    settings_wi = gvrs['settings_widgets']

    start_wi += [

        # Start Button
        Button(
        gvrs['display'],
        100,
        100,
        150,
        50,
        inactiveColour=(150, 0, 0),
        pressedColour=(100, 0, 0),
        hoverColour=(200, 0, 0),
        text='START',
        onClick=lambda: transition_state('game', start_wi, game_wi),
        ),

        # Settings Button
        Button(
        gvrs['display'],
        100,
        200,
        150,
        50,
        inactiveColour=(150, 0, 0),
        pressedColour=(100, 0, 0),
        hoverColour=(200, 0, 0),
        text='SETTINGS',
        onClick=lambda: set_game_state('settings')
        ),

        # Acknowledgments Button
        Button(
        gvrs['display'],
        100,
        300,
        150,
        50,
        inactiveColour=(150, 0, 0),
        pressedColour=(100, 0, 0),
        hoverColour=(200, 0, 0),
        text='ACKNOWLEDGMENTS',
        onClick=lambda: set_game_state('acknowledgments')
        ),
    ]

    game_wi += [
        
    ]

    settings_wi += [

    ]

# Change all required states to fit new game state.
def transition_state(dest, to_hide, to_show):
    for widget in to_hide:
        print(to_hide)
        widget.hide()

    for widget in to_show:
        widget.show()

    set_game_state(dest)

# Show start screen widgets.
def show_start_screen():
    for widget in gvrs['start_screen_widgets']:
        widget.show()

# Hide start screen widgets
def hide_start_screen():
    for widget in gvrs['start_screen_widgets']:
        widget.hide()

# Operations to be carried out in the start screen.
def start_screen(f_dat, dest_surf):
    pass

# Set the game state to 'new_state'.
def set_game_state(new_state):
    gvrs['game_state'] = new_state

# Return the current game state.
def get_game_state():
    return gvrs['game_state']

# Handle all game operations.
def game(f_dat):

    # Handle pausing the game
    if f_dat['keys'][pygame.K_ESCAPE] and not gvrs['last_paused']:
        set_game_state('paused' if not get_game_state() == 'paused' else 'game')
        gvrs['last_paused'] = True
    elif f_dat['keys'][pygame.K_ESCAPE] and gvrs['last_paused']:
        gvrs['last_paused'] = True
    else:
        gvrs['last_paused'] = False

    # Handle keyboard input.
    if f_dat['keys'][pygame.K_1]:
        gvrs['player'].weaponSelect = 0
    elif f_dat['keys'][pygame.K_2]:
        gvrs['player'].weaponSelect = 1
    elif f_dat['keys'][pygame.K_3]:
        gvrs['player'].weaponSelect = 2
    elif f_dat['keys'][pygame.K_4]:
        gvrs['player'].weaponSelect = 3
    elif f_dat['keys'][pygame.K_5]:
        gvrs['player'].weaponSelect = 4

    if f_dat['keys'][pygame.K_o]:
        gvrs['asteroids'].add(Asteroid())
    # Handle player shooting weapons.
    playerWeapon = gvrs['player'].weapons[gvrs['player'].weaponSelect]
    if f_dat['mouse_pressed'][0]:
        if playerWeapon[4]:
            if f_dat['current_time'] - playerWeapon[5] > playerWeapon[2]:
                playerWeapon[3](gvrs['player'].rect.center, f_dat['mouse_pos'])
                playerWeapon[5] = f_dat['current_time']
            
        else:
            if not gvrs['player'].hasShot and f_dat['current_time'] - playerWeapon[5] > playerWeapon[2]:
                playerWeapon[3](gvrs['player'].rect.center, f_dat['mouse_pos'])
                playerWeapon[5] = f_dat['current_time']
                gvrs['player'].hasShot = True

    else:
        gvrs['player'].hasShot = False

    # Add asteroids according to waves.
    if gvrs['waves'][gvrs['current_wave']]['numAsteroids'] > 0 and gvrs['wave_timer'] > gvrs['waves'][gvrs['current_wave']]['spawnRate']:
        
        gvrs['asteroids'].add(Asteroid(pos=[-95, -95], type="satellite" if random.randrange(0, 100) > 90 else "normal", velocity=[(random.uniform(0.25, 0.75))*6, (random.uniform(0.25, 0.75))*6]))
        gvrs['wave_timer'] = 0
        gvrs['waves'][gvrs['current_wave']]['numAsteroids'] -= 1
    
    if gvrs['waves'][gvrs['current_wave']]['numAsteroids'] == 0 and len(gvrs['asteroids']) == 0:
        gvrs['current_wave'] += 1
        gvrs['player'].weapons[0][1] += 200
        gvrs['player'].weapons[0][1] += 15
        gvrs['player'].weapons[0][1] += 5
        gvrs['player'].weapons[0][1] += 200
        gvrs['player'].weapons[0][1] += 3
    else:
        gvrs['wave_timer'] += 1

    # Update all entities.
    gvrs['particles'].update()
    gvrs['bullets'].update()
    gvrs['asteroids'].update()
    gvrs['player'].update(f_dat['keys'], f_dat['mouse_pos'])

    # Handle player death.
    if gvrs['player'].health < 1:
        set_game_state('gameOver')
        gvrs['current_wave'] = 0
        gvrs['player'] = Player()
        for asteroid in gvrs['asteroids']:
            asteroid.kill()
            del asteroid

        for bullet in gvrs['bullets']:
            bullet.kill()
            del bullet

        for particle in gvrs['particles']:
            particle.kill()
            del particle

    # Draw everything
    draw_everything(gvrs['display'])

# Operations to be carried out in the settings menu.
def settings_menu(f_dat, dest_surf):
    dest_surf.blit(sprites['background'], (0, 0))
    for particle in gvrs['particles']:
        particle.draw()

    for bullet in gvrs['bullets']:
        bullet.draw()

    gvrs['player'].draw()
    for asteroid in gvrs['asteroids']:
        asteroid.draw()
    
    if f_dat['keys'][pygame.K_ESCAPE] and not gvrs['last_paused']:
        set_game_state('paused' if not get_game_state() == 'paused' else 'game')
        gvrs['last_paused'] = True
    elif f_dat['keys'][pygame.K_ESCAPE] and gvrs['last_paused']:
        gvrs['last_paused'] = True
    else:
        gvrs['last_paused'] = False

# Operations to be carried out in the "game over" screen.
def game_over_menu(f_dat, dest_surf):
    dest_surf.blit(sprites['background'], (0, 0))

# Draw all sprites.
def draw_everything(dest_surf):
    dest_surf.blit(sprites['background'], (0, 0))
    for particle in gvrs['particles']:
        particle.draw()

    for bullet in gvrs['bullets']:
        bullet.draw()

    gvrs['player'].draw()
    for asteroid in gvrs['asteroids']:
        asteroid.draw()

    if gvrs['clock'].get_fps() < 40:
        for particle in gvrs['particles']:
            particle.kill()
            del particle

# Debug state operations.
def testing_mode(f_data):
    pass

# Load a png sprite with a colorkey
def load_sprite(name, c_key, custom_c_key=False):
    sprites[name] = pygame.image.load(f'./res/images/{name}.png').convert(),
    if c_key:
        sprites[name].set_colorkey(custom_c_key if custom_c_key else (0, 0, 0))

# Unload the sprite.
def unload_sprite(name):
    del sprites[name]

# Change the volume of all sounds.