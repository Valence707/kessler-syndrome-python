import pygame, random, math, os

pygame.init()
pygame.font.init()
pygame.mixer.init()

# Constants
WIN_SIZE = (1200, 800)
TARGET_FPS = 60

# Global objects
display = pygame.display.set_mode(WIN_SIZE)
clock = pygame.time.Clock()

options = {
    'sound_enabled': True,
    'sound_volume': 0.5,
    'music_enabled': True,
    'music_volume': 0.5,
}

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

sprites = {
    'asteroids': [pygame.image.load(f'res/images/asteroid_{x+1}.png').convert() for x in range(5)],
    'bullet': pygame.image.load('res/images/bullet.png').convert(),
    'player_ship': pygame.image.load('res/images/ship.png').convert(),
    'cursors': [pygame.image.load(f'res/images/cursor{x+1}.png').convert() for x in range(2)],
    'background': pygame.image.load('res/images/background.png').convert()
}

sounds = {
    'music': [pygame.mixer.music.load(F'./res/sounds/music/{song}') for song in os.listdir(path='res/sounds/music')],
    'explosions': [pygame.mixer.Sound(f'res/sounds/explosion_{i+1}.wav') for i in range(10)],
    'blaster_shot': pygame.mixer.Sound('res/sounds/shoot.wav'),
    'shotgun_shot': pygame.mixer.Sound('res/sounds/shotgun_shoot.wav'),
    'photon_gun_shot': pygame.mixer.Sound('res/sounds/photon_rifle_shoot.wav'),
    'machine_gun_shot': pygame.mixer.Sound('res/sounds/automatic_cannon.wav'),
    'frag_cannon_shot': pygame.mixer.Sound('res/sounds/frag_cannon.wav'),
    'frag_cannon_burst': pygame.mixer.Sound('res/sounds/frag_explosion.wav')
}

for i in sprites['asteroids']:
    i.set_colorkey((0, 0, 0))

sprites['player_ship'].set_colorkey((0, 0, 0))
for i in sprites['cursors']:
    i.set_colorkey((0, 255, 0))

# Change volume of sounds
for sound in sounds:
    if sound == 'music' or sound == 'explosions':
        continue

    sounds[sound].set_volume(options['sound_volume'])

pygame.mixer.music.set_volume(options['music_volume'])

pygame.display.set_caption("Kessler Syndrome")
pygame.display.set_icon(sprites['player_ship'])

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = sprites['player_ship']
        self.rect = self.image.get_rect()
        self.pos = [WIN_SIZE[0] / 2 - 15, WIN_SIZE[1] / 2 - 15]
        self.rect.x, self.rect.y = self.pos[0], self.pos[1]
        self.velocity = [0, 0]
        self.maxVelocity = 4
        self.rotateAngle = 0
        self.rotated_rect = [0, 0]
        self.startTime = pygame.time.get_ticks()
        self.mass = self.rect.width
        self.score = 0
        self.health = 10000
        self.maxHealth = 10000
        self.hitTime = 0
        self.collisionTime = 0

        self.shootTime = 0
        self.hasShot = False
        self.weaponSelect = 0
        self.weapons = [
            ["Standard Blaster", 5000, 250, standard_blaster_shoot, False, 1],
            ["Shotgun", 75, 1000, shotgun_shoot, False, 1],
            ["Photon Rifle", 25, 3000, photon_rifle_shoot, False, 1],
            ["Automatic Cannon", 2500, 100, automatic_cannon_shoot, True, 1],
            ["Frag Cannon", 11, 5000, frag_cannon_shoot, False, 1]
        ]

    def update(self, keys, mousePos):
        if pygame.time.get_ticks() - self.collisionTime > 60:
            self.collisionTime = 0

        if not keys[pygame.K_SPACE] and not self.collisionTime > 0:
            if keys[pygame.K_w]:
                self.velocity[1] -= .25 if self.velocity[1] - 0.25 > -self.maxVelocity else 0

            if keys[pygame.K_s]:
                self.velocity[1] += .25 if self.velocity[1] + 0.25 < self.maxVelocity else 0

            if keys[pygame.K_a]:
                self.velocity[0] -= .25 if self.velocity[0] - 0.25 > -self.maxVelocity else 0
            
            if keys[pygame.K_d]:
                self.velocity[0] += .25 if self.velocity[0] + 0.25 < self.maxVelocity else 0
        
        else:
            self.velocity[0] = self.velocity[0] - 0.1 if self.velocity[0] > 0 else self.velocity[0] + 0.1 if self.velocity[0] < 0 else 0 if self.velocity[0] < 0.1 and self.velocity[0] > -0.1 else 0
            self.velocity[1] = self.velocity[1] - 0.1 if self.velocity[1] > 0 else self.velocity[1] + 0.1 if self.velocity[1] < 0 else 0 if self.velocity[1] < 0.1 and self.velocity[1] > -0.1 else 0
            if particlesEnabled:
                particles.add(Particle(player.rect.center, [1, 1], (255, 255, 255), 1))

        self.pos[0] += self.velocity[0]
        self.pos[1] += self.velocity[1]

        if self.pos[0] < -25:
            self.pos[0] = WIN_SIZE[0]
        elif self.pos[0] > WIN_SIZE[0]:
            self.pos[0] = -24
        
        if self.pos[1] < -25:
            self.pos[1] = WIN_SIZE[1]
        elif self.pos[1] > WIN_SIZE[1]:
            self.pos[1] = -24

        self.rect.x, self.rect.y = self.pos[0], self.pos[1]

        collidedAsteroid = pygame.sprite.spritecollideany(self, asteroids)
        if collidedAsteroid:
            self.collisionTime = pygame.time.get_ticks()
            if pygame.time.get_ticks() - self.hitTime > 500:
                self.health -= 10 if collidedAsteroid.mass > 75 else 5 if collidedAsteroid.mass > 25 else 1
                self.hitTime = pygame.time.get_ticks()

            overlay.update_player_healthbar()
            dx = abs(self.rect.centerx - collidedAsteroid.rect.centerx)
            dy = abs(self.rect.centery - collidedAsteroid.rect.centery)
            if dx > dy:
                self.rect.x -= self.velocity[0]
                collidedAsteroid.pos[0] -= collidedAsteroid.velocity[0]

                astVel = collidedAsteroid.velocity[0]
                collidedAsteroid.velocity[0] = self.velocity[0] * (self.mass / collidedAsteroid.mass)
                self.velocity[0] = astVel * (collidedAsteroid.mass / self.mass)
            elif dy > dx:
                self.rect.x -= self.velocity[1]
                collidedAsteroid.pos[1] -= collidedAsteroid.velocity[1]

                astVel = collidedAsteroid.velocity[1]
                collidedAsteroid.velocity[1] = self.velocity[1] * (self.mass / collidedAsteroid.mass)
                self.velocity[1] = astVel * (collidedAsteroid.mass / self.mass)
            
        mousePos = pygame.math.Vector2(mousePos)
        playerPos = pygame.math.Vector2(self.rect.center)
        ds2mx = playerPos[0]-mousePos[0]
        ds2my = playerPos[1]-mousePos[1]
        ds2ml = math.sqrt(ds2mx**2 + ds2my**2)
        self.rotateAngle = math.atan2(ds2mx / ds2ml, ds2my / ds2ml) * 57.29578

        if particlesEnabled and (pygame.time.get_ticks() - self.startTime) % 100 >= 75:
            particles.add(Particle((self.rect.x+random.randrange(0, self.rect.width), self.rect.y+random.randrange(0, self.rect.height)), [4, 4], (random.randrange(0, 2)*255, random.randrange(0, 2)*255, random.randrange(0, 2)*255), 0.1, 1))

    def draw(self):
        rotated_image = pygame.transform.rotate(self.image, self.rotateAngle)
        self.rotated_rect = rotated_image.get_rect()
        display.blit(rotated_image, (self.rect.x-(self.rotated_rect.width - self.rect.width)/2, self.rect.y-(self.rotated_rect.height - self.rect.height)/2))

class Asteroid(pygame.sprite.Sprite):
    def __init__(self, type='normal', pos=None, size=None, velocity=None, minVelocity=0.25):
        super().__init__()
        self.type = type
        randomSize = 50 if type == 'satellite' else random.randrange(40, 110) if not size else size
        self.image = pygame.transform.scale(sprites['asteroids'][len(sprites['asteroids'])-1] if type == 'satellite' else sprites['asteroids'][random.randrange(0, len(sprites['asteroids'])-1)], (randomSize, randomSize))
        self.rect = self.image.get_rect()
        self.pos = [random.randrange(0, WIN_SIZE[0]), random.randrange(0, WIN_SIZE[1])] if not pos else pos
        self.velocity = [(random.random()-0.5)*4, (random.random()-0.5)*4] if not velocity else velocity
        self.minVelocity = minVelocity
        if self.velocity[0] < minVelocity and self.velocity[0] > -minVelocity:
            self.velocity[0] += -minVelocity if self.velocity[0] < 0 else minVelocity
        if self.velocity[1] < minVelocity and self.velocity[1] > -minVelocity:
            self.velocity[1] += -minVelocity if self.velocity[1] < 0 else minVelocity
        self.mass = randomSize

        self.health = 5 if randomSize > 70 else 3 if randomSize > 40 else 1
        self.maxHealth = self.health
        self.rotateAngle = 0
        self.rotateSpeed = random.randrange(-1, 2, 2)*random.random()*3
        self.spawnTime = 10000
        self.startTime = pygame.time.get_ticks()

        self.hBarBkgrnd = pygame.Surface((self.rect.width, 5))
        self.hBar = pygame.Surface((self.rect.width, 5))
        self.hBarRect = self.hBar.get_rect()
        pygame.Surface.fill(self.hBar, (255, 0, 0))

        self.rect.x, self.rect.y = self.pos[0], self.pos[1]

    def update(self):
        self.pos[0], self.pos[1] = self.pos[0]+self.velocity[0], self.pos[1]+self.velocity[1]
        if self.pos[0] < -100 or self.pos[1] < -100 or self.pos[0] > WIN_SIZE[0]+50 or self.pos[1] > WIN_SIZE[1]+50:
            newPos = []
            while True:
                newPos = [
                    random.randrange(-120, WIN_SIZE[0]+120),
                    random.randrange(-120, WIN_SIZE[1]+120)
                ]
                if not (newPos[0] > -1*self.rect.width and newPos[0] < WIN_SIZE[0]+self.rect.width and newPos[1] > -1*self.rect.height and newPos[1] < WIN_SIZE[1]+self.rect.height):
                    self.velocity = [(random.random()-0.5)*4, (random.random()-0.5)*4]
                    if self.velocity[0] < self.minVelocity and self.velocity[0] > -self.minVelocity:
                        self.velocity[0] += -self.minVelocity if self.velocity[0] < 0 else self.minVelocity
                    if self.velocity[1] < self.minVelocity and self.velocity[1] > -self.minVelocity:
                        self.velocity[1] += -self.minVelocity if self.velocity[1] < 0 else self.minVelocity
                    break

            self.pos = newPos

        if particlesEnabled:
            if self.health == 5 and (pygame.time.get_ticks() - self.startTime) % 100 >= 60:
                colorRange = random.randrange(75, 125)
                randomParticleSize = random.randrange(3, 7)
                particles.add(Particle((self.pos[0]+random.randrange(0, self.rect.width), self.pos[1]+random.randrange(0, self.rect.height)), [randomParticleSize, randomParticleSize], (colorRange, colorRange/2, colorRange/2), 0.25, 1))
            elif self.health == 3 and (pygame.time.get_ticks() - self.startTime) % 100 >= 70:
                colorRange = random.randrange(75, 125)
                randomParticleSize = random.randrange(2, 5)
                particles.add(Particle((self.pos[0]+random.randrange(0, self.rect.width), self.pos[1]+random.randrange(0, self.rect.height)), [randomParticleSize, randomParticleSize], (colorRange, colorRange/2, colorRange/2), 0.25, 1))
            elif self.health == 1 and (pygame.time.get_ticks() - self.startTime) % 100 >= 80:
                colorRange = random.randrange(75, 125)
                randomParticleSize = random.randrange(1, 3)
                particles.add(Particle((self.pos[0]+random.randrange(0, self.rect.width), self.pos[1]+random.randrange(0, self.rect.height)), [randomParticleSize, randomParticleSize], (colorRange, colorRange/2, colorRange/2), 0.25, 1))

        self.rotateAngle += self.rotateSpeed
        self.rect.x, self.rect.y = self.pos[0], self.pos[1]
        self.hBarRect.x, self.hBarRect.y = self.pos[0], self.pos[1]-15

    def die(self):
        self.kill()
        player.score += 1

        sounds['explosions'][random.randrange(0, len(sounds['explosions']))].play()
        overlay.update_text()

        if self.type == 'satellite':
            if particlesEnabled:
                for i in range(25):
                    colorRange = random.randrange(150, 255)
                    randomParticleSize = random.randrange(4, 10)
                    particles.add(Particle((self.pos[0]+random.randrange(0, self.rect.width), self.pos[1]+random.randrange(0, self.rect.height)), [randomParticleSize, randomParticleSize], (colorRange, colorRange, colorRange/4), 2, (random.random()+0.1)*2))

                dropChance = random.randrange(0, 100)
        else:
            if particlesEnabled and self.maxHealth == 1:
                for i in range(10):
                    colorRange = random.randrange(75, 255)
                    randomParticleSize = random.randrange(4, 10)
                    particles.add(Particle((self.pos[0]+random.randrange(0, self.rect.width), self.pos[1]+random.randrange(0, self.rect.height)), [randomParticleSize, randomParticleSize], (colorRange, colorRange/3, colorRange/4), 2, (random.random()+0.1)*2))

            elif self.maxHealth == 3:
                for i in range(random.randrange(2, 10)):
                    asteroids.add(Asteroid(pos=[self.pos[0]+random.randrange(0, self.rect.width), self.pos[1]+random.randrange(0, self.rect.height)], size=random.randrange(30, 40)))

                if particlesEnabled:
                    for i in range(30):
                        colorRange = random.randrange(75, 255)
                        randomParticleSize = random.randrange(4, 10)
                        particles.add(Particle((self.pos[0]+random.randrange(0, self.rect.width), self.pos[1]+random.randrange(0, self.rect.height)), [randomParticleSize, randomParticleSize], (colorRange, colorRange/3, colorRange/4), 2, (random.random()+0.1)*2))

            elif self.maxHealth == 5:
                for i in range(random.randrange(3, 30)):
                    asteroids.add(Asteroid(pos=[self.pos[0]+random.randrange(0, self.rect.width), self.pos[1]+random.randrange(0, self.rect.height)], size=random.randrange(30, 40)))
                    
                if particlesEnabled:
                    for i in range(75):
                        colorRange = random.randrange(75, 255)
                        randomParticleSize = random.randrange(4, 10)
                        particles.add(Particle((self.pos[0]+random.randrange(0, self.rect.width), self.pos[1]+random.randrange(0, self.rect.height)), [randomParticleSize, randomParticleSize], (colorRange, colorRange/3, colorRange/4), 6, (random.random()+0.1)*2))

        del self
        return

    def update_health(self, amnt):
            self.health -= amnt
            if self.health < 1:
                self.die()
            else:
                self.hBar = pygame.transform.scale(self.hBar, (self.hBarRect.width*(self.health / self.maxHealth), self.hBarRect.height))

    def draw(self):
        rotated_image = pygame.transform.rotate(self.image, self.rotateAngle)
        display.blit(rotated_image, (self.rect.x-(rotated_image.get_rect().width - self.rect.width)/2, self.rect.y-(rotated_image.get_rect().height - self.rect.height)/2))
        if self.health != self.maxHealth:
            display.blit(self.hBarBkgrnd, (self.hBarRect.x, self.hBarRect.y))
            display.blit(self.hBar, (self.hBarRect.x, self.hBarRect.y))

class Bullet(pygame.sprite.Sprite):
    def __init__(self, origin, destination, image=None, size=[2, 2], velocity=15, spread=0, damage=1, color=(255, 255, 0), trailColor=(255, 255, 0), particleDensity=10, dieFunc = None):
        super().__init__()
        self.image = image if image else pygame.Surface(size)
        if not image:
            pygame.Surface.fill(self.image, color)
        
        self.color = color
        self.trailColor = trailColor
        self.rect = self.image.get_rect()
        self.pos = [origin[0], origin[1]]
        self.rect.x, self.rect.y = origin[0], origin[1]
        # destination = pygame.math.Vector2(destination)
        ds2mx = origin[0]-destination[0]
        ds2my = origin[1]-destination[1]
        self.direction = None
        try:
            self.direction = -pygame.math.Vector2([ds2mx, ds2my]).normalize()
        except:
            return
        self.direction.x += random.uniform(-spread, spread)
        self.direction.y += random.uniform(-spread, spread)
        self.velocity = velocity
        self.startTime = pygame.time.get_ticks()
        # ds2ml = math.sqrt(ds2mx**2 + ds2my**2)
        # self.rotateAngle = math.atan2(ds2mx / ds2ml, ds2my / ds2ml) * 57.29578
        self.damage = damage
        self.particleDensity = particleDensity
        self.dieFunc = dieFunc

    def update(self):
        self.pos[0] += self.velocity * self.direction.x
        self.pos[1] += self.velocity * self.direction.y
        self.rect.x, self.rect.y = self.pos[0]-self.rect.width/2, self.pos[1]-self.rect.height/2

        collided = pygame.sprite.spritecollideany(self, asteroids)
        if collided:
            collided.update_health(self.damage)
            self.kill()
            if self.dieFunc:
                self.dieFunc(self.pos)

            if particlesEnabled:
                for i in range(10):
                    particles.add(Particle(origin=self.pos, color=self.color, velocityRange=0.5, size=[1, 1], duration=random.random()*3+1))

            del self
            return

        # Uncomment this for horrible chaos
        # if self.pos[0] < 0:
        #     self.pos[0] = WIN_SIZE[0]
        # elif self.pos[0] > WIN_SIZE[0]:
        #     self.pos[0] = 0
        
        # if self.pos[1] < 0:
        #     self.pos[1] = WIN_SIZE[1]
        # elif self.pos[1] > WIN_SIZE[1]:
        #     self.pos[1] = 0

        if self.pos[0] < -120 or self.pos[1] < -120 or self.pos[0] > WIN_SIZE[0] + 120 or self.pos[1] > WIN_SIZE[1] + 120:
            self.kill()
            del self
            return

        if particlesEnabled and (pygame.time.get_ticks()) % 100 >= self.particleDensity:
            particles.add(Particle(self.pos, duration=random.uniform(0.15, 0.3), velocityRange=0.5, color=self.trailColor))

    def draw(self):
        # rotated_image = pygame.transform.rotate(self.image, self.rotateAngle)
        # display.blit(rotated_image, (self.rect.x-(rotated_image.get_rect().width - self.rect.width)/2, self.rect.y-(rotated_image.get_rect().height - self.rect.height)/2))
        display.blit(self.image, (self.rect.x, self.rect.y))

class Particle(pygame.sprite.Sprite):
    def __init__(self, origin, size=[2, 2], color=(255, 255, 0), velocityRange=0.25, duration=1, destination=None,):
        super().__init__()
        self.image = pygame.Surface(size)
        pygame.Surface.fill(self.image, color)
        self.rect = self.image.get_rect()
        self.pos = [origin[0], origin[1]]
        if destination:
            pass
        else:
            self.velocity = [random.randrange(-1, 2, 2)*random.random()*velocityRange, random.randrange(-1, 2, 2)*random.random()*velocityRange]
        self.startTime = pygame.time.get_ticks()
        self.duration = duration

    def update(self):
        if pygame.time.get_ticks() - self.startTime > self.duration*1000:
            self.kill()
            del self
            return

        self.pos[0] += self.velocity[0]
        self.pos[1] += self.velocity[1]
        self.rect.x, self.rect.y = self.pos

    def draw(self):
        display.blit(self.image, (self.rect.x, self.rect.y))

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
            [True, fonts['8bit_16px'], f"ASTEROIDS LEFT: {len(asteroids)}", [175, 175, 175], (985, 40)],
            [True, fonts['8bit_16px'], f"WAVE: {wave}", [175, 175, 175], (985, 60)],
            [True, fonts['8bit_16px'], f"SCORE: {player.score}", [175, 175, 175], (985, 80)],
            [True, fonts['8bit_24px'], f"WEAPONS", [225, 225, 225], (1000, 125)],
            [True, fonts['8bit_regular_18px'], f"Main Gun", [150, 150, 150], (1000, 150)],
            [True, fonts['8bit_regular_18px'], f"Shotgun", [150, 150, 150], (1000, 180)],
            [True, fonts['8bit_regular_18px'], f"Photon Gun", [150, 150, 150], (1000, 210)],
            [True, fonts['8bit_regular_18px'], f"Machine Gun", [150, 150, 150], (1000, 240)],
            [True, fonts['8bit_regular_18px'], f"AMERICAN PRIDE", [150, 150, 150], (1000, 270)],
        ]
        self.text[player.weaponSelect+5][3] = [255, 255, 255]

    def update_player_healthbar(self):
        if player.health < 1:
            return
        self.healthbar = pygame.transform.scale(self.healthbar, (self.healthbarRect.width*(player.health / player.maxHealth), self.healthbarRect.height))

    def update_weapon_cooldown_display(self, time):
        
        for weapon in enumerate(player.weapons):
            if time - weapon[1][5] < weapon[1][2]:
                self.rectangles[weapon[0]]['image'].set_alpha(100)
                self.rectangles[weapon[0]]['image'] = pygame.transform.scale(self.rectangles[weapon[0]]['image'], [self.rectangles[weapon[0]]['width']*((time - weapon[1][5]) / weapon[1][2]), 26])
                pygame.Surface.fill(self.rectangles[weapon[0]]['image'], (175, 175, 175))
            else:
                self.rectangles[weapon[0]]['image'] = pygame.transform.scale(self.rectangles[weapon[0]]['image'], [self.rectangles[weapon[0]]['width'], 26])

    def draw(self):

        display.blit(self.healthbarBackground, (980, 10))
        display.blit(self.healthbar, (985, 15))

        for rectangle in self.rectangles:
            display.blit(rectangle['image'], rectangle['pos'])

        for text in self.text:
            if text[0]:
                display.blit(text[1].render(text[2], False, text[3]), text[4])


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
                display.blit(text[1].render(text[2], False, text[3]), text[4])

        for button in self.buttons:
            display.blit(button[0], (button[1].x, button[1].y))

class EndScreenOverlay():
    def __init__(self):
        # Visiblity, font, text, color, position
        self.text = [
            [True, fonts['8bit_48px'], f"GAME OVER!", (255, 255, 255), (150, 150)],
            [True, fonts['8bit_24px'], f"PLAY AGAIN", (255, 255, 255), (150, 260)],
            [True, fonts['8bit_24px'], f"SCORE: {player.score}", (255, 255, 255), (150, 225)],
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
                display.blit(text[1].render(text[2], False, text[3]), text[4])

        for button in self.buttons:
            display.blit(button[0], (button[1].x, button[1].y))

def standard_blaster_shoot(origin, destination):
    bullets.add(Bullet(origin, destination, velocity=15, spread=0))
    sounds['blaster_shot'].play()

def shotgun_shoot(origin, destination):
    for i in range(7):
        bullets.add(Bullet(origin, [destination[0]+(i-5)*10, destination[1]+(i-5)*10], spread=0.15))
    sounds['shotgun_shot'].play()

def photon_rifle_shoot(origin, destination):
    bullets.add(Bullet(origin, destination, spread=0, size=[10, 10], velocity=25, damage=100, color=(100, 100, 255), trailColor=(100, 100, 255)))
    sounds['photon_gun_shot'].play()

def automatic_cannon_shoot(origin, destination):
    bullets.add(Bullet(origin, destination, spread=0.15, size=[2, 2], velocity=15, damage=1, color=(255, 100, 100), trailColor=(255, 100, 100), particleDensity=50))
    sounds['machine_gun_shot'].play()

american_colors = [(255, 0, 0), (255, 255, 255), (0, 0, 255)]

def frag_bullet_explosion(origin, velocity = 5, amount = 100):
    for i in range(amount):
        bulletPos = [origin[0]+random.randrange(-amount, amount), origin[1]+random.randrange(-amount, amount)]
        bullets.add(Bullet(origin, bulletPos, velocity=velocity+random.randrange(0, 3), color=american_colors[random.randrange(0, 3)], particleDensity=100))

    if particlesEnabled:
        for i in range(150):
            colorRange = random.randrange(75, 255)
            randomParticleSize = random.randrange(5, 15)
            particles.add(Particle((origin[0]+random.randrange(0, 6), origin[1]+random.randrange(0, 6)), [randomParticleSize, randomParticleSize], american_colors[random.randrange(0, 3)], 6, (random.random()+0.1)*2))

    sounds['frag_cannon_burst'].play()

def frag_cannon_shoot(origin, destination):
    bullets.add(Bullet(origin, destination, spread=0, size=[15, 15], velocity=10, damage=3, color=(255, 255, 255), trailColor=(255, 255, 255), dieFunc=frag_bullet_explosion))
    sounds['frag_cannon_shot'].play()

# def set_game_state(state):
#     global 

def set_sound_volume():
    pass

asteroids = pygame.sprite.Group()
bullets = pygame.sprite.Group()
particles = pygame.sprite.Group()
player = Player()
start_screen_overlay = StartScreenOverlay()
end_screen_overlay = EndScreenOverlay()
overlay = GameOverlay()
particlesEnabled = True
wave = 0

waves = [
    {'numAsteroids': 10, 'spawnRate': 100},
    {'numAsteroids': 20, 'spawnRate': 85},
    {'numAsteroids': 30, 'spawnRate': 70},
    {'numAsteroids': 40, 'spawnRate': 55},
    {'numAsteroids': 50, 'spawnRate': 40},
]

for i in range(50):
    waves.append({'numAsteroids': 50+(i+1), 'spawnRate': 40})

# Debug wave
# waves = [
#     {'numAsteroids': 1, 'spawnRate': 10}
# ]

def main():
    global wave, particlesEnabled, player
    run = True

    gameState = "startScreen"
    waveTimer = 0

    lastSong = 0
    currentSong = 0
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play()

    for i in range(100):
        if particlesEnabled:
            particles.add(Particle((random.randrange(0, WIN_SIZE[0]-10), random.randrange(0, WIN_SIZE[1]-10)), size=[1, 1], color=(255, 255, 255), velocityRange=0.5, duration=random.random()*10))

    lastPaused = False
    mouseImage = sprites['cursors'][1]

    overlay.update_text()
    print(player)

    dt = 0

    pygame.mouse.set_visible(False)

    while run:
        if not pygame.mixer.music.get_busy():
            lastSong = currentSong
            while True:
                currentSong = random.randrange(0, len(sounds['music']))
                if currentSong != lastSong:
                    pygame.mixer.music.play()
                    break

        keys = pygame.key.get_pressed()
        mousePos = pygame.mouse.get_pos()
        mousePressed = pygame.mouse.get_pressed(3)
        current_time = pygame.time.get_ticks()
        if keys[pygame.K_q]:
            run = False
            continue

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            elif event.type == pygame.MOUSEWHEEL:
                player.weaponSelect += -event.y
                player.weaponSelect = 0 if player.weaponSelect+1 > len(player.weapons) else len(player.weapons)-1 if player.weaponSelect < 0 else player.weaponSelect
                player.shootTime = 0
                overlay.update_text()

        if gameState == 'startScreen':
            display.blit(sprites['background'], (0, 0))
            if len(particles) < 100:
                particles.add(Particle((random.randrange(0, WIN_SIZE[0]-10), random.randrange(0, WIN_SIZE[1]-10)), size=[1, 1], color=(200, 200, 200), velocityRange=0.5, duration=random.random()*10))
            particles.update()
            particles.draw(display)
            display.blit(sprites['asteroids'][0], (15, 35))
            display.blit(sprites['asteroids'][1], (235, 65))
            display.blit(sprites['asteroids'][2], (35, 230))
            display.blit(sprites['asteroids'][3], (50, 135))
            display.blit(sprites['asteroids'][4], (145, 600))
            display.blit(pygame.transform.rotate(sprites['player_ship'], 45), (233, 212))

            for button in start_screen_overlay.buttons:
                if button[1].collidepoint(mousePos[0], mousePos[1]):
                    button[0].set_alpha(100)
                else:
                    button[0].set_alpha(0)

            start_screen_overlay.draw()

            if mousePressed[0]: 
                if start_screen_overlay.buttons[0][1].collidepoint(mousePos[0], mousePos[1]):
                    mouseImage = sprites['cursors'][0]
                    gameState = 'game'

        elif gameState == 'game':

            if keys[pygame.K_ESCAPE] and not lastPaused:
                gameState = 'paused' if not gameState == 'paused' else 'game'
                lastPaused = True
            elif keys[pygame.K_ESCAPE] and lastPaused:
                lastPaused = True
            else:
                lastPaused = False

            if keys[pygame.K_1]:
                player.weaponSelect = 0
                overlay.update_text()
            elif keys[pygame.K_2]:
                player.weaponSelect = 1
                overlay.update_text()
            elif keys[pygame.K_3]:
                player.weaponSelect = 2
                overlay.update_text()
            elif keys[pygame.K_4]:
                player.weaponSelect = 3
                overlay.update_text()
            elif keys[pygame.K_5]:
                player.weaponSelect = 4
                overlay.update_text()

            if keys[pygame.K_o]:
                asteroids.add(Asteroid())
                overlay.update_text()

            playerWeapon = player.weapons[player.weaponSelect]
            if mousePressed[0]:
                if playerWeapon[4]:
                    if current_time - playerWeapon[5] > playerWeapon[2]:
                        playerWeapon[3](player.rect.center, mousePos)
                        playerWeapon[5] = current_time
                    
                else:
                    if not player.hasShot and current_time - playerWeapon[5] > playerWeapon[2]:
                        playerWeapon[3](player.rect.center, mousePos)
                        playerWeapon[5] = current_time
                        player.hasShot = True

            else:
                player.hasShot = False

            overlay.update_weapon_cooldown_display(current_time)


            if waves[wave]['numAsteroids'] > 0 and waveTimer > waves[wave]['spawnRate']:
                
                asteroids.add(Asteroid(pos=[-95, -95], type="satellite" if random.randrange(0, 100) > 90 else "normal", velocity=[(random.uniform(0.25, 0.75))*6, (random.uniform(0.25, 0.75))*6]))
                overlay.update_text()
                waveTimer = 0
                waves[wave]['numAsteroids'] -= 1
            
            if waves[wave]['numAsteroids'] == 0 and len(asteroids) == 0:
                wave += 1
                player.weapons[0][1] += 200
                player.weapons[0][1] += 15
                player.weapons[0][1] += 5
                player.weapons[0][1] += 200
                player.weapons[0][1] += 3
            else:
                waveTimer += 1

            particles.update()
            bullets.update()
            asteroids.update()
            player.update(keys, mousePos)

            if player.health < 1:
                gameState = "gameOver"
                wave = 0
                player = Player()
                overlay.update_player_healthbar()
                overlay.update_text()
                for asteroid in asteroids:
                    asteroid.kill()
                    del asteroid

                for bullet in bullets:
                    bullet.kill()
                    del bullet

                for particle in particles:
                    particle.kill()
                    del particle

            display.blit(sprites['background'], (0, 0))
            for particle in particles:
                particle.draw()

            for bullet in bullets:
                bullet.draw()

            player.draw()
            for asteroid in asteroids:
                asteroid.draw()
            
            overlay.draw()

            if clock.get_fps() < 40:
                for particle in particles:
                    particle.kill()
                    del particle

        elif gameState == 'paused':
            display.blit(sprites['background'], (0, 0))
            for particle in particles:
                particle.draw()

            for bullet in bullets:
                bullet.draw()

            player.draw()
            for asteroid in asteroids:
                asteroid.draw()
            
            overlay.draw()
            if keys[pygame.K_ESCAPE] and not lastPaused:
                gameState = 'paused' if not gameState == 'paused' else 'game'
                lastPaused = True
            elif keys[pygame.K_ESCAPE] and lastPaused:
                lastPaused = True
            else:
                lastPaused = False

        elif gameState == 'gameOver':
            
            display.blit(sprites['background'], (0, 0))

            for button in end_screen_overlay.buttons:
                if button[1].collidepoint(mousePos[0], mousePos[1]):
                    button[0].set_alpha(100)
                else:
                    button[0].set_alpha(0)

            end_screen_overlay.draw()

            if mousePressed[0]: 
                if end_screen_overlay.buttons[0][1].collidepoint(mousePos[0], mousePos[1]):
                    mouseImage = sprites['cursors'][0]
                    gameState = 'game'

                elif end_screen_overlay.buttons[1][1].collidepoint(mousePos[0], mousePos[1]):
                    run = False
                    break
        
        display.blit(mouseImage, (mousePos[0]-10, mousePos[1]-10))
        pygame.display.flip()
        
        print(clock.tick(TARGET_FPS))

main()