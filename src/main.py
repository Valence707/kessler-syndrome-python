import pygame, random, os

# Initialize essential modules, objects, and data
pygame.init()
pygame.font.init()
pygame.mixer.init()

# Global objects
display = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
clock = pygame.time.Clock()

# All game data
from data import *
from gfx import *
from entities import *
from overlays import *
from program_functions import *

gamevars['display'] = display
gamevars['clock'] = clock
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

gamevars['waves'] = [
    {'numAsteroids': 10, 'spawnRate': 100},
    {'numAsteroids': 20, 'spawnRate': 85},
    {'numAsteroids': 30, 'spawnRate': 70},
    {'numAsteroids': 40, 'spawnRate': 55},
    {'numAsteroids': 50, 'spawnRate': 40},
]

for i in range(50):
    gamevars['waves'].append({'numAsteroids': 50+(i*5), 'spawnRate': 40})

def main():

    run = True
    init_start_screen()
    gamevars['last_song'] = 0
    gamevars['current_song'] = 0
    pygame.mixer.music.load(f'res/sounds/music/{music[gamevars["current_song"]]}')
    pygame.mixer.music.play()

    if options['particles_enabled']:
        for i in range(100):
            gamevars['particles'].add(Particle((random.randrange(0, options['win_res'][0]-10), random.randrange(0, options['win_res'][1]-10)), size=[1, 1], color=(255, 255, 255), velocityRange=0.5, duration=random.random()*10))

    gamevars['last_paused'] = False
    gamevars['mouse_image'] = sprites['cursor2']
    gamevars['overlay'].update_text()

    pygame.mouse.set_visible(False)

    while run:

        gamevars['display'].fill((0, 0, 0))
        # Play music randomly
        if not pygame.mixer.music.get_busy():
            gamevars['last_song'] = gamevars['current_song']
            while True:
                gamevars['current_song'] = random.randrange(0, len(os.listdir(path='res/sounds/music')))
                
                if gamevars['current_song'] != gamevars['last_song']:
                    pygame.mixer.music.load(f'res/sounds/music/{music[gamevars["current_song"]]}')
                    pygame.mixer.music.play()
                    break

        # Data important for each frame
        frame_data = {
            'keys': pygame.key.get_pressed(),
            'mouse_pos': pygame.mouse.get_pos(),
            'mouse_pressed': pygame.mouse.get_pressed(3),
            'current_time': pygame.time.get_ticks(),
            'events': pygame.event.get()
        }

        # Quit game if 'q' is pressed. CHANGE!
        if frame_data['keys'][pygame.K_q]:
            run = False
            continue

        # Handle events
        for event in frame_data['events']:

            # Quit game
            if event.type == pygame.QUIT:
                run = False
                break

            # Handle player scrolls
            elif event.type == pygame.MOUSEWHEEL:
                gamevars['player'].handle_scroll(event)

        # Draw the start screen.
        if gamevars['game_state'] == 'startScreen':
            start_screen(frame_data, gamevars['display'])

        # The main game loop.
        elif gamevars['game_state'] == 'game':
            game(frame_data)
            gamevars['display'].blit(sprites['overlay_test'], (0, 0))

        # Paused game loop.
        elif gamevars['game_state'] == 'paused':
            options_menu(frame_data, gamevars['display'])

        # Game over loop.
        elif gamevars['game_state'] == 'gameOver':
            game_over_menu(frame_data, gamevars['display'])

        elif gamevars['game_state'] == 'testing':
            testing_mode(frame_data)
        
        gamevars['display'].blit(gamevars['mouse_image'], (frame_data['mouse_pos'][0]-10, frame_data['mouse_pos'][1]-10))
        pygame_widgets.update(frame_data['events'])
        pygame.display.flip()
        gamevars['clock'].tick(options['target_fps'])

main()