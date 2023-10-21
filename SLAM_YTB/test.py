import pygame
import math

pygame.init()
# Set up the screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Set up the robot dimensions and position
ROBOT_WIDTH = 50
ROBOT_HEIGHT = 50
robot_x = SCREEN_WIDTH // 2 - ROBOT_WIDTH // 2
robot_y = SCREEN_HEIGHT // 2 - ROBOT_HEIGHT // 2

# Set up the robot speed and direction
robot_speed = 0
robot_direction = 0

# Set up the clock
clock = pygame.time.Clock()

# Define the robot drawing function
def draw_robot(x, y, angle):
    # Define the dimensions of the robot drawing
    robot_width = 50
    robot_height = 50
    body_width = 40
    body_height = 30
    wheel_radius = 10

    # Calculate the position of the front wheel based on the angle of the robot
    wheel_x = x + body_width / 2 * math.cos(math.radians(angle))
    wheel_y = y - body_width / 2 * math.sin(math.radians(angle))

    # Draw the body of the robot
    pygame.draw.rect(screen, (0, 0, 255), pygame.Rect(x, y - body_height / 2, body_width, body_height))

    # Draw the front wheel of the robot
    pygame.draw.circle(screen, (255, 255, 255), (int(wheel_x), int(wheel_y)), wheel_radius)

    # Draw the rear wheels of the robot
    pygame.draw.circle(screen, (255, 0, 255), (int(x + wheel_radius), int(y + body_height / 2 - wheel_radius)), wheel_radius)
    pygame.draw.circle(screen, (255, 0, 255), (int(x + body_width - wheel_radius), int(y + body_height / 2 - wheel_radius)), wheel_radius)

# Define the main game loop
running = True
while running:

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                robot_speed = 2
            elif event.key == pygame.K_DOWN:
                robot_speed = -2

            elif event.key == pygame.K_LEFT:

                robot_direction += 20

            elif event.key == pygame.K_RIGHT:

                robot_direction -= 20

        elif event.type != pygame.KEYDOWN:
            robot_speed = 0

    # Update the robot's position based on its speed and direction
    robot_x += robot_speed * math.cos(math.radians(robot_direction))
    robot_y -= robot_speed * math.sin(math.radians(robot_direction))

    # Clear the screen and draw the robot
    screen.fill((0, 0, 0))
    draw_robot(robot_x, robot_y, robot_direction)

    # Update the screen
    pygame.display.flip()

    # Set the frame rate
    clock.tick(60)

# Clean up Pygame
pygame.quit()
