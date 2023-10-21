import pygame
import math

class Robot:
    def __init__(self, startpos, width):
        self.m2p = 3779.52
        
        # robot dims
        self.w = width
        self.x = startpos[0]
        self.y = startpos[1]
        self.theta = 0
        self.vl = 0.01 * self.m2p
        self.vr = 0.01 * self.m2p
        self.maxspeed = 0.02 * self.m2p
        self.minspeed = 0.02 * self.m2p


    def draw_robot(self, screen):
    # Define the dimensions of the robot drawing
        body_width = 40

        wheel_radius = 5
        x = self.x
        y = self.y
        angle = self.theta

        # Calculate the position of the front wheel based on the angle of the robot
        wheel_x = x + body_width / 2 * math.cos(math.radians(angle))
        wheel_y = y - body_width / 2 * math.sin(math.radians(angle))

        # Draw the front wheel of the robot
        pygame.draw.circle(screen, (0, 0, 255), (int(wheel_x), int(wheel_y)), wheel_radius)

    def control(self, event, dt):

        if event.key == pygame.K_UP:
            self.vl = 10
            self.vr = 10
        elif event.key == pygame.K_DOWN:
            self.vl = -2
            self.vr = -2
        elif event.key == pygame.K_LEFT:
            self.theta += 1
        elif event.key == pygame.K_RIGHT:
            self.theta -= 1

        self.x += ((self.vl + self.vr) / 2) * math.cos(self.theta)
        self.y -= ((self.vl + self.vr) / 2) * math.sin(self.theta)
        self.theta += (self.vr - self.vl) / self.w * dt
        





