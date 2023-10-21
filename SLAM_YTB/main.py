import env
import sensors
import robot_drive
import pygame
import Particle_filter

environment = env.buildEnvironment((600, 1200))
environment.originalMap = environment.map.copy()
laser = sensors.Laserensor(100, environment.originalMap, uncertainty=(0.5, 0.01))
robot = robot_drive.Robot([200, 200], 10)
environment.map.fill((0,0,0))
environment.infomap = environment.map.copy()
running = True

dt = 0
lasttime = pygame.time.get_ticks()

while running:
    dt = (pygame.time.get_ticks()-lasttime) / 1000
    sensorON = True
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            robot.control(event, dt)

        if sensorON:
            position = [robot.x, robot.y]
            laser.position = position
            sensor_data = laser.sense_obstacles()
            environment.dataStorage(sensor_data, position)
            environment.show_sensorData()
        environment.map.blit(environment.infomap, (0,0))
        pygame.display.update()



# mouse input
# while running:
#     sensorON = False
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#         if pygame.mouse.get_focused():
#             sensorON = True
#         elif not pygame.mouse.get_focused():
#             sensorON = False

#         if sensorON:
#             position = pygame.mouse.get_pos()
#             laser.position = position
#             sensor_data = laser.sense_obstacles()
#             environment.dataStorage(sensor_data) #error
#             environment.show_sensorData()
#         environment.map.blit(environment.infomap, (0,0))
#         pygame.display.update()