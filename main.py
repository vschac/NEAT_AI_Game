import pygame
import fight_enemies
import os
import neat
import pickle
from Components import Button, BUTTON_FONT, WIN_HEIGHT, WIN_WIDTH


def best_network(config, directory):
    file_path = os.path.join(directory, "best.pickle")
    with open(file_path, "rb") as f:
        winner = pickle.load(f)
    return neat.nn.FeedForwardNetwork.create(winner, config)


def main_menu():
    pygame.display.set_caption("Main Menu")

    local_directory = os.path.dirname(__file__)
    config_path = os.path.join(local_directory, "config-fight.txt")
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)

    clock = pygame.time.Clock()
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

    game_button = Button(200, 150, 200, 50, "Run Trained AI", BUTTON_FONT, (100, 100, 100), (150, 150, 150))
    fight_button = Button(200, 250, 200, 50, "Watch AI Train", BUTTON_FONT, (100, 100, 100), (150, 150, 150))
    quit_button = Button(200, 350, 200, 50, "Quit", BUTTON_FONT, (100, 100, 100), (150, 150, 150))

    running = True
    while running:
        clock.tick(60)
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if game_button.is_clicked(mouse_pos):
                    fight_enemies.run(config, best_network(config, local_directory))
                elif fight_button.is_clicked(mouse_pos):
                    fight_enemies.run(config, None)
                elif quit_button.is_clicked(mouse_pos):
                    running = False

        if game_button.is_hovered(mouse_pos):
            game_button.current_color = game_button.hover_color
        else:
            game_button.current_color = game_button.color

        if fight_button.is_hovered(mouse_pos):
            fight_button.current_color = fight_button.hover_color
        else:
            fight_button.current_color = fight_button.color

        if quit_button.is_hovered(mouse_pos):
            quit_button.current_color = quit_button.hover_color
        else:
            quit_button.current_color = quit_button.color

        win.fill((0, 0, 0))
        game_button.draw(win)
        fight_button.draw(win)
        quit_button.draw(win)
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main_menu()