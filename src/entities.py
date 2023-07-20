import pygame, math, random
from data import *
from gfx import *

class Asteroid(pygame.sprite.Sprite):
    
    """ Asteroids are obstacles that the player shoots at and must avoid being hit by. They
        drift with set velocities and may break into smaller asteroids upon impact. """
    
    def __init__(self, type='normal', pos=None, size=None, velocity=None, minVelocity=0.25):
        super().__init__()
        self.type, self.minVelocity = type, minVelocity
        randomSize = 50 if type == 'satellite' else random.randrange(40, 110) if not size else size
        self.mass = randomSize
        self.image = pygame.transform.scale(sprites['asteroids'][len(sprites['asteroids'])-1] if type == 'satellite' else sprites['asteroids'][random.randrange(0, len(sprites['asteroids'])-1)], (randomSize, randomSize))
        self.rect = self.image.get_rect()
        self.pos = [random.randrange(0, options['win_res'][0]), random.randrange(0, options['win_res'][1])] if not pos else pos
        self.velocity = [(random.random()-0.5)*4, (random.random()-0.5)*4] if not velocity else velocity

        self.health = 5 if randomSize > 70 else 3 if randomSize > 40 else 1
        self.maxHealth = self.health
        self.rotateAngle = 0
        self.rotateSpeed = random.randrange(-1, 2, 2)*random.random()*3
        self.spawnTime = 10000
        self.start_time = pygame.time.get_ticks()
        self.rect.x, self.rect.y = self.pos[0], self.pos[1]

    def update(self):
        self.pos[0] += self.velocity[0]
        self.pos[1] += self.velocity[1]

        if self.pos[0] < -100 or self.pos[1] < -100 or self.pos[0] > options['win_res'][0]+50 or self.pos[1] > options['win_res'][1]+50:
            newPos = []

            while True:
                newPos = [
                    random.randrange(-120, options['win_res'][0]+120),
                    random.randrange(-120, options['win_res'][1]+120)
                ]
                if not (newPos[0] > -1*self.rect.width and newPos[0] < options['win_res'][0]+self.rect.width and newPos[1] > -1*self.rect.height and newPos[1] < options['win_res'][1]+self.rect.height):
                    self.velocity = [(random.random()-0.5)*4, (random.random()-0.5)*4]
                    if self.velocity[0] < self.minVelocity and self.velocity[0] > -self.minVelocity:
                        self.velocity[0] += -self.minVelocity if self.velocity[0] < 0 else self.minVelocity
                    if self.velocity[1] < self.minVelocity and self.velocity[1] > -self.minVelocity:
                        self.velocity[1] += -self.minVelocity if self.velocity[1] < 0 else self.minVelocity
                    break

            self.pos = newPos

        if options['particles_enabled']:
            if self.health == 5 and (pygame.time.get_ticks() - self.start_time) % 100 >= 60:
                colorRange = random.randrange(75, 125)
                randomParticleSize = random.randrange(3, 7)
                gvrs['particles'].add(Particle((self.pos[0]+random.randrange(0, self.rect.width), self.pos[1]+random.randrange(0, self.rect.height)), [randomParticleSize, randomParticleSize], (colorRange, colorRange/2, colorRange/2), 0.25, 1))
            elif self.health == 3 and (pygame.time.get_ticks() - self.start_time) % 100 >= 70:
                colorRange = random.randrange(75, 125)
                randomParticleSize = random.randrange(2, 5)
                gvrs['particles'].add(Particle((self.pos[0]+random.randrange(0, self.rect.width), self.pos[1]+random.randrange(0, self.rect.height)), [randomParticleSize, randomParticleSize], (colorRange, colorRange/2, colorRange/2), 0.25, 1))
            elif self.health == 1 and (pygame.time.get_ticks() - self.start_time) % 100 >= 80:
                colorRange = random.randrange(75, 125)
                randomParticleSize = random.randrange(1, 3)
                gvrs['particles'].add(Particle((self.pos[0]+random.randrange(0, self.rect.width), self.pos[1]+random.randrange(0, self.rect.height)), [randomParticleSize, randomParticleSize], (colorRange, colorRange/2, colorRange/2), 0.25, 1))

        self.rotateAngle += self.rotateSpeed
        self.rect.x, self.rect.y = self.pos[0], self.pos[1]

    def die(self):
        self.kill()
        gvrs['player'].score += 1

        soundfx[f'explosion_{random.randrange(1, 11)}'].play()
        gvrs['overlay'].update_text()

        if self.type == 'satellite':
            if options['particles_enabled']:
                for i in range(25):
                    colorRange = random.randrange(150, 255)
                    randomParticleSize = random.randrange(4, 10)
                    gvrs['particles'].add(Particle((self.pos[0]+random.randrange(0, self.rect.width), self.pos[1]+random.randrange(0, self.rect.height)), [randomParticleSize, randomParticleSize], (colorRange, colorRange, colorRange/4), 2, (random.random()+0.1)*2))

                dropChance = random.randrange(0, 100)
        else:
            if options['particles_enabled'] and self.maxHealth == 1:
                for i in range(10):
                    colorRange = random.randrange(75, 255)
                    randomParticleSize = random.randrange(4, 10)
                    gvrs['particles'].add(Particle((self.pos[0]+random.randrange(0, self.rect.width), self.pos[1]+random.randrange(0, self.rect.height)), [randomParticleSize, randomParticleSize], (colorRange, colorRange/3, colorRange/4), 2, (random.random()+0.1)*2))

            elif self.maxHealth == 3:
                for i in range(random.randrange(2, 10)):
                    gvrs['asteroids'].add(Asteroid(pos=[self.pos[0]+random.randrange(0, self.rect.width), self.pos[1]+random.randrange(0, self.rect.height)], size=random.randrange(30, 40)))

                if options['particles_enabled']:
                    for i in range(30):
                        colorRange = random.randrange(75, 255)
                        randomParticleSize = random.randrange(4, 10)
                        gvrs['particles'].add(Particle((self.pos[0]+random.randrange(0, self.rect.width), self.pos[1]+random.randrange(0, self.rect.height)), [randomParticleSize, randomParticleSize], (colorRange, colorRange/3, colorRange/4), 2, (random.random()+0.1)*2))

            elif self.maxHealth == 5:
                for i in range(random.randrange(3, 30)):
                    gvrs['asteroids'].add(Asteroid(pos=[self.pos[0]+random.randrange(0, self.rect.width), self.pos[1]+random.randrange(0, self.rect.height)], size=random.randrange(30, 40)))
                    
                if options['particles_enabled']:
                    for i in range(75):
                        colorRange = random.randrange(75, 255)
                        randomParticleSize = random.randrange(4, 10)
                        gvrs['particles'].add(Particle((self.pos[0]+random.randrange(0, self.rect.width), self.pos[1]+random.randrange(0, self.rect.height)), [randomParticleSize, randomParticleSize], (colorRange, colorRange/3, colorRange/4), 6, (random.random()+0.1)*2))

        del self
        return

    def update_health(self, amnt):
            self.health -= amnt
            if self.health < 1:
                self.die()

    def draw(self):
        rotated_image = pygame.transform.rotate(self.image, self.rotateAngle)
        gvrs['display'].blit(rotated_image, (self.rect.x-(rotated_image.get_rect().width - self.rect.width)/2, self.rect.y-(rotated_image.get_rect().height - self.rect.height)/2))
        
        if self.health != self.maxHealth:
            pygame.draw.rect(gvrs['display'], (0, 0, 0), (self.rect.x, self.rect.y-15, self.rect.width, 5))
            pygame.draw.rect(gvrs['display'], (255, 0, 0), (self.rect.x, self.rect.y-15, self.rect.width*(self.health / self.maxHealth), 5))

class Bullet(pygame.sprite.Sprite):
    def __init__(self, origin, destination, image=None, size=[2, 2], velocity=15, spread=0, damage=1, color=(255, 255, 0), trailColor=(255, 255, 0), particleDensity=10, dieFunc = None, particles=False):
        super().__init__()

        self.image = image if image else pygame.Surface(size)
        if not image:
            pygame.Surface.fill(self.image, color)

        # Initialize instance variables
        self.color, self.trailColor, self.velocity, self.damage, self.dieFunc, self.particles_enabled, self.particleDensity = color, trailColor, velocity, damage, dieFunc, particles, particleDensity

        # Compute variables
        self.rect = self.image.get_rect()
        self.pos = [origin[0], origin[1]]
        self.rect.x, self.rect.y = origin[0], origin[1]
        
        # Calculate direction
        ds2mx = origin[0]-destination[0]
        ds2my = origin[1]-destination[1]
        self.direction = None
        try:
            self.direction = -pygame.math.Vector2([ds2mx, ds2my]).normalize()
        except:
            return

        if spread > 0:
            self.direction.x += random.uniform(-spread, spread)
            self.direction.y += random.uniform(-spread, spread)

        ds2ml = math.sqrt(self.direction.x**2 + self.direction.y**2)
        self.rotateAngle = math.atan2(self.direction.x / ds2ml, self.direction.y / ds2ml) * 57.29578
        self.rotatedImage = pygame.transform.rotate(self.image, self.rotateAngle)
        self.rotatedPosOffset = [(self.rotatedImage.get_rect().width-self.rect.width)/2, (self.rotatedImage.get_rect().height - self.rect.height)/2]

        self.start_time = pygame.time.get_ticks()

    def update(self):
        self.pos[0] += self.velocity * self.direction.x
        self.pos[1] += self.velocity * self.direction.y
        self.rect.x, self.rect.y = self.pos[0]-self.rect.width/2, self.pos[1]-self.rect.height/2

        collided = pygame.sprite.spritecollideany(self, gvrs['asteroids'])
        if collided:
            collided.update_health(self.damage)
            self.kill()
            if self.dieFunc:
                self.dieFunc(self.pos)

            if options['particles_enabled'] and self.particles_enabled:
                for i in range(10):
                    gvrs['particles'].add(Particle(origin=self.pos, color=self.color, velocityRange=0.5, size=[1, 1], duration=random.random()*3+1))

            del self
            return

        # Uncomment this for horrible chaos
        # if self.pos[0] < 0:
        #     self.pos[0] = options['win_res'][0]
        # elif self.pos[0] > options['win_res'][0]:
        #     self.pos[0] = 0
        
        # if self.pos[1] < 0:
        #     self.pos[1] = options['win_res'][1]
        # elif self.pos[1] > options['win_res'][1]:
        #     self.pos[1] = 0

        if self.pos[0] < -120 or self.pos[1] < -120 or self.pos[0] > options['win_res'][0] + 120 or self.pos[1] > options['win_res'][1] + 120:
            self.kill()
            del self
            return

        if options['particles_enabled'] and self.particles_enabled and (pygame.time.get_ticks()) % 100 >= self.particleDensity:
            gvrs['particles'].add(Particle(self.pos, duration=random.uniform(0.15, 0.3), velocityRange=0.5, color=self.trailColor))

    def draw(self):
        gvrs['display'].blit(self.rotatedImage, (self.rect.x-self.rotatedPosOffset[0], self.rect.y-self.rotatedPosOffset[1]))

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = sprites['player_ship']
        self.rect = self.image.get_rect()
        self.pos = [options['win_res'][0] / 2 - 15, options['win_res'][1] / 2 - 15]
        self.rect.x, self.rect.y = self.pos[0], self.pos[1]
        self.velocity = [0, 0]
        self.maxVelocity = 4
        self.rotateAngle = 0
        self.rotated_rect = [0, 0]
        self.start_time = pygame.time.get_ticks()
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
            if options['particles_enabled']:
                gvrs['particles'].add(Particle(gvrs['player'].rect.center, [1, 1], (255, 255, 255), 1))

        self.pos[0] += self.velocity[0]
        self.pos[1] += self.velocity[1]

        if self.pos[0] < -25:
            self.pos[0] = options['win_res'][0]
        elif self.pos[0] > options['win_res'][0]:
            self.pos[0] = -24
        
        if self.pos[1] < -25:
            self.pos[1] = options['win_res'][1]
        elif self.pos[1] > options['win_res'][1]:
            self.pos[1] = -24

        self.rect.x, self.rect.y = self.pos[0], self.pos[1]

        collidedAsteroid = pygame.sprite.spritecollideany(self, gvrs['asteroids'])
        if collidedAsteroid:
            self.collisionTime = pygame.time.get_ticks()
            if pygame.time.get_ticks() - self.hitTime > 500:
                self.health -= 10 if collidedAsteroid.mass > 75 else 5 if collidedAsteroid.mass > 25 else 1
                self.hitTime = pygame.time.get_ticks()

            gvrs['overlay'].update_player_healthbar()
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

    def handle_scroll(self, event):
        self.weaponSelect += -event.y
        self.weaponSelect = 0 if self.weaponSelect+1 > len(self.weapons) else len(self.weapons)-1 if self.weaponSelect < 0 else self.weaponSelect
        self.shootTime = 0
        gvrs['overlay'].update_text()

    def draw(self):
        rotated_image = pygame.transform.rotate(self.image, self.rotateAngle)
        self.rotated_rect = rotated_image.get_rect()
        gvrs['display'].blit(rotated_image, (self.rect.x-(self.rotated_rect.width - self.rect.width)/2, self.rect.y-(self.rotated_rect.height - self.rect.height)/2))

def standard_blaster_shoot(origin, destination):
    gvrs['bullets'].add(Bullet(origin, destination, velocity=15, spread=0, image=sprites['projectile_blaster']))
    soundfx['blaster_shot'].play()

def shotgun_shoot(origin, destination):
    for i in range(7):
        gvrs['bullets'].add(Bullet(origin, [destination[0]+(i-5)*10, destination[1]+(i-5)*10], spread=0.15, image=sprites['projectile_blaster']))
    soundfx['shotgun_shot'].play()

def photon_rifle_shoot(origin, destination):
    gvrs['bullets'].add(Bullet(origin, destination, spread=0, size=[10, 10], velocity=25, damage=100, color=(100, 100, 255), trailColor=(100, 100, 255), image=sprites['projectile_photongun']))
    soundfx['photon_gun_shot'].play()

def automatic_cannon_shoot(origin, destination):
    gvrs['bullets'].add(Bullet(origin, destination, spread=0.15, size=[2, 2], velocity=15, damage=1, color=(255, 100, 100), trailColor=(255, 100, 100), particleDensity=50, image=sprites['projectile_machinegun']))
    soundfx['machine_gun_shot'].play()

def frag_bullet_explosion(origin, velocity = 5, amount = 100):
    for i in range(amount):
        bulletPos = [origin[0]+random.randrange(-amount, amount), origin[1]+random.randrange(-amount, amount)]
        gvrs['bullets'].add(Bullet(origin, bulletPos, velocity=velocity+random.randrange(0, 3), color=gvrs['american_colors'][random.randrange(0, 3)], particleDensity=100))

    if options['particles_enabled']:
        for i in range(150):
            colorRange = random.randrange(75, 255)
            randomParticleSize = random.randrange(5, 15)
            gvrs['particles'].add(Particle((origin[0]+random.randrange(0, 6), origin[1]+random.randrange(0, 6)), [randomParticleSize, randomParticleSize], gvrs['american_colors'][random.randrange(0, 3)], 6, (random.random()+0.1)*2))

    soundfx['frag_cannon_burst'].play()

def frag_cannon_shoot(origin, destination):
    gvrs['bullets'].add(Bullet(origin, destination, spread=0, size=[15, 15], velocity=10, damage=3, color=(255, 255, 255), trailColor=(255, 255, 255), dieFunc=frag_bullet_explosion, image=sprites['projectile_americanpride']))
    soundfx['frag_cannon_shot'].play()