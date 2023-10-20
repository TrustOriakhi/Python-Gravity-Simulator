import pygame
import math

# Constants
WIDTH, HEIGHT = 800, 600
G = 10
FPS = 60
PLANET_SIZE = 50
OBJ_SIZE = 5
VEL_SCALE = 100

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Initialize pygame
pygame.init()
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Gravitational Slingshot Simulation')

# Load images
BG = pygame.transform.scale(pygame.image.load('background.jpg'), (WIDTH, HEIGHT))
planet = pygame.transform.scale(pygame.image.load('jupiter.png'), (PLANET_SIZE * 2, PLANET_SIZE * 2))

class Planet:
    def __init__(self, x, y, mass):
        self.x = x
        self.y = y
        self.mass = mass

    def draw(self):
        win.blit(planet, (int(self.x - PLANET_SIZE), int(self.y - PLANET_SIZE)))

class Spacecraft:
    def __init__(self, x, y, vel_x, vel_y, mass):
        self.x = x
        self.y = y
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.mass = mass

    def move(self, planet):
        distance = math.sqrt((self.x - planet.x) ** 2 + (self.y - planet.y) ** 2)
        force = (G * self.mass * planet.mass) / (distance ** 2)
        acceleration = force / self.mass
        angle = math.atan2(planet.y - self.y, planet.x - self.x)
        acceleration_x = acceleration * math.cos(angle)
        acceleration_y = acceleration * math.sin(angle)
        self.vel_x += acceleration_x
        self.vel_y += acceleration_y
        self.x += self.vel_x
        self.y += self.vel_y

    def draw(self):
        pygame.draw.circle(win, RED, (int(self.x), int(self.y)), OBJ_SIZE)

def create_ship(location, mouse, mass):
    t_x, t_y = location
    m_x, m_y = mouse

    vel_x = (m_x - t_x) / VEL_SCALE
    vel_y = (m_y - t_y) / VEL_SCALE
    obj = Spacecraft(t_x, t_y, vel_x, vel_y, mass)
    return obj

def draw_slider(win, x, y, width, value, min_val, max_val, label):
    # Draw the slider track
    pygame.draw.rect(win, (255, 255, 255), (x, y, width, 10))
    
    # Calculate the position of the slider handle
    slider_handle_x = int(x + (value - min_val) / (max_val - min_val) * width)
    
    # Draw the slider handle
    pygame.draw.rect(win, (255, 0, 0), (slider_handle_x, y - 5, 10, 20))
    
    # Draw the label
    font = pygame.font.Font(None, 36)
    text = font.render(label, True, (255, 255, 255))
    win.blit(text, (x, y - 40))

def main():
    running = True
    clock = pygame.time.Clock()

    spacecraft_mass = 5
    planet_mass = 100

    planet = Planet(WIDTH // 2, HEIGHT // 2, planet_mass)
    objects = []
    temp_obj_pos = None
    
    if temp_obj_pos:
        pygame.draw.circle(win, RED, temp_obj_pos, OBJ_SIZE)
        pygame.draw.line(win, WHITE, temp_obj_pos, mouse_pos, 2)

    # Slider parameters
    slider_x = 10
    slider_width = 200
    slider_min = 1
    slider_max = 500
    spacecraft_mass_input = spacecraft_mass

    slider_planet_x = 10
    slider_planet_width = 200
    slider_planet_min = 1
    slider_planet_max = 1000
    planet_mass_input = planet_mass

    slider_dragging_spacecraft = False
    slider_dragging_planet = False

    while running:
        clock.tick(FPS)

        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if (slider_x <= mouse_pos[0] <= slider_x + slider_width) and (10 <= mouse_pos[1] <= 30):
                    slider_dragging_spacecraft = True
                elif (slider_planet_x <= mouse_pos[0] <= slider_planet_x + slider_planet_width) and (10 <= mouse_pos[1] <= 30):
                    slider_dragging_planet = True
            elif event.type == pygame.MOUSEBUTTONUP:
                slider_dragging_spacecraft = False
                slider_dragging_planet = False

        if slider_dragging_spacecraft:
            spacecraft_mass_input = max(slider_min, min(slider_max, (mouse_pos[0] - slider_x) / slider_width * (slider_max - slider_min)))
            spacecraft_mass = spacecraft_mass_input

        if slider_dragging_planet:
            planet_mass_input = max(slider_planet_min, min(slider_planet_max, (mouse_pos[0] - slider_planet_x) / slider_planet_width * (slider_planet_max - slider_planet_min)))
            planet_mass = planet_mass_input

        win.blit(BG, (0, 0))

        draw_slider(win, slider_x, 10, slider_width, spacecraft_mass_input, slider_min, slider_max, "Spacecraft Mass")
        draw_slider(win, slider_planet_x, 50, slider_planet_width, planet_mass_input, slider_planet_min, slider_planet_max, "Planet Mass")

        if temp_obj_pos:
            pygame.draw.circle(win, RED, temp_obj_pos, OBJ_SIZE)
            pygame.draw.line(win, WHITE, temp_obj_pos, mouse_pos, 2)

        for obj in objects:
            obj.draw()
            obj.move(planet)
            off_screen = (
                obj.x < 0 or obj.x > WIDTH or obj.y < 0 or obj.y > HEIGHT
            )
            collided = (
                math.sqrt((obj.x - planet.x) ** 2 + (obj.y - planet.y) ** 2)
                <= PLANET_SIZE
            )
            if off_screen or collided:
                objects.remove(obj)

        planet.mass = planet_mass
        planet.draw()

        pygame.display.update()

    pygame.quit()

if __name__ == '__main__':
    main()
