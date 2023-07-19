from data import *

class GameOverlay(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.healthbar = pygame.Surface((200, 20))
        self.healthbarBackground = pygame.Surface((210, 30))
        self.healthbarRect = self.healthbar.get_rect()
        pygame.Surface.fill(self.healthbar, (255, 0, 0))
        self.healthbar.set_alpha(175)
        self.healthbarBackground.set_alpha(175)

        rectangleTemplates = [
            {'pos': [997, 150], 'size': [175, 26], 'color': [255, 255, 255], 'opacity': 50},
            {'pos': [997, 180], 'size': [175, 26], 'color': [255, 255, 255], 'opacity': 50},
            {'pos': [997, 210], 'size': [175, 26], 'color': [255, 255, 255], 'opacity': 50},
            {'pos': [997, 240], 'size': [175, 26], 'color': [255, 255, 255], 'opacity': 50},
            {'pos': [997, 270], 'size': [175, 26], 'color': [255, 255, 255], 'opacity': 50},
        ]
        self.rectangles = []
        for rectangle in rectangleTemplates:
            newRectangle = {
                'image': pygame.Surface(rectangle['size']),
            }
            newRectangle['rect'] = newRectangle['image'].get_rect()
            newRectangle['pos'] = rectangle['pos']
            newRectangle['width'] = rectangle['size'][0]
            pygame.Surface.fill(newRectangle['image'], rectangle['color'])
            newRectangle['image'].set_alpha(rectangle['opacity'])
            self.rectangles.append(newRectangle)

        self.text = []

    def update_text(self):
        # Visiblity, font, text, color, position
        self.text = [
            [True, fonts['8bit_16px'], "HEALTH", [225, 225, 225], (1050, 20)],
            [True, fonts['8bit_16px'], f"ASTEROIDS LEFT: {len(gamevars['asteroids'])}", [175, 175, 175], (985, 40)],
            [True, fonts['8bit_16px'], f"WAVE: {gamevars['wave']}", [175, 175, 175], (985, 60)],
            [True, fonts['8bit_16px'], f"SCORE: {gamevars['player'].score}", [175, 175, 175], (985, 80)],
            [True, fonts['8bit_24px'], f"WEAPONS", [225, 225, 225], (1000, 125)],
            [True, fonts['8bit_regular_18px'], f"Main Gun", [150, 150, 150], (1000, 150)],
            [True, fonts['8bit_regular_18px'], f"Shotgun", [150, 150, 150], (1000, 180)],
            [True, fonts['8bit_regular_18px'], f"Photon Gun", [150, 150, 150], (1000, 210)],
            [True, fonts['8bit_regular_18px'], f"Machine Gun", [150, 150, 150], (1000, 240)],
            [True, fonts['8bit_regular_18px'], f"AMERICAN PRIDE", [150, 150, 150], (1000, 270)],
        ]
        self.text[gamevars['player'].weaponSelect+5][3] = [255, 255, 255]

    def update_player_healthbar(self):
        if gamevars['player'].health < 1:
            return
        self.healthbar = pygame.transform.scale(self.healthbar, (self.healthbarRect.width*(gamevars['player'].health / gamevars['player'].maxHealth), self.healthbarRect.height))

    def update_weapon_cooldown_display(self, time):
        
        for weapon in enumerate(gamevars['player'].weapons):
            if time - weapon[1][5] < weapon[1][2]:
                self.rectangles[weapon[0]]['image'].set_alpha(100)
                self.rectangles[weapon[0]]['image'] = pygame.transform.scale(self.rectangles[weapon[0]]['image'], [self.rectangles[weapon[0]]['width']*((time - weapon[1][5]) / weapon[1][2]), 26])
                pygame.Surface.fill(self.rectangles[weapon[0]]['image'], (175, 175, 175))
            else:
                self.rectangles[weapon[0]]['image'] = pygame.transform.scale(self.rectangles[weapon[0]]['image'], [self.rectangles[weapon[0]]['width'], 26])

    def draw(self):

        gamevars['display'].blit(self.healthbarBackground, (980, 10))
        gamevars['display'].blit(self.healthbar, (985, 15))

        for rectangle in self.rectangles:
            gamevars['display'].blit(rectangle['image'], rectangle['pos'])

        for text in self.text:
            if text[0]:
                gamevars['display'].blit(text[1].render(text[2], False, text[3]), text[4])


class StartScreenOverlay():
    def __init__(self):
        # Visiblity, font, text, color, position
        self.text = [
            [True, fonts['8bit_48px'], f"Kessler Syndrome", (255, 0, 0), (140, 150)],
            [True, fonts['8bit_24px'], f"Start", (0, 255, 0), (150, 225)],
            [True, fonts['8bit_regular_18px'], f"WASD to move up, left, down, and right. SPACE to brake. ESCAPE to pause.", (255, 255, 255), (100, 500)],
            [True, fonts['8bit_regular_18px'], f"Number keys or scroll to select weapon, left click to shoot.", (255, 255, 255), (100, 525)],
            [True, fonts['8bit_regular_12px'], f"By Marcus Secu", (255, 255, 255), (1095, 784)],
            [True, fonts['8bit_20px'], f"Good luck, soldier. Now go clean up our skies.", (255, 255, 100), (100, 560)],
        ]

        self.startButton = pygame.Surface((85, 30))
        self.startButtonRect = self.startButton.get_rect()
        self.startButtonRect.x, self.startButtonRect.y = 145, 217

        self.settingsButton = pygame.Surface((130, 30))
        self.settingsBtnRect = self.settingsButton.get_rect()
        self.settingsBtnRect.x, self.settingsBtnRect.y = 145, 253

        self.buttonTemplates = [
            [True, [145, 217], [85, 30], [255, 255, 255]],
        ]
        self.buttons = []
        
        # Turn self.buttons into button sprites with rects
        for button in enumerate(self.buttonTemplates):
            if button[1][0]:
                newButtonImage = pygame.Surface(button[1][2])
                pygame.Surface.fill(newButtonImage, button[1][3])
                newButtonRect = newButtonImage.get_rect()
                newButtonRect.x, newButtonRect.y = button[1][1][0], button[1][1][1]
                self.buttons.append([newButtonImage, newButtonRect])

    def draw(self):
        for text in self.text:
            if text[0]:
                gamevars['display'].blit(text[1].render(text[2], False, text[3]), text[4])

        for button in self.buttons:
            gamevars['display'].blit(button[0], (button[1].x, button[1].y))

class EndScreenOverlay():
    def __init__(self):
        # Visiblity, font, text, color, position
        self.text = [
            [True, fonts['8bit_48px'], f"GAME OVER!", (255, 255, 255), (150, 150)],
            [True, fonts['8bit_24px'], f"PLAY AGAIN", (255, 255, 255), (150, 260)],
            [True, fonts['8bit_24px'], f"SCORE: {gamevars['player'].score}", (255, 255, 255), (150, 225)],
            [True, fonts['8bit_24px'], f"QUIT", (255, 255, 255), (150, 295)],
        ]

        self.restartButton = pygame.Surface((85, 30))
        self.restartButtonRect = self.restartButton.get_rect()
        self.restartButtonRect.x, self.restartButtonRect.y = 145, 217

        self.quitButton = pygame.Surface((130, 30))
        self.quitBtnRect = self.quitButton.get_rect()
        self.quitBtnRect.x, self.quitBtnRect.y = 145, 253

        self.buttonTemplates = [
            [True, [145, 253], [160, 30], [255, 255, 255]],
            [True, [145, 289], [73, 30], [255, 255, 255]],
        ]
        self.buttons = []
        
        # Turn self.buttons into button sprites with rects
        for button in enumerate(self.buttonTemplates):
            if button[1][0]:
                newButtonImage = pygame.Surface(button[1][2])
                pygame.Surface.fill(newButtonImage, button[1][3])
                newButtonRect = newButtonImage.get_rect()
                newButtonRect.x, newButtonRect.y = button[1][1][0], button[1][1][1]
                self.buttons.append([newButtonImage, newButtonRect])

    def draw(self):
        for text in self.text:
            if text[0]:
                gamevars['display'].blit(text[1].render(text[2], False, text[3]), text[4])

        for button in self.buttons:
            gamevars['display'].blit(button[0], (button[1].x, button[1].y))