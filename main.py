import pygame
import pygame_gui

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
running = True

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("The game")
clock = pygame.time.Clock()


def start_menu():
    start_screen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    running = True
    start_manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT))
    start_container = pygame_gui.elements.ui_auto_resizing_container.UIAutoResizingContainer(pygame.Rect(10, 10, 50, 50), manager=start_manager, anchors={'centerx': 'centerx', 'centery': 'centery'})
    start_button = pygame_gui.elements.ui_button.UIButton(pygame.Rect(0, 0, -1, -1), manager=start_manager, container=start_container, anchors={'centerx': 'centerx'}, text='НАЧАТЬ ИГРУ')
    settings_button = pygame_gui.elements.ui_button.UIButton(pygame.Rect(0, 1, -1, -1), manager=start_manager, container=start_container, anchors={'centerx': 'centerx', 'top_target': start_button}, text='НАСТРОЙКИ')
    quit_button = pygame_gui.elements.ui_button.UIButton(pygame.Rect(0, 1, -1, -1), manager=start_manager, container=start_container, anchors={'centerx': 'centerx', 'top_target': settings_button}, text='ВЫЙТИ')

    while running:
        time_delta = clock.tick(60)/1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == quit_button:
                    running = False
                elif event.ui_element == settings_button:
                    settings_menu()

            start_manager.process_events(event)

        start_manager.update(time_delta)
        start_manager.draw_ui(start_screen)


        screen.blit(start_screen, (0, 0))
        pygame.display.update()


def settings_menu():
    setting_screen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    running_settings = True
    settings_manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT))
    setting_container = pygame_gui.elements.ui_auto_resizing_container.UIAutoResizingContainer(pygame.Rect(0, 0, 50, 50), manager=settings_manager, anchors={'centerx': 'centerx', 'centery': 'centery'})
    exit_button = pygame_gui.elements.ui_button.UIButton(pygame.Rect(0, 1, -1, -1), manager=settings_manager, container=setting_container, anchors={'centerx': 'centerx'}, text='ВЫЙТИ')
    while running_settings:
        time_delta = clock.tick(60)/1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running_settings = False
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == exit_button:
                    running_settings = False

            settings_manager.process_events(event)

        settings_manager.update(time_delta)
        settings_manager.draw_ui(setting_screen)


        screen.blit(setting_screen, (0, 0))
        pygame.display.update()

def start_game():
    

        

start_menu()


pygame.quit()
