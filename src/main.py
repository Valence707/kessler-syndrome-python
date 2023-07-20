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
from program_functions import *

gvrs['display'] = display
gvrs['clock'] = clock
pygame.display.set_caption("Kessler Syndrome")
pygame.display.set_icon(sprites['player_ship'])

gvrs['player'] = Player()

# Change music volume
pygame.mixer.music.set_volume(options['music_volume'])

# Change volume of sounds
for sound in soundfx:
    soundfx[sound].set_volume(options['soundfx_volume'])

for i in sprites['asteroids']:
    i.set_colorkey((0, 0, 0))

for key in sprites:
    if not key == 'asteroids' and not key == 'background':
        sprites[key].set_colorkey((0, 0, 0))

# Main
def main():

    pygame.mixer.music.load(f'res/sounds/music/{music[gvrs["current_song"]]}')
    pygame.mixer.music.play()

    if options['particles_enabled']:
        for i in range(100):
            gvrs['particles'].add(Particle((random.randrange(0, options['win_res'][0]-10), random.randrange(0, options['win_res'][1]-10)), size=[1, 1], color=(255, 255, 255), velocityRange=0.5, duration=random.random()*10))

    gvrs['mouse_image'] = sprites['cursor2']

    pygame.mouse.set_visible(False)

    create_all_widgets()

    while gvrs['run']:

        gvrs['display'].fill((0, 0, 0))
        # Play music randomly
        if not pygame.mixer.music.get_busy():
            gvrs['last_song'] = gvrs['current_song']
            while True:
                gvrs['current_song'] = random.randrange(0, len(os.listdir(path='res/sounds/music')))
                
                if gvrs['current_song'] != gvrs['last_song']:
                    pygame.mixer.music.load(f'res/sounds/music/{music[gvrs["current_song"]]}')
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
            gvrs['run'] = False
            continue

        # Handle events
        for event in frame_data['events']:

            # Quit game
            if event.type == pygame.QUIT:
                gvrs['run'] = False
                break

            # Handle player scrolls
            elif event.type == pygame.MOUSEWHEEL:
                gvrs['player'].handle_scroll(event)

        # Draw the start screen.
        if get_game_state() == 'startScreen':
            start_screen(frame_data, gvrs['display'])

        # The main game loop.
        elif get_game_state() == 'game':
            game(frame_data)
            gvrs['display'].blit(sprites['overlay_test'], (0, 0))

        # Paused game loop.
        elif get_game_state() == 'paused':
            settings_menu(frame_data, gvrs['display'])

        # Game over loop.
        elif get_game_state() == 'gameOver':
            game_over_menu(frame_data, gvrs['display'])

        elif get_game_state() == 'testing':
            testing_mode(frame_data)
        
        gvrs['display'].blit(gvrs['mouse_image'], (frame_data['mouse_pos'][0]-10, frame_data['mouse_pos'][1]-10))
        pygame_widgets.update(frame_data['events'])
        pygame.display.flip()
        gvrs['clock'].tick(options['target_fps'])

main()