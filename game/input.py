def get_node_at_pos(pos, mouse_pos, radius=20):
    for node, (x, y) in pos.items():
        dx, dy = mouse_pos[0] - x, mouse_pos[1] - y
        if dx*dx + dy*dy <= radius*radius:
            return node
    return None