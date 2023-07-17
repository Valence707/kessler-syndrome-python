import pygame, random, os
from constants import *

# Initialize essential modules, objects, and data
pygame.init()
pygame.font.init()
pygame.mixer.init()

# Global objects
display = pygame.display.set_mode(CONSTS['WIN_RES'], pygame.SCALED)
clock = pygame.time.Clock()

# All game data
from data import *
from gfx import *
from entities import *
from overlays import *

gamevars['display'] = display
pygame.display.set_caption("Kessler Syndrome")
pygame.display.set_icon(sprites['player_ship'])

gamevars['asteroids'] = pygame.sprite.Group()
gamevars['bullets'] = pygame.sprite.Group()
gamevars['particles'] = pygame.sprite.Group()
gamevars['player'] = Player()
gamevars['start_screen_overlay'] = StartScreenOverlay()
gamevars['end_screen_overlay'] = EndScreenOverlay()
gamevars['overlay'] = GameOverlay()
options['particles_enabled'] = True
gamevars['wave'] = 0

waves = [
    {'numAsteroids': 10, 'spawnRate': 100},
    {'numAsteroids': 20, 'spawnRate': 85},
    {'numAsteroids': 30, 'spawnRate': 70},
    {'numAsteroids': 40, 'spawnRate': 55},
    {'numAsteroids': 50, 'spawnRate': 40},
]

for i in range(50):
    waves.append({'numAsteroids': 50+(i*5), 'spawnRate': 40})

def main():
    run = True


    lastSong = 0
    currentSong = 0
    pygame.mixer.music.load(f'res/sounds/music/{music[currentSong]}')
    pygame.mixer.music.play()

    if options['particles_enabled']:
        for i in range(100):
            gamevars['particles'].add(Particle((random.randrange(0, CONSTS['WIN_RES'][0]-10), random.randrange(0, CONSTS['WIN_RES'][1]-10)), size=[1, 1], color=(255, 255, 255), velocityRange=0.5, duration=random.random()*10))

    lastPaused = False
    mouseImage = sprites['cursor2']

    gamevars['overlay'].update_text()

    pygame.mouse.set_visible(False)

    while run:

        # Play music randomly
        if not pygame.mixer.music.get_busy():
            lastSong = currentSong
            while True:
                currentSong = random.randrange(0, len(os.listdir(path='res/sounds/music')))
                
                if currentSong != lastSong:
                    pygame.mixer.music.load(f'res/sounds/music/{music[currentSong]}')
                    pygame.mixer.music.play()
                    break

        # Initialize frame data.
        keys = pygame.key.get_pressed()
        mousePos = pygame.mouse.get_pos()
        mousePressed = pygame.mouse.get_pressed(3)
        current_time = pygame.time.get_ticks()

        # Quit game if 'q' is pressed. CHANGE!
        if keys[pygame.K_q]:
            run = False
            continue

        # Handle events
        for event in pygame.event.get():

            # Quit game
            if event.type == pygame.QUIT:
                run = False
                break

            # Handle player scrolls
            elif event.type == pygame.MOUSEWHEEL:
                gamevars['player'].handle_scroll(event)

        # Draw the start screen.
        if gamevars['game_state'] == 'startScreen':
            gamevars['display'].blit(sprites['background'], (0, 0))
            if len(gamevars['particles']) < 100:
                gamevars['particles'].add(Particle((random.randrange(0, CONSTS['WIN_RES'][0]-10), random.randrange(0, CONSTS['WIN_RES'][1]-10)), size=[1, 1], color=(200, 200, 200), velocityRange=0.5, duration=random.random()*10))
            gamevars['particles'].update()
            gamevars['particles'].draw(gamevars['display'])
            gamevars['display'].blit(sprites['asteroids'][0], (15, 35))
            gamevars['display'].blit(sprites['asteroids'][1], (235, 65))
            gamevars['display'].blit(sprites['asteroids'][2], (35, 230))
            gamevars['display'].blit(sprites['asteroids'][3], (50, 135))
            gamevars['display'].blit(sprites['asteroids'][4], (145, 600))
            gamevars['display'].blit(pygame.transform.rotate(sprites['player_ship'], 45), (233, 212))

            # Change opacity of buttons as player hovers over them.
            for button in gamevars['start_screen_overlay'].buttons:
                if button[1].collidepoint(mousePos[0], mousePos[1]):
                    button[0].set_alpha(100)
                else:
                    button[0].set_alpha(0)

            gamevars['start_screen_overlay'].draw()

            # Detect and handle button presses.
            if mousePressed[0]: 
                if gamevars['start_screen_overlay'].buttons[0][1].collidepoint(mousePos[0], mousePos[1]):
                    mouseImage = sprites['cursor1']
                    gamevars['game_state'] = 'game'

        # The main game loop.
        elif gamevars['game_state'] == 'game':

            # Handle pausing the game
            if keys[pygame.K_ESCAPE] and not lastPaused:
                gamevars['game_state'] = 'paused' if not gamevars['game_state'] == 'paused' else 'game'
                lastPaused = True
            elif keys[pygame.K_ESCAPE] and lastPaused:
                lastPaused = True
            else:
                lastPaused = False

            # Handle keyboard input.
            if keys[pygame.K_1]:
                gamevars['player'].weaponSelect = 0
                gamevars['overlay'].update_text()
            elif keys[pygame.K_2]:
                gamevars['player'].weaponSelect = 1
                gamevars['overlay'].update_text()
            elif keys[pygame.K_3]:
                gamevars['player'].weaponSelect = 2
                gamevars['overlay'].update_text()
            elif keys[pygame.K_4]:
                gamevars['player'].weaponSelect = 3
                gamevars['overlay'].update_text()
            elif keys[pygame.K_5]:
                gamevars['player'].weaponSelect = 4
                gamevars['overlay'].update_text()

            if keys[pygame.K_o]:
                gamevars['asteroids'].add(Asteroid())
                gamevars['overlay'].update_text()

            # Handle player shooting weapons.
            playerWeapon = gamevars['player'].weapons[gamevars['player'].weaponSelect]
            if mousePressed[0]:
                if playerWeapon[4]:
                    if current_time - playerWeapon[5] > playerWeapon[2]:
                        playerWeapon[3](gamevars['player'].rect.center, mousePos)
                        playerWeapon[5] = current_time
                    
                else:
                    if not gamevars['player'].hasShot and current_time - playerWeapon[5] > playerWeapon[2]:
                        playerWeapon[3](gamevars['player'].rect.center, mousePos)
                        playerWeapon[5] = current_time
                        gamevars['player'].hasShot = True

            else:
                gamevars['player'].hasShot = False

            # Update weapon cooldown display.
            gamevars['overlay'].update_weapon_cooldown_display(current_time)

            # Add asteroids according to waves.
            if waves[gamevars['wave']]['numAsteroids'] > 0 and gamevars['wave_timer'] > waves[gamevars['wave']]['spawnRate']:
                
                gamevars['asteroids'].add(Asteroid(pos=[-95, -95], type="satellite" if random.randrange(0, 100) > 90 else "normal", velocity=[(random.uniform(0.25, 0.75))*6, (random.uniform(0.25, 0.75))*6]))
                gamevars['overlay'].update_text()
                gamevars['wave_timer'] = 0
                waves[gamevars['wave']]['numAsteroids'] -= 1
            
            if waves[gamevars['wave']]['numAsteroids'] == 0 and len(gamevars['asteroids']) == 0:
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
            gamevars['player'].update(keys, mousePos)

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
            gamevars['display'].blit(sprites['background'], (0, 0))
            for particle in gamevars['particles']:
                particle.draw()

            for bullet in gamevars['bullets']:
                bullet.draw()

            gamevars['player'].draw()
            for asteroid in gamevars['asteroids']:
                asteroid.draw()
            
            gamevars['overlay'].draw()

            if clock.get_fps() < 40:
                for particle in gamevars['particles']:
                    particle.kill()
                    del particle

        # Paused game loop.
        elif gamevars['game_state'] == 'paused':
            gamevars['display'].blit(sprites['background'], (0, 0))
            for particle in gamevars['particles']:
                particle.draw()

            for bullet in gamevars['bullets']:
                bullet.draw()

            gamevars['player'].draw()
            for asteroid in gamevars['asteroids']:
                asteroid.draw()
            
            gamevars['overlay'].draw()
            if keys[pygame.K_ESCAPE] and not lastPaused:
                gamevars['game_state'] = 'paused' if not gamevars['game_state'] == 'paused' else 'game'
                lastPaused = True
            elif keys[pygame.K_ESCAPE] and lastPaused:
                lastPaused = True
            else:
                lastPaused = False

        elif gamevars['game_state'] == 'gameOver':
            
            gamevars['display'].blit(sprites['background'], (0, 0))

            for button in gamevars['end_screen_overlay'].buttons:
                if button[1].collidepoint(mousePos[0], mousePos[1]):
                    button[0].set_alpha(100)
                else:
                    button[0].set_alpha(0)

            gamevars['end_screen_overlay'].draw()

            if mousePressed[0]: 
                if gamevars['end_screen_overlay'].buttons[0][1].collidepoint(mousePos[0], mousePos[1]):
                    mouseImage = sprites['cursor1']
                    gamevars['game_state'] = 'game'

                elif gamevars['end_screen_overlay'].buttons[1][1].collidepoint(mousePos[0], mousePos[1]):
                    run = False
                    break
        
        gamevars['display'].blit(mouseImage, (mousePos[0]-10, mousePos[1]-10))
        pygame.display.flip()
        clock.tick(CONSTS['T_FPS'])

main()