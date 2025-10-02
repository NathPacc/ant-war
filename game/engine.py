from game.ants import Ant

def spawn_black_ants(graph, count):
    ants = []
    colony_nodes = [n for n in graph.nodes if graph.nodes[n].get('type') == 'spawn']
    for i in range(count):
        start = colony_nodes[i % len(colony_nodes)]
        ant = Ant(f"B{i}", "black", start, hp=1)
        ants.append(ant)
    return ants