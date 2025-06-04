import pygame
import pygame_gui
from camera import Camera

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 120

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
        time_delta = clock.tick(FPS)/1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == quit_button:
                    running = False
                elif event.ui_element == settings_button:
                    settings_menu()
                elif event.ui_element == start_button:
                    the_game()

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
        time_delta = clock.tick(FPS)/1000.0
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

def the_game():
    mouse_tracking = False
    mouse_previous_pos = (0, 0)

    main_loop = True
    main_screen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    main_manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT))

    game_map = pygame.image.load('images\\map.png')
    camera = Camera(game_map.size, (SCREEN_WIDTH, SCREEN_HEIGHT))
    
    while main_loop:
        time_delta = clock.tick(FPS)/1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                main_loop = False
            elif event.type == pygame_gui.UI_BUTTON_PRESSED:
                pass
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_tracking = True
                mouse_previous_pos = pygame.mouse.get_pos()
            elif event.type == pygame.MOUSEMOTION:
                if mouse_tracking:
                    camera.position = (camera.position[0] - (pygame.mouse.get_pos()[0] - mouse_previous_pos[0]) / camera.scaling_factor, camera.position[1] - (pygame.mouse.get_pos()[1] - mouse_previous_pos[1]) / camera.scaling_factor)
                    mouse_previous_pos = pygame.mouse.get_pos()
            elif event.type == pygame.MOUSEBUTTONUP:
                if mouse_tracking:
                    mouse_tracking = False
            elif event.type == pygame.MOUSEWHEEL:
                if event.y == 1:
                    camera.scaling_factor += camera.scaling_step
                if event.y == -1:
                    camera.scaling_factor -= camera.scaling_step

            main_manager.process_events(event)
        main_manager.update(time_delta)
        main_manager.draw_ui(main_screen)

        main_screen.fill((0, 0, 0))

        main_screen.blit(pygame.transform.scale_by(game_map, camera.scaling_factor), camera.return_render_coords())

        screen.blit(main_screen, (0, 0))
        pygame.display.update()



        

start_menu()


pygame.quit()
