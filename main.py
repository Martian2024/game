import pygame
import pygame_gui
from camera import Camera
from sprites import SimpleHouse, Tree, RifleMan, MouseSprite, BaseEnemy, Shield, Boss
import random
from math import sqrt


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 120

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("The game")
clock = pygame.time.Clock()

def generate_map_backgound(tiles, tile_size):
    game_map = pygame.Surface((tile_size * tiles, tile_size * tiles))
    game_map.set_colorkey((0, 0, 0))
    pygame.draw.rect(game_map, '#39FF14', (0, 0, tile_size * tiles, tile_size * tiles), width=7)
    for i in range(1, tiles):
        pygame.draw.line(game_map, '#39FF14', (0, tile_size * i), (tile_size * tiles, tile_size * i))
    for i in range(1, tiles):
        pygame.draw.line(game_map, '#39FF14', (tile_size * i, 0), (tile_size * i, tile_size * tiles))
    return game_map

def check_visibility(a, b):
        x = a.rect.center[0] - b.rect.center[0]
        y = a.rect.center[0] - b.rect.center[0]
        print(a, b, sqrt(x ** 2 + y ** 2))
        return sqrt(x ** 2 + y ** 2) < a.vision



def start_menu():
    start_screen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    running = True
    start_manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT))
    start_container = pygame_gui.elements.ui_auto_resizing_container.UIAutoResizingContainer(pygame.Rect(10, 10, 50, 50), manager=start_manager, anchors={'centerx': 'centerx', 'centery': 'centery'})
    start_button = pygame_gui.elements.ui_button.UIButton(pygame.Rect(0, 0, -1, -1), manager=start_manager, container=start_container, anchors={'centerx': 'centerx'}, text='НАЧАТЬ ИГРУ')
    settings_button = pygame_gui.elements.ui_button.UIButton(pygame.Rect(0, 1, -1, -1), manager=start_manager, container=start_container, anchors={'centerx': 'centerx', 'top_target': start_button}, text='НАСТРОЙКИ')
    quit_button = pygame_gui.elements.ui_button.UIButton(pygame.Rect(0, 1, -1, -1), manager=start_manager, container=start_container, anchors={'centerx': 'centerx', 'top_target': settings_button}, text='ВЫЙТИ')

    tiles = 15
    tile_size = 200
    game_map = generate_map_backgound(tiles, tile_size)
    houses = pygame.sprite.Group()
    trees = pygame.sprite.Group()
    houses_list = [[(100, 50), (200, 75), houses], 
                   [(-80, 70), (80, 120), houses],
                   [(-180, 80), (90, 90), houses], 
                   [(-70, -100), (75, 100), houses],
                   [(-170, -100), (50, 50), houses], 
                   [(120, -75), (50, 50), houses],
                   [(95, -120), (100, 50), houses],
                   [(250, -70), (100, 50), houses],
                   [(330, 70), (75, 50), houses],
                   [(330, 300), (50, 75), houses],
                   [(75, 250), (75, 150), houses],
                   [(185, 210), (150, 75), houses],]
    for i in range(len(houses_list)):
        SimpleHouse(*houses_list[i])
    for i in range(random.randint(1, 1000)):
        Tree((random.randint(-1 * (tiles * tile_size) // 2, (tiles * tile_size) // 2), random.randint(-1 * (tiles * tile_size) // 2, (tiles * tile_size) // 2)), 50, trees)

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
                    result = the_game()
                    running = False
                    

            start_manager.process_events(event)


        for i in houses:
            start_screen.blit(i.image, (SCREEN_WIDTH // 2 - (i.rect.center[0]) - i.rect.size[0] // 2,SCREEN_HEIGHT // 2 - (i.rect.center[1]) - i.rect.size[1] // 2))

        for i in trees:
            start_screen.blit(i.image, (SCREEN_WIDTH // 2 - (i.rect.center[0]) - i.rect.size[0] // 2, SCREEN_HEIGHT // 2 - (i.rect.center[1]) - i.rect.size[1] // 2))

        start_screen.blit(game_map, (-1 * SCREEN_WIDTH // 2, -1 * SCREEN_HEIGHT // 2))

        start_manager.update(time_delta)
        start_manager.draw_ui(start_screen)

        screen.blit(start_screen, (0, 0))
        pygame.display.update()

    end_game(result)

def end_game(result):
    end_manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT))
    end_container = pygame_gui.elements.ui_auto_resizing_container.UIAutoResizingContainer(pygame.Rect(10, 10, 50, 50), manager=end_manager, anchors={'centerx': 'centerx', 'centery': 'centery'})
    quit_button = pygame_gui.elements.ui_button.UIButton(pygame.Rect(0, 1, -1, -1), manager=end_manager, container=end_container, anchors={'centerx': 'centerx', 'centery': 'centery'}, text='ВЫЙТИ')
    in_this_menu = True
    while in_this_menu:
        time_delta = clock.tick(FPS)/1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                in_this_menu = False
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == quit_button:
                    in_this_menu = False

            end_manager.process_events(event)

        screen.fill((0, 0, 0))
        pygame.font.init()
        my_font = pygame.font.SysFont('Comic Sans MS', 30)
        text_surface = my_font.render('You Won!' if result else 'You Lost!', False, (0, 255, 0))
        end_manager.update(time_delta)
        end_manager.draw_ui(screen)
        screen.blit(text_surface, ((SCREEN_WIDTH - text_surface.get_rect()[2])  // 2, (SCREEN_HEIGHT - text_surface.get_rect()[3])  // 3))
        # print(SCREEN_WIDTH, SCREEN_HEIGHT)
        # print(text_surface.get_rect()[2], (SCREEN_HEIGHT - text_surface.get_rect()[1])  // 2)
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

    main_loop = True
    main_screen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    main_manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT))
    mouse_sprite = MouseSprite()
    selected_sprite = []


    # game_map = pygame.image.load('images\\map.png')
    tiles = 15
    tile_size = 200
    game_map = generate_map_backgound(tiles, tile_size)
    fog_of_war = pygame.Surface(game_map.size)
    fog_of_war.set_colorkey((255, 255, 255))
    houses = pygame.sprite.Group()
    trees = pygame.sprite.Group()
    houses_list = [[(100, 50), (200, 75), houses], 
                   [(-80, 70), (80, 120), houses],
                   [(-180, 80), (90, 90), houses], 
                   [(-70, -100), (75, 100), houses],
                   [(-170, -100), (50, 50), houses], 
                   [(120, -75), (50, 50), houses],
                   [(95, -120), (100, 50), houses],
                   [(250, -70), (100, 50), houses],
                   [(330, 70), (75, 50), houses],
                   [(330, 300), (50, 75), houses],
                   [(75, 250), (75, 150), houses],
                   [(185, 210), (150, 75), houses],]
    for i in range(len(houses_list)):
        SimpleHouse(*houses_list[i])
    for i in range(random.randint(1, 1000)):
        Tree((random.randint(-1 * (tiles * tile_size) // 2 + 20, (tiles * tile_size) // 2 - 20), random.randint(-1 * (tiles * tile_size) // 2 + 20, (tiles * tile_size) // 2 - 20)), 50, trees)
    #houses = pygame.sprite.Group([SimpleHouse((random.randint(1, SCREEN_WIDTH), random.randint(1, SCREEN_HEIGHT)), (random.randint(25, 100), random.randint(25, 100))) for i in range(random.randint(1, 10))])
    crew = pygame.sprite.Group()
    rifleman = RifleMan((0, tile_size * (tiles // 2 - 1) + 50), crew)
    rifleman2 = RifleMan((-50, tile_size * (tiles // 2 - 1) + 50), crew)
    shield = Shield((0, tile_size * (tiles // 2 - 1)), crew)
    enemies = pygame.sprite.Group()
    boss = Boss((0, 0), enemies)

    camera = Camera(game_map.size, (SCREEN_WIDTH, SCREEN_HEIGHT), (0, tile_size * (tiles // 2 - 1)))

    while main_loop:
        time_delta = clock.tick(FPS)/1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                main_loop = False
            elif event.type == pygame_gui.UI_BUTTON_PRESSED:
                pass
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if selected_sprite:
                        if selected_sprite[0].selected:
                            selected_sprite[0].selected = False
                        else:
                            selected_sprite[0].selected = True
                    mouse_sprite.rect.center = (camera.position[0] + (pygame.mouse.get_pos()[0] - camera.screen_size[0] // 2) / camera.scaling_factor, camera.position[1] + (pygame.mouse.get_pos()[1] - camera.screen_size[1] // 2) / camera.scaling_factor)
                    selected_sprite = pygame.sprite.spritecollide(mouse_sprite, crew, dokill=False)
                    if selected_sprite:
                        if selected_sprite[0].selected:
                            selected_sprite[0].selected = False
                        else:
                            selected_sprite[0].selected = True
                        #selected_sprite[0].update()
                elif event.button == 2:
                    mouse_tracking = True
                    mouse_previous_pos = pygame.mouse.get_pos()
                elif event.button == 3:
                    if selected_sprite:
                        x = camera.position[0] + (pygame.mouse.get_pos()[0] - camera.screen_size[0] // 2) / camera.scaling_factor
                        y = camera.position[1] + (pygame.mouse.get_pos()[1] - camera.screen_size[1] // 2) / camera.scaling_factor
                        if -1 * camera.map_size[0] // 2 < x < camera.map_size[0] // 2 and -1 * camera.map_size[0] // 2 < y < camera.map_size[1] // 2:
                            mouse_sprite.rect.center = (camera.position[0] + (pygame.mouse.get_pos()[0] - camera.screen_size[0] // 2) / camera.scaling_factor, camera.position[1] + (pygame.mouse.get_pos()[1] - camera.screen_size[1] // 2) / camera.scaling_factor)
                            clicked_enemies = pygame.sprite.spritecollide(mouse_sprite, enemies, dokill=False)
                            if clicked_enemies:
                                selected_sprite[0].target = clicked_enemies[0]
                                selected_sprite[0].autoattack = False
                            else:
                                selected_sprite[0].autoattack = True
                                intersects = False
                                for i in houses:
                                    if i.rect.clipline(selected_sprite[0].position, (x, y)):
                                        intersects = True
                                if not intersects:
                                    selected_sprite[0].order = 'MOTION'
                                    selected_sprite[0].destination = (x, y)
                        # x = camera.position[0] + (pygame.mouse.get_pos()[0] - camera.screen_size[0] // 2) / camera.scaling_factor - selected_sprite[0].rect.center[0]
                        # y = camera.position[1] + (pygame.mouse.get_pos()[1] - camera.screen_size[1] // 2) / camera.scaling_factor - selected_sprite[0].rect.center[1]
                        # length = sqrt(x ** 2 + y ** 2)
                        # print(x / length, y / length)
                        # selected_sprite[0].motionvector = (x * (selected_sprite[0].speed / length), 
                        #                                    y * (selected_sprite[0].speed / length))
                        
            elif event.type == pygame.MOUSEMOTION:
                if mouse_tracking:
                    camera.position = (camera.position[0] - (pygame.mouse.get_pos()[0] - mouse_previous_pos[0]) / camera.scaling_factor, camera.position[1] - (pygame.mouse.get_pos()[1] - mouse_previous_pos[1]) / camera.scaling_factor)
                    mouse_previous_pos = pygame.mouse.get_pos()
            elif event.type == pygame.MOUSEBUTTONUP:
                if mouse_tracking:
                    mouse_tracking = False
            elif event.type == pygame.MOUSEWHEEL:
                if event.y == 1:
                    camera.scaling_factor = min(1.4, camera.scaling_factor + camera.scaling_step)
                if event.y == -1:
                    camera.scaling_factor = max(0.6, camera.scaling_factor - camera.scaling_step)

            main_manager.process_events(event)
        
        main_screen.fill((0, 0, 0))

        main_manager.update(time_delta)
        main_manager.draw_ui(main_screen)

        crew.update()

        active_enemies = pygame.sprite.groupcollide(enemies, crew, False, False, check_visibility)
        for i in active_enemies.keys():
            for member in active_enemies[i]:
                intersects = False
                for house in houses:
                    if house.rect.clipline(i.position, member.position):
                        intersects = True
                if not intersects:
                    i.target = member
        enemies.update()
        if boss.cooldown_counter == 0:
            BaseEnemy((random.randint(-20, 20), random.randint(-20, 20)), enemies)

        for member in crew:
            if member.auto_attack:
                visible_enemies = pygame.sprite.spritecollide(member, enemies, dokill=False, collided=check_visibility)
                if visible_enemies:
                    member.target = visible_enemies[0]
            if member.target:
                print(member.target)
                if member.cooldown_counter == 0:
                    member.cooldown_counter += 1
                    intersects = False
                    for house in houses:
                        if house.rect.clipline(member.position, member.target.position):
                            intersects = True
                    if not intersects:
                        member.target.hp -= 1
                        pygame.draw.line(main_screen, '#39FF14', ((camera.screen_size[0] // 2 - (camera.position[0] - member.rect.center[0]) * camera.scaling_factor - member.rect.size[0] // 2 * camera.scaling_factor, 
                                                                   camera.screen_size[1] // 2 - (camera.position[1] - member.rect.center[1]) * camera.scaling_factor - member.rect.size[1] // 2 * camera.scaling_factor)),
                                                                 ((camera.screen_size[0] // 2 - (camera.position[0] - member.target.rect.center[0]) * camera.scaling_factor - member.target.rect.size[0] // 2 * camera.scaling_factor, 
                                                                   camera.screen_size[1] // 2 - (camera.position[1] - member.target.rect.center[1]) * camera.scaling_factor - member.target.rect.size[1] // 2 * camera.scaling_factor)))
                else:
                    member.cooldown_counter += 1
                    if member.cooldown_counter == member.counter_max:
                        member.cooldown_counter = 0

        for i in houses:
            main_screen.blit(pygame.transform.scale_by(i.image, camera.scaling_factor), (camera.screen_size[0] // 2 - (camera.position[0] - i.rect.center[0]) * camera.scaling_factor - i.rect.size[0] // 2 * camera.scaling_factor, camera.screen_size[1] // 2 - (camera.position[1] - i.rect.center[1]) * camera.scaling_factor - i.rect.size[1] // 2 * camera.scaling_factor))

        for i in trees:
            main_screen.blit(pygame.transform.scale_by(i.image, camera.scaling_factor), (camera.screen_size[0] // 2 - (camera.position[0] - i.rect.center[0]) * camera.scaling_factor - i.rect.size[0] // 2 * camera.scaling_factor, camera.screen_size[1] // 2 - (camera.position[1] - i.rect.center[1]) * camera.scaling_factor - i.rect.size[1] // 2 * camera.scaling_factor))

        for i in enemies:
            main_screen.blit(i.image, (camera.screen_size[0] // 2 - (camera.position[0] - i.rect.center[0]) * camera.scaling_factor - i.rect.size[0] // 2 * camera.scaling_factor - i.rect.width // 2, camera.screen_size[1] // 2 - (camera.position[1] - i.rect.center[1]) * camera.scaling_factor - i.rect.size[1] // 2 * camera.scaling_factor - i.rect.height // 2))
        
        #main_screen.blit(boss.image, (camera.screen_size[0] // 2 - (camera.position[0] - boss.rect.center[0]) * camera.scaling_factor - boss.rect.size[0] // 2 * camera.scaling_factor - boss.rect.width // 2, camera.screen_size[1] // 2 - (camera.position[1] - boss.rect.center[1]) * camera.scaling_factor - boss.rect.size[1] // 2 * camera.scaling_factor - boss.rect.height // 2))

        for i in crew:
            main_screen.blit(i.image, (camera.screen_size[0] // 2 - (camera.position[0] - i.rect.center[0]) * camera.scaling_factor - i.rect.size[0] // 2 * camera.scaling_factor - i.rect.width // 2, camera.screen_size[1] // 2 - (camera.position[1] - i.rect.center[1]) * camera.scaling_factor - i.rect.size[1] // 2 * camera.scaling_factor - i.rect.height // 2))
            pygame.draw.circle(main_screen, (int(255 * (i.max_hp - i.hp) / i.max_hp), int(255 * (i.hp / i.max_hp)), 0), (camera.screen_size[0] // 2 - (camera.position[0] - i.rect.center[0]) * camera.scaling_factor - i.rect.size[0] // 2 * camera.scaling_factor, camera.screen_size[1] // 2 - (camera.position[1] - i.rect.center[1]) * camera.scaling_factor - i.rect.size[1] // 2 * camera.scaling_factor), 20, 5)

        
        fog_of_war.fill((0, 0, 0))
        for i in crew:
            pygame.draw.circle(fog_of_war, (255, 255, 255), ((fog_of_war.size[0] // 2 + i.rect.center[0]), (fog_of_war.size[1] // 2 + i.rect.center[1])), i.vision)
        for i in crew:
            pygame.draw.circle(fog_of_war, '#39FF14', ((fog_of_war.size[0] // 2 + i.rect.center[0]), (fog_of_war.size[1] // 2 + i.rect.center[1])), i.vision, 5)
        main_screen.blit(pygame.transform.scale_by(fog_of_war, camera.scaling_factor), camera.return_render_coords())

        main_screen.blit(pygame.transform.scale_by(game_map, camera.scaling_factor), camera.return_render_coords())
        
        pygame.draw.circle(main_screen, (255, 255, 0), mouse_sprite.rect.center, 5)
        screen.blit(main_screen, (0, 0))
        pygame.display.update()

        if boss.hp <= 0:
            return True
        elif len(crew) == 0:
            return False



        

start_menu()


pygame.quit()
