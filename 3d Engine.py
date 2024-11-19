import pygame
from pygame.locals import *
from math import *
from random import randint

SCREEN_SIZE = (640, 480)
CUBE_SIZE = 300

class Vector3:
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other):
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, scalar):
        return Vector3(self.x * scalar, self.y * scalar, self.z * scalar)

    def get_magnitude(self):
        return sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

    def __repr__(self):
        return f"Vector3({self.x:.2f}, {self.y:.2f}, {self.z:.2f})"

def calculate_viewing_distance(fov, screen_width):
    return (screen_width / 2.0) / tan(fov / 2.0)

def run():
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE, 0)
    default_font = pygame.font.get_default_font()
    font = pygame.font.SysFont(default_font, 24)
    ball = pygame.Surface((10, 10), pygame.SRCALPHA)
    pygame.draw.circle(ball, (255, 255, 255), (5, 5), 5)

    points = []
    fov = 90.0  # Field of view
    viewing_distance = calculate_viewing_distance(radians(fov), SCREEN_SIZE[0])

    # Generate cube edge points
    for x in range(0, CUBE_SIZE + 1, 20):
        edge_x = x == 0 or x == CUBE_SIZE
        for y in range(0, CUBE_SIZE + 1, 20):
            edge_y = y == 0 or y == CUBE_SIZE
            for z in range(0, CUBE_SIZE + 1, 20):
                edge_z = z == 0 or z == CUBE_SIZE
                if sum((edge_x, edge_y, edge_z)) >= 2:
                    points.append(Vector3(
                        x - CUBE_SIZE / 2, 
                        y - CUBE_SIZE / 2, 
                        z - CUBE_SIZE / 2))

    points.sort(key=lambda point: point.z, reverse=True)
    center_x, center_y = SCREEN_SIZE[0] / 2, SCREEN_SIZE[1] / 2
    ball_w, ball_h = ball.get_size()
    ball_center_x, ball_center_y = ball_w / 2, ball_h / 2

    camera_position = Vector3(0.0, 0.0, -700.0)
    camera_speed = 300.0
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                return

        screen.fill((0, 0, 0))
        pressed_keys = pygame.key.get_pressed()
        time_passed = clock.tick(60)  # Cap at 60 FPS
        time_passed_seconds = time_passed / 1000.0

        direction = Vector3()
        if pressed_keys[K_LEFT]:
            direction.x = -1.0
        if pressed_keys[K_RIGHT]:
            direction.x = 1.0
        if pressed_keys[K_UP]:
            direction.y = 1.0
        if pressed_keys[K_DOWN]:
            direction.y = -1.0
        if pressed_keys[K_q]:
            direction.z = 1.0
        if pressed_keys[K_a]:
            direction.z = -1.0

        if pressed_keys[K_w]:
            fov = min(179.0, fov + 1.0)
            viewing_distance = calculate_viewing_distance(radians(fov), SCREEN_SIZE[0])
        if pressed_keys[K_s]:
            fov = max(1.0, fov - 1.0)
            viewing_distance = calculate_viewing_distance(radians(fov), SCREEN_SIZE[0])

        camera_position += direction * camera_speed * time_passed_seconds

        for point in points:
            relative_point = point - camera_position
            if relative_point.z > 20.0:
                x = relative_point.x * viewing_distance / relative_point.z
                y = -relative_point.y * viewing_distance / relative_point.z
                x += center_x
                y += center_y
                screen.blit(ball, (x - ball_center_x, y - ball_center_y))

        # Display debug info
        white = (255, 255, 255)
        cam_text = font.render(f"Camera = {camera_position}", True, white)
        screen.blit(cam_text, (5, 5))
        fov_text = font.render(f"FOV = {int(fov)}", True, white)
        screen.blit(fov_text, (5, 35))
        d_text = font.render(f"Viewing Distance = {viewing_distance:.3f}", True, white)
        screen.blit(d_text, (5, 65))

        pygame.display.update()

if __name__ == "__main__":
    run()
