import pygame, random
from data import *
from entities import *

def start_screen(f_dat, dest_surf):
    dest_surf.blit(sprites['background'], (0, 0))
    if len(gamevars['particles']) < 100:
        gamevars['particles'].add(Particle((random.randrange(0, CONSTS['WIN_RES'][0]-10), random.randrange(0, CONSTS['WIN_RES'][1]-10)), size=[1, 1], color=(200, 200, 200), velocityRange=0.5, duration=random.random()*10))
    gamevars['particles'].update()
    gamevars['particles'].draw(dest_surf)
    dest_surf.blit(sprites['asteroids'][0], (15, 35))
    dest_surf.blit(sprites['asteroids'][1], (235, 65))
    dest_surf.blit(sprites['asteroids'][2], (35, 230))
    dest_surf.blit(sprites['asteroids'][3], (50, 135))
    dest_surf.blit(sprites['asteroids'][4], (145, 600))
    dest_surf.blit(pygame.transform.rotate(sprites['player_ship'], 45), (233, 212))

    # Change opacity of buttons as player hovers over them.
    for button in gamevars['start_screen_overlay'].buttons:
        if button[1].collidepoint(f_dat['mouse_pos'][0], f_dat['mouse_pos'][1]):
            button[0].set_alpha(100)
        else:
            button[0].set_alpha(0)

    gamevars['start_screen_overlay'].draw()

    # Detect and handle button presses.
    if f_dat['mouse_pressed'][0]: 
        if gamevars['start_screen_overlay'].buttons[0][1].collidepoint(f_dat['mouse_pos'][0], f_dat['mouse_pos'][1]):
            gamevars['mouse_image'] = sprites['cursor1']
            gamevars['game_state'] = 'game'

def game(f_dat):
    # Handle pausing the game
    if f_dat['keys'][pygame.K_ESCAPE] and not gamevars['last_paused']:
        gamevars['game_state'] = 'paused' if not gamevars['game_state'] == 'paused' else 'game'
        gamevars['last_paused'] = True
    elif f_dat['keys'][pygame.K_ESCAPE] and gamevars['last_paused']:
        gamevars['last_paused'] = True
    else:
        gamevars['last_paused'] = False

    # Handle keyboard input.
    if f_dat['keys'][pygame.K_1]:
        gamevars['player'].weaponSelect = 0
        gamevars['overlay'].update_text()
    elif f_dat['keys'][pygame.K_2]:
        gamevars['player'].weaponSelect = 1
        gamevars['overlay'].update_text()
    elif f_dat['keys'][pygame.K_3]:
        gamevars['player'].weaponSelect = 2
        gamevars['overlay'].update_text()
    elif f_dat['keys'][pygame.K_4]:
        gamevars['player'].weaponSelect = 3
        gamevars['overlay'].update_text()
    elif f_dat['keys'][pygame.K_5]:
        gamevars['player'].weaponSelect = 4
        gamevars['overlay'].update_text()

    if f_dat['keys'][pygame.K_o]:
        gamevars['asteroids'].add(Asteroid())
        gamevars['overlay'].update_text()

    # Handle player shooting weapons.
    playerWeapon = gamevars['player'].weapons[gamevars['player'].weaponSelect]
    if f_dat['mouse_pressed'][0]:
        if playerWeapon[4]:
            if f_dat['current_time'] - playerWeapon[5] > playerWeapon[2]:
                playerWeapon[3](gamevars['player'].rect.center, f_dat['mouse_pos'])
                playerWeapon[5] = f_dat['current_time']
            
        else:
            if not gamevars['player'].hasShot and f_dat['current_time'] - playerWeapon[5] > playerWeapon[2]:
                playerWeapon[3](gamevars['player'].rect.center, f_dat['mouse_pos'])
                playerWeapon[5] = f_dat['current_time']
                gamevars['player'].hasShot = True

    else:
        gamevars['player'].hasShot = False

    # Update weapon cooldown display.
    gamevars['overlay'].update_weapon_cooldown_display(f_dat['current_time'])

    # Add asteroids according to waves.
    if gamevars['waves'][gamevars['wave']]['numAsteroids'] > 0 and gamevars['wave_timer'] > gamevars['waves'][gamevars['wave']]['spawnRate']:
        
        gamevars['asteroids'].add(Asteroid(pos=[-95, -95], type="satellite" if random.randrange(0, 100) > 90 else "normal", velocity=[(random.uniform(0.25, 0.75))*6, (random.uniform(0.25, 0.75))*6]))
        gamevars['overlay'].update_text()
        gamevars['wave_timer'] = 0
        gamevars['waves'][gamevars['wave']]['numAsteroids'] -= 1
    
    if gamevars['waves'][gamevars['wave']]['numAsteroids'] == 0 and len(gamevars['asteroids']) == 0:
        gamevars['wave'] += 1
        gamevars['player'].weapons[0][1] += 200
        gamevars['player'].weapons[0][1] += 15
        gamevars['player'].weapons[0][1] += 5
        gamevars['player'].weapons[0][1] += 200
        gamevars['player'].weapons[0][1] += 3
    else:
        gamevars['wave_timer'] += 1

    # Update all entities.
    gamevars['particles'].update()
    gamevars['bullets'].update()
    gamevars['asteroids'].update()
    gamevars['player'].update(f_dat['keys'], f_dat['mouse_pos'])

    # Handle player death.
    if gamevars['player'].health < 1:
        gamevars['game_state'] = "gameOver"
        gamevars['wave'] = 0
        gamevars['player'] = Player()
        gamevars['overlay'].update_player_healthbar()
        gamevars['overlay'].update_text()
        for asteroid in gamevars['asteroids']:
            asteroid.kill()
            del asteroid

        for bullet in gamevars['bullets']:
            bullet.kill()
            del bullet

        for particle in gamevars['particles']:
            particle.kill()
            del particle

    # Draw everything
    draw_everything(gamevars['display'])

def options_menu(f_dat, dest_surf):
    dest_surf.blit(sprites['background'], (0, 0))
    for particle in gamevars['particles']:
        particle.draw()

    for bullet in gamevars['bullets']:
        bullet.draw()

    gamevars['player'].draw()
    for asteroid in gamevars['asteroids']:
        asteroid.draw()
    
    gamevars['overlay'].draw()
    if f_dat['keys'][pygame.K_ESCAPE] and not gamevars['last_paused']:
        gamevars['game_state'] = 'paused' if not gamevars['game_state'] == 'paused' else 'game'
        gamevars['last_paused'] = True
    elif f_dat['keys'][pygame.K_ESCAPE] and gamevars['last_paused']:
        gamevars['last_paused'] = True
    else:
        gamevars['last_paused'] = False

def game_over_menu(f_dat, dest_surf):
    dest_surf.blit(sprites['background'], (0, 0))
    for button in gamevars['end_screen_overlay'].buttons:
        if button[1].collidepoint(f_dat['mouse_pos'][0], f_dat['mouse_pos'][1]):
            button[0].set_alpha(100)
        else:
            button[0].set_alpha(0)

    gamevars['end_screen_overlay'].draw()

    if f_dat['mouse_pressed'][0]: 
        if gamevars['end_screen_overlay'].buttons[0][1].collidepoint(f_dat['mouse_pos'][0], f_dat['mouse_pos'][1]):
            gamevars['mouse_image'] = sprites['cursor1']
            gamevars['game_state'] = 'game'

        elif gamevars['end_screen_overlay'].buttons[1][1].collidepoint(f_dat['mouse_pos'][0], f_dat['mouse_pos'][1]):
            run = False

def draw_everything(dest_surf):
    dest_surf.blit(sprites['background'], (0, 0))
    for particle in gamevars['particles']:
        particle.draw()

    for bullet in gamevars['bullets']:
        bullet.draw()

    gamevars['player'].draw()
    for asteroid in gamevars['asteroids']:
        asteroid.draw()
    
    gamevars['overlay'].draw()

    if gamevars['clock'].get_fps() < 40:
        for particle in gamevars['particles']:
            particle.kill()
            del particle

# def new_overlay(f_data):