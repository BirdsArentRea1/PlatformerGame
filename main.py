import pygame


pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("OOP Platformer Base Code")

clock = pygame.time.Clock()
GRAVITY = 0.5

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 100, 255)
GREEN = (0, 200, 0)

#-class platform----------------------------------------------------------------------------------------------
class Platform:
    
    def __init__(self, x, y, w, h): #constructor
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def draw(self, surface): #draw function
        pygame.draw.rect(surface, GREEN, (self.x, self.y, self.w, self.h))
        

#-class player----------------------------------------------------------------------------------------------
class Player:
    
    def __init__(self, x, y): #constructor
        self.x = x
        self.y = y
        self.w = 40
        self.h = 60
        self.vy = 0
        self.on_ground = False

    def handle_input(self, keys): #keyboard input
        if keys[pygame.K_RIGHT]:
            self.x += 5
        if keys[pygame.K_SPACE] and self.on_ground:
            self.vy = -12
            self.on_ground = False

    def apply_gravity(self): #make player fall
        self.vy += GRAVITY
        self.y += self.vy

    def check_collision(self, platforms): 
        self.on_ground = False #assume we're in the air, change if not
        for plat in platforms: #check all the platforms in the list
            if self.is_colliding(plat): #if we ARE colliding, reset feet to top of platform...
                if self.y + self.h <= plat.y + self.vy:
                    self.y = plat.y - self.h
                    self.vy = 0
                    self.on_ground = True

    def is_colliding(self, plat): #bounding box collision
        if self.x + self.w > plat.x and self.x < plat.x + plat.w and self.y + self.h > plat.y and self.y < plat.y + plat.h:
            return True
        else:
            return False
        

    def update(self, platforms): #funtion that calls a bunch of other functions (keeps game loop more simple)
        self.apply_gravity()
        self.check_collision(platforms)

    def draw(self, surface):
        pygame.draw.rect(surface, BLUE, (self.x, self.y, self.w, self.h))

#-end of classes----------------------------------------------------------------------------------------------

#list to contain platforms
platforms = [
    Platform(100, 500, 600, 20), #calling platform class constructor
    Platform(300, 400, 100, 10),
    Platform(500, 300, 100, 10)
]

player = Player(100, 100) #calling player class constructor


running = True
while running: #GAME LOOP############################################################################
    
    #input section-------------------
    clock.tick(60)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    player.handle_input(keys)
    
    #update/physics section-----------
    player.update(platforms)

    #render section-------------------
    screen.fill(WHITE)
    
    for plat in platforms:
        plat.draw(screen)

    player.draw(screen)

    pygame.display.flip()
    
#END OF GAME LOOP############################################################################

pygame.quit()
