from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import random
import json


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
            inventory_menu.update_text()
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



class InventoryMenu(Entity):
    """Display inventory contents."""
    def __init__(self):
        super().__init__(parent=camera.ui, enabled=False)
        self.bg = Panel(scale=(0.4, 0.3), color=color.rgba(0,0,0,180))
        self.text = Text(parent=self, text='', origin=(0,0), scale=2)
        self.update_text()
    def toggle(self):
        self.enabled = not self.enabled
        mouse.locked = not self.enabled
        player.enabled = not self.enabled
    def update_text(self):
        lines=[f"{k.capitalize()}: {v}" for k,v in resources.items()]
        self.text.text="\n".join(lines)

class BuildingMenu(Entity):
    """Menu for selecting buildings to place."""
    def __init__(self):
        super().__init__(parent=camera.ui, enabled=False)
        self.bg = Panel(scale=(0.3,0.2), color=color.rgba(0,0,0,180))
        self.miner_button=Button(text='Place Miner', parent=self, scale=(0.2,0.05), position=(0,0))
        self.miner_button.on_click=self.place_miner
    def toggle(self):
        self.enabled = not self.enabled
        mouse.locked = not self.enabled
        player.enabled = not self.enabled
    def place_miner(self):
        global build_mode
        build_mode=True
        self.toggle()

class EscapeMenu(Entity):
    """Escape menu with game options."""
    def __init__(self):
        super().__init__(parent=camera.ui, enabled=False)
        self.bg = Panel(scale=(0.3,0.3), color=color.rgba(0,0,0,180))
        self.new_button=Button(text='New Game', parent=self, scale=(0.2,0.05), position=(0,0.1))
        self.new_button.on_click=new_game
        self.save_button=Button(text='Save Game', parent=self, scale=(0.2,0.05), position=(0,0))
        self.save_button.on_click=save_game
        self.exit_button=Button(text='Exit', parent=self, scale=(0.2,0.05), position=(0,-0.1))
        self.exit_button.on_click=application.quit
    def toggle(self):
        self.enabled = not self.enabled
        mouse.locked = not self.enabled
        player.enabled = not self.enabled

app = Ursina()

# Ground
Entity(model='plane', scale=50, texture='white_cube', texture_scale=(50, 50), collider='box', color=color.green)

player = FirstPersonController()
player.cursor.visible = True

resources = {'stone': 0, 'iron': 0, 'copper': 0}
nodes = generate_world()
miners = []
hud = ResourceHUD()
inventory_menu = InventoryMenu()
building_menu = BuildingMenu()
escape_menu = EscapeMenu()

build_mode = False


def new_game():
    global nodes, miners, resources
    for m in miners:
        destroy(m)
    miners.clear()
    for n in nodes:
        destroy(n)
    nodes = generate_world()
    resources = {'stone': 0, 'iron': 0, 'copper': 0}
    hud.update_text()
    inventory_menu.update_text()


def save_game():
    with open('save.json', 'w') as f:
        json.dump({'resources': resources}, f)
    print('Game saved')



def input(key):
    if key == 'i':
        inventory_menu.toggle()
    if key == 'b':
        building_menu.toggle()
    if key == 'escape':
        if escape_menu.enabled:
            escape_menu.toggle()
        elif inventory_menu.enabled:
            inventory_menu.toggle()
        elif building_menu.enabled:
            building_menu.toggle()
        else:
            escape_menu.toggle()


def update():
    global build_mode
    if inventory_menu.enabled or building_menu.enabled or escape_menu.enabled:
        return
    if held_keys['e']:
        for node in nodes:
            if distance(player.position, node.position) < 3 and node.miner is None:
                resources[node.resource_type] += 1
                hud.update_text()
                inventory_menu.update_text()
                break
    if build_mode and mouse.left:
        for node in nodes:
            if distance(player.position, node.position) < 3 and node.miner is None:
                cost = {'stone': 5, 'iron': 3, 'copper': 2}
                if all(resources[r] >= cost[r] for r in cost):
                    for r in cost:
                        resources[r] -= cost[r]
                    hud.update_text()
                    inventory_menu.update_text()
                    miner = Miner(node)
                    miners.append(miner)
                    node.miner = miner
                break
app.run()

