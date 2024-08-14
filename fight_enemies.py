import pygame
import neat
import random
from Components import BUTTON_FONT, FPS, WIN_HEIGHT, WIN_WIDTH
from Player import Player
from Enemy import Enemy
from main import main_menu


GEN = 0
goodNet = None
nets = []
ge = []

class AIPlayer(Player):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.hitEnemies = set()
    
    def addToSet(self, enemy):
        self.hitEnemies.add(enemy)

class AIEnemy(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.hits = 0
    
    def convert(self):
        self.hits += 1


def draw_scene(win, players, enemies, GEN, lowestEnemies, score):
    #win.fill((0, 0, 0)) 
    background = pygame.image.load("background.jpg")
    win.blit(background, (0,0))
    for player in players:
        player.draw(win)
        for enemy in enemies:
            enemy.draw(win)
        for projectile in player.projectiles[:]:
            projectile.draw(win)
            if projectile.x < 0 or projectile.x > WIN_WIDTH or projectile.y < 0 or projectile.y > WIN_HEIGHT:
                player.projectiles.remove(projectile)
    if goodNet != None:
        score = score // 15
    score_text = BUTTON_FONT.render(f"Score: {score}", 1, (255, 255, 255))
    win.blit(score_text, (WIN_WIDTH - score_text.get_width() - 10, 10))
    gen_text = BUTTON_FONT.render(f"Gen: {GEN}", 1, (255, 255, 255))
    win.blit(gen_text, (10, 20))
    for player in lowestEnemies:
        pygame.draw.line(win, (0, 255, 0), (player.x, player.y), 
                         (lowestEnemies.get(player).x if lowestEnemies.get(player).x else WIN_WIDTH/2,
                           lowestEnemies.get(player).y if lowestEnemies.get(player).y else WIN_HEIGHT/2), 1)
    pygame.display.update()

def check_collision(player, enemies):
    player_bb = player.get_bounding_box()
    for enemy in enemies:
        enemy_bb = enemy.get_bounding_box()
        if player_bb.colliderect(enemy_bb) and enemy not in player.hitEnemies:
            enemy.convert()
            player.addToSet(enemy)
            return True
    return False

def handle_projectile_collisions(player, enemies):
    for projectile in player.projectiles[:]:
        projectile_bb = projectile.get_bounding_box() 
        for enemy in enemies[:]:
            enemy_bb = enemy.get_bounding_box()
            if projectile_bb.colliderect(enemy_bb) and enemy not in player.hitEnemies:
                player.projectiles.remove(projectile)
                enemy.convert()
                player.addToSet(enemy)
                return True

                
def handle_enemy_shooting(enemy, player):
    enemy.shoot()
    for projectile in enemy.enemy_projectiles[:]:
        projectile.move()
        if projectile.y > WIN_HEIGHT:
            enemy.enemy_projectiles.remove(projectile)
        elif projectile.get_bounding_box().colliderect(player.get_bounding_box()):
            enemy.enemy_projectiles.remove(projectile)
            player.health -= 1

# Fitness function
def game_loop(genomes, config):
    global GEN
    GEN += 1
    GAME_HEALTH = 2
    GAME_SCORE = 0
    players = []

    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(goodNet if goodNet != None else net)
        players.append(AIPlayer(WIN_WIDTH/2, 550))
        g.fitness = 0
        ge.append(g)

    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()

    enemies = [AIEnemy(random.randint(10, 590), random.randint(-300, 25)) for _ in range(10)]

    run = True
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                nets.clear()
                ge.clear()
                players.clear()
                enemies.clear()
                GEN = 0                
                main_menu()


        if len(enemies) == 0 or len(players) == 0:
            run = False

        if len(enemies) < 9:
            enemies.append(AIEnemy(random.randint(10, 590), random.randint(-250, 25)))

        if GAME_HEALTH <= 0:
            run = False

        if GAME_SCORE > 150 and goodNet is None:
            run = False

        lowestEnemies = {} 

        for x, player in enumerate(players):

            player.lowestEnemy = max([enemy for enemy in enemies if enemy not in player.hitEnemies], key=lambda enemy: enemy.y, default=AIEnemy(WIN_WIDTH/2, WIN_HEIGHT/2))
            lowestEnemies[player] = player.lowestEnemy

            if player.lowestEnemy:
                output = nets[x].activate((player.x, player.lowestEnemy.x))
                
            if output[0] <= 0:
                player.shoot()
                ge[x].fitness += 1 if abs(player.x - player.lowestEnemy.x) < 2 else -0.1

            if output[1] < 0:
                player.move(1)
                ge[x].fitness += 0.1 if abs(player.lowestEnemy.x - (player.x - 1)) < abs(player.lowestEnemy.x - player.x) else -0.1 
            if output[1] >=0 and output[1] <= 3:
                ge[x].fitness -= 0.1
            if output[1] > 3:
                player.move(2)
                ge[x].fitness += 0.1 if abs(player.lowestEnemy.x - (player.x + 1)) < abs(player.lowestEnemy.x - player.x) else -0.1 
                
            if player.health <= 0:
                players.pop(x)
                nets.pop(x)
                ge.pop(x)

            for projectile in player.projectiles:
                projectile.move()

            if check_collision(player, enemies):
                player.health -= 1

            if handle_projectile_collisions(player, enemies):
                GAME_SCORE += 1
            

            for enemy in enemies:
                enemy.move()
                if enemy.y > 600 or enemy.hits >= 15: #15 is pop size
                    enemies.remove(enemy)
                    if enemy.hits == 0:
                        GAME_HEALTH -= 1

        draw_scene(win, players, enemies, GEN, lowestEnemies, GAME_SCORE)
    

def run(config, net):
    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    global goodNet
    goodNet = net

    winner = p.run(game_loop) 
    print('\nBest genome:\n{!s}'.format(winner))
    #with open("best.pickle", "wb") as f:
    #    pickle.dump(winner, f)
