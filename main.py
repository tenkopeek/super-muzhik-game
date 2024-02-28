import pygame

from lib.dash import Dashboard
from lib.menu import Menu
from lib.level import Level
from lib.sound import Sound
from lib.entities.Player import Player

windowSize = 640, 480


def main():
    pygame.mixer.pre_init(44100, -16, 2, 4096)
    pygame.init()
    screen = pygame.display.set_mode(windowSize)
    max_frame_rate = 60
    dashboard = Dashboard("assets/images/font.png", 8, screen)
    sound = Sound()
    level = Level(screen, sound, dashboard)
    menu = Menu(screen, dashboard, level, sound)

    while not menu.start:
        menu.update()

    player = Player(0, 0, level, screen, dashboard, sound)
    clock = pygame.time.Clock()

    while not player.restart:
        pygame.display.set_caption("Super Muzhik running with {:d} FPS".format(int(clock.get_fps())))
        if player.pause:
            player.pauseObj.update()
        else:
            level.drawLevel(player.camera)
            dashboard.update()
            player.update()
        pygame.display.update()
        clock.tick(max_frame_rate)
    return 'restart'


if __name__ == "__main__":
    exitmessage = 'restart'
    while exitmessage == 'restart':
        exitmessage = main()
