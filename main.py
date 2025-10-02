import pygame
from game.map import load_colony_layout, draw_graph, draw_ants
from game.engine import spawn_black_ants
from game.input import get_node_at_pos

# Constantes
WIDTH, HEIGHT = 800, 600
NODE_RADIUS = 6
WHITE, BLACK = (255, 255, 255), (0, 0, 0)
COLORS = {
    'empty': (200, 200, 200),
    'colony': (0, 100, 0),
    'obstacle': (100, 0, 0),
    'enemy_spawn': (200, 0, 0)
}

def main():
    pygame.init()
    font = pygame.font.SysFont(None, 20)

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Test de la colonie : level1")
    clock = pygame.time.Clock()
    ant_black_img = pygame.image.load("assets/sprites/black_ant.png").convert_alpha()

    graph, pos, black_count = load_colony_layout("assets/levels/level1.colony")
    black_ants = spawn_black_ants(graph, count=int(black_count))
    selected_ant = None

    running = True
    message = ""
    message_timer= 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                print("Clic détecté à :", mouse_pos)
                clicked_node = get_node_at_pos(pos, mouse_pos)
                print("Nœud détecté :", clicked_node)

                if clicked_node:
                    if selected_ant:
                        if clicked_node in graph.neighbors(selected_ant.position):
                            selected_ant.plan_move(clicked_node)
                            print(f"{selected_ant.id} planifie déplacement vers {clicked_node}")
                            selected_ant.selected = False
                            selected_ant = None
                        else:
                            print("Déplacement interdit : nœud non adjacent")
                            message = "Déplacement interdit : salle non connectée"
                            message_timer = 120
                            selected_ant.selected = False
                    else:
                        for ant in black_ants:
                            if ant.position == clicked_node and ant.active:
                                selected_ant = ant
                                ant.selected = True
                                break

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                for ant in black_ants:
                    print(f"{ant.id} → next_node = {ant.next_node}")
                    ant.execute_move()
                    print(f"{ant.id} → nouvelle position = {ant.position}")

        # Affichage
        screen.fill((255, 255, 255))
        draw_graph(screen, graph, pos, font)
        draw_ants(screen, black_ants, pos, ant_black_img)
        if message_timer > 0:
            font_msg = pygame.font.SysFont(None, 24)
            text_surface = font_msg.render(message, True, (255, 0, 0))
            screen.blit(text_surface, (20, 20))
            message_timer -= 1

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()


if __name__ == "__main__":
    main()
