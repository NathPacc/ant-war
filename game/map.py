import pygame
import networkx as nx
import math

def load_colony_layout(filepath):
    G = nx.Graph()
    pos = {}
    types = {}

    with open(filepath, 'r') as f:
        mode = None
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if line == "NODES:":
                mode = "nodes"
                continue
            if line == "HALLWAYS:":
                mode = "hallway"
                continue
            if line == "UNITS:":
                mode = "units"
                continue

            if mode == "nodes":
                parts = line.split()
                node_id = parts[0]
                x, y = int(parts[1]), int(parts[2])
                node_type = parts[3] if len(parts) > 3 else "empty"
                G.add_node(node_id)
                pos[node_id] = (x, y)
                G.nodes[node_id]['type'] = node_type

            elif mode == "hallway":
                a, b = line.split()
                G.add_edge(a, b)

            elif mode == "units":
                a, b = line.split()
                if a == "black":
                    black_count = b

    return G, pos, black_count

def draw_graph(screen, graph, pos, font):
    for edge in graph.edges():
        pygame.draw.line(screen, (0, 0, 0), pos[edge[0]], pos[edge[1]], 2)

    for node in graph.nodes():
        node_type = graph.nodes[node].get('type', 'empty')
        x, y = pos[node]

        # Couleur selon le type
        color = {
            'empty': (200, 200, 200),
            'entry':(200, 0, 0),
            'queen': (0, 100, 0),
            'spawn': (0, 0, 200)
        }.get(node_type, (150, 150, 150))

        # Taille et forme
        if node_type == 'spawn':
            rect = pygame.Rect(x - 60, y - 45, 120, 90)
            pygame.draw.ellipse(screen, color, rect)
        else:
            pygame.draw.circle(screen, color, (x, y), 36)

        # Texte centré
        label = font.render(str(node), True, (255, 255, 255))
        label_rect = label.get_rect(center=(x, y))
        screen.blit(label, label_rect)

def draw_ants(screen, ants, pos, ant_img):
    for ant in ants:
        if ant.active:
            x1, y1 = pos[ant.position]
            rect = ant_img.get_rect(center=(x1, y1))
            screen.blit(ant_img, rect)
            if ant.selected:
                pygame.draw.circle(screen, (0, 0, 255), (x1, y1), 12, 2)
            if ant.next_node:
                x2, y2 = pos[ant.next_node]
                pygame.draw.line(screen, (0, 150, 0), (x1, y1), (x2, y2), 2)

                # Tête de flèche
                dx, dy = x2 - x1, y2 - y1
                angle = math.atan2(dy, dx)
                arrow_length = 10
                arrow_angle = math.pi / 6  # 30°

                # Deux segments pour la tête
                end1 = (x2 - arrow_length * math.cos(angle - arrow_angle),
                        y2 - arrow_length * math.sin(angle - arrow_angle))
                end2 = (x2 - arrow_length * math.cos(angle + arrow_angle),
                        y2 - arrow_length * math.sin(angle + arrow_angle))

                pygame.draw.line(screen, (0, 150, 0), (x2, y2), end1, 2)
                pygame.draw.line(screen, (0, 150, 0), (x2, y2), end2, 2)
        