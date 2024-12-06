import pygame
import math
import os
from win32con import ENUM_CURRENT_SETTINGS
from win32api import EnumDisplaySettings


os.chdir(os.path.dirname(os.path.abspath(__file__)))  # sets the current directory to the file's directory # noqa


class Engine:

    win_aspect_ratio = 10/14
    window_height = 720
    wh = window_height
    window_width = int(window_height * win_aspect_ratio)
    window_size = (window_width, window_height)

    def set_up():

        dev_mode = EnumDisplaySettings(None, ENUM_CURRENT_SETTINGS)  # get the OS's fps setting
        fps_config = "system"
        if fps_config == "system":  # you can specify the fps you want or just leave the native framerate
            Engine.fps = dev_mode.DisplayFrequency
        else:
            Engine.fps = int(fps_config)
        Engine.fps_relation = (144/Engine.fps)  # this is used to keep the proportion and timings i designed for the game whatever the frame rate is

        Engine.timer = pygame.time.Clock()

        Engine.screen = pygame.display.set_mode(Engine.window_size)

        pygame.display.set_caption("Bouncy Broda")

        pygame.display.set_icon(pygame.image.load("media\\icon.png").convert_alpha())  # sets window icon

        Engine.font1 = pygame.font.SysFont("Times New Roman", Engine.wh//38)
        Engine.font2 = pygame.font.SysFont("Times New Roman", Engine.wh//46)


class Platform:

    def __init__(self, x, y, length, thickness, color):
        self.x = x
        self.y = y
        self.length = length
        self.thickness = thickness
        self.color = color

    def draw(self):
        pygame.draw.line(Engine.screen, self.color, (self.x, self.y), (self.x+self.length, self.y), width=self.thickness)

    def check_collision(self, circle_center, circle_radius):  # colision between line and a circle.

        if circle_center[0] + circle_radius < self.x or self.x + self.length < circle_center[0] - circle_radius:  # if the circle is not within the platform's x-range, it can't collide
            return False  # quick return

        # (CHATGPTED)
        # Platform endpoints
        line_start = (self.x, self.y)
        line_end = (self.x + self.length, self.y)
        # Circle center
        cx, cy = circle_center
        # Vector math: line equation components
        lx1, ly1 = line_start
        lx2, ly2 = line_end
        # Line segment vector and circle-to-line-start vector
        line_vec = (lx2 - lx1, ly2 - ly1)
        start_to_circle_vec = (cx - lx1, cy - ly1)
        # Project circle's center onto the line
        line_length_sq = line_vec[0]**2 + line_vec[1]**2
        if line_length_sq == 0:  # Handle degenerate (point-like) line
            return math.hypot(cx - lx1, cy - ly1) <= circle_radius
        t = max(0, min(1, (start_to_circle_vec[0] * line_vec[0] + start_to_circle_vec[1] * line_vec[1]) / line_length_sq))
        nearest_point = (lx1 + t * line_vec[0], ly1 + t * line_vec[1])
        # Distance from the circle's center to the nearest point on the line
        distance_to_circle = math.hypot(nearest_point[0] - cx, nearest_point[1] - cy)
        # Check collision
        return distance_to_circle <= circle_radius


class Ball:

    def __init__(self, vel, radius, color) -> None:

        self.x = Engine.window_width // 2
        self.y = Engine.window_height // 2
        self.vel = vel
        self.radius = radius
        self.color = color
        self.active_boost = False

    def draw(self):
        if self.active_boost:
            color = (self.color[0]+40, self.color[1]-15, self.color[2]-50)  # something like yellow when boost is on
        else:
            color = self.color

        pygame.draw.circle(Engine.screen, color, (self.x, self.y), self.radius)

    def boost(self, timer):
        self.active_boost = True
        self.boost_timer = timer


class UI:

    def __init__(self):

        UI.rect_surface = pygame.Surface((Engine.window_width, Engine.window_height//70), pygame.SRCALPHA)
        UI.rect_surface.fill((255, 0, 0, 40))
