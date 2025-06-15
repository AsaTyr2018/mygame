from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import random


class ResourceNode(Entity):
    """A simple resource node that can be mined by the player."""

    colors = {
        'stone': color.gray,
        'iron': color.rgb(192, 192, 192),
        'copper': color.rgb(184, 115, 51),
    }

    def __init__(self, resource_type, position=(0, 0, 0)):
        super().__init__(
            model='cube',
            color=self.colors.get(resource_type, color.white),
            collider='box',
            position=position,
            scale=1.5,
        )
        self.resource_type = resource_type
        self.miner = None


class Miner(Entity):
    """Automated resource generator placed on a node."""

    def __init__(self, node):
        super().__init__(
            model='cube',
            color=color.yellow,
            position=node.position + Vec3(0, 1, 0),
            scale=1,
        )
        self.node = node
        self.timer = 0

    def update(self):
        self.timer += time.dt
        if self.timer >= 10:
            resources[self.node.resource_type] += 1
            hud.update_text()
            self.timer = 0


def generate_world():
    """Create resource nodes at random positions."""
    nodes = []
    for resource_type in ['stone', 'iron', 'copper']:
        for _ in range(5):
            pos = Vec3(random.uniform(-20, 20), 0, random.uniform(-20, 20))
            node = ResourceNode(resource_type, position=pos)
            nodes.append(node)
    return nodes


class ResourceHUD(Entity):
    """Display current resources at top of the screen."""

    def __init__(self):
        super().__init__(parent=camera.ui)
        self.text_entity = Text(text='', position=Vec2(-0.5, 0.45), scale=2)
        self.update_text()

    def update_text(self):
        self.text_entity.text = (
            f"[Eisen: {resources['iron']}] [Kupfer: {resources['copper']}] "
            f"[Stein: {resources['stone']}]"
        )


app = Ursina()

# Ground
Entity(model='plane', scale=50, texture='white_cube', texture_scale=(50, 50), collider='box', color=color.green)

player = FirstPersonController()
player.cursor.visible = True

resources = {'stone': 0, 'iron': 0, 'copper': 0}
nodes = generate_world()
miners = []
hud = ResourceHUD()

build_mode = False


def update():
    global build_mode

    if held_keys['b']:
        build_mode = True
    if held_keys['escape']:
        build_mode = False

    # Gather resources when pressing E near a node
    if held_keys['e']:
        for node in nodes:
            if distance(player.position, node.position) < 3 and node.miner is None:
                resources[node.resource_type] += 1
                hud.update_text()
                break

    # Place miner on node when in build mode and left mouse clicked
    if build_mode and mouse.left:
        for node in nodes:
            if distance(player.position, node.position) < 3 and node.miner is None:
                cost = {'stone': 5, 'iron': 3, 'copper': 2}
                if all(resources[r] >= cost[r] for r in cost):
                    for r in cost:
                        resources[r] -= cost[r]
                    hud.update_text()
                    miner = Miner(node)
                    miners.append(miner)
                    node.miner = miner
                break


app.run()

