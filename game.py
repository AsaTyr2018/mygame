from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import random
import json
# Global seed used to generate the world so it can be reproduced on load
world_seed = None

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

    def __init__(self, node, yield_amount=3, interval=10):
        super().__init__(
            model='cube',
            color=color.yellow,
            position=node.position + Vec3(0, 1, 0),
            scale=1,
        )
        self.node = node
        self.timer = 0
        self.container = None
        self.yield_amount = yield_amount
        self.interval = interval

    def update(self):
        self.timer += time.dt
        if self.timer >= self.interval:
            if self.container is not None:
                self.container.deposit(self.node.resource_type, self.yield_amount)
            self.timer = 0

class StorageContainer(Entity):
    """Simple storage placed next to a miner to collect resources."""
    def __init__(self, position):
        super().__init__(
            model='cube',
            color=color.brown,
            collider='box',
            position=position,
            scale=1,
        )
        self.contents = {'stone': 0, 'iron': 0, 'copper': 0}

    def deposit(self, resource_type, amount=1):
        if resource_type in self.contents:
            self.contents[resource_type] += amount

def generate_world(seed):
    """Create resource nodes using a seed for reproducibility."""
    rng = random.Random(seed)
    nodes = []
    for resource_type in ["stone", "iron", "copper"]:
        for _ in range(5):
            pos = Vec3(rng.uniform(-20, 20), 0, rng.uniform(-20, 20))
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
        self.bg = Panel(parent=self, scale=(0.4, 0.3), color=color.rgba(0,0,0,180))
        self.text = Text(parent=self, text='', origin=(0,0), scale=2)
        self.update_text()
    def toggle(self):
        self.enabled = not self.enabled
        mouse.locked = not self.enabled
        player.enabled = not self.enabled
    def update_text(self):
        lines=[f"{k.capitalize()}: {v}" for k,v in resources.items()]
        self.text.text="\n".join(lines)

class ContainerMenu(Entity):
    """UI for interacting with storage containers."""
    def __init__(self):
        super().__init__(parent=camera.ui, enabled=False)
        self.bg = Panel(parent=self, scale=(0.3,0.2), color=color.rgba(0,0,0,180))
        self.text = Text(parent=self, text='', origin=(0,0), scale=2)
        self.take_all_button = Button(text='Take All', parent=self, scale=(0.2,0.05), position=(0,-0.07))
        self.take_all_button.on_click=self.take_all
        self.container = None

    def toggle(self, container=None):
        if not self.enabled and container is not None:
            self.container = container
            self.update_text()
        self.enabled = not self.enabled
        mouse.locked = not self.enabled
        player.enabled = not self.enabled

    def update_text(self):
        if self.container:
            lines=[f"{k.capitalize()}: {v}" for k,v in self.container.contents.items()]
            self.text.text="\n".join(lines)
        else:
            self.text.text=""

    def take_all(self):
        if not self.container:
            return
        for r,v in self.container.contents.items():
            resources[r] += v
            self.container.contents[r] = 0
        self.update_text()
        hud.update_text()
        inventory_menu.update_text()
class BuildingMenu(Entity):

    """Menu for selecting buildings to place."""
    def __init__(self):
        super().__init__(parent=camera.ui, enabled=False)
        self.bg = Panel(parent=self, scale=(0.3,0.2), color=color.rgba(0,0,0,180))
        self.container_button=Button(text='Place Container', parent=self, scale=(0.2,0.05), position=(0,-0.06))
        self.container_button.on_click=self.place_container
        self.miner_button=Button(text='Place Miner', parent=self, scale=(0.2,0.05), position=(0,0))
        self.miner_button.on_click=self.place_miner
    def toggle(self):
        self.enabled = not self.enabled
        mouse.locked = not self.enabled
        player.enabled = not self.enabled
    def place_miner(self):
        global build_mode
        build_mode='miner'
        self.toggle()
    def place_container(self):
        global build_mode
        build_mode='container'
        self.toggle()

class EscapeMenu(Entity):
    """Escape menu with game options."""
    def __init__(self):
        super().__init__(parent=camera.ui, enabled=False)
        self.bg = Panel(parent=self, scale=(0.3,0.3), color=color.rgba(0,0,0,180))
        self.new_button=Button(text='New Game', parent=self, scale=(0.2,0.05), position=(0,0.1))
        self.new_button.on_click=new_game
        self.save_button=Button(text='Save Game', parent=self, scale=(0.2,0.05), position=(0,0))
        self.save_button.on_click=save_game
        self.load_button=Button(text="Load Game", parent=self, scale=(0.2,0.05), position=(0,-0.05))
        self.load_button.on_click=load_game
        self.exit_button=Button(text='Exit', parent=self, scale=(0.2,0.05), position=(0,-0.15))
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
world_seed = random.randint(0, 2**32 - 1)
nodes = generate_world(world_seed)
miners = []
hud = ResourceHUD()
containers = []
inventory_menu = InventoryMenu()
building_menu = BuildingMenu()
container_menu = ContainerMenu()

build_mode = None

mine_timer = 0
PLAYER_MINE_INTERVAL = 10
def new_game():
    global nodes, miners, containers, resources, world_seed, build_mode
    for m in miners:
        destroy(m)
    miners.clear()
    for c in containers:
        destroy(c)
    containers.clear()
    for n in nodes:
        destroy(n)
    world_seed = random.randint(0, 2**32 - 1)
    nodes = generate_world(world_seed)
    resources = {'stone': 0, 'iron': 0, 'copper': 0}
    player.position = Vec3(0,0,0)
    build_mode = None
    hud.update_text()
    inventory_menu.update_text()
def save_game():
    data = {
        "seed": world_seed,
        "resources": resources,
        "position": [float(player.position.x), float(player.position.y), float(player.position.z)]
    }
    with open("save.json", "w") as f:
        json.dump(data, f)
    print("Game saved")


def load_game():
    global nodes, miners, containers, resources, world_seed, build_mode
    try:
        with open("save.json", "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        print("No save file")
        return
    for m in miners:
        destroy(m)
    miners.clear()
    for c in containers:
        destroy(c)
    containers.clear()
    for n in nodes:
        destroy(n)
    world_seed = data.get("seed", random.randint(0, 2**32 - 1))
    nodes = generate_world(world_seed)
    resources = data.get("resources", {'stone': 0, 'iron': 0, 'copper': 0})
    pos = data.get("position", [0, 0, 0])
    player.position = Vec3(*pos)
    build_mode = None
    hud.update_text()
    inventory_menu.update_text()
    print("Game loaded")
escape_menu = EscapeMenu()


def input(key):
    if key == 'e':
        for c in containers:
            if distance(player.position, c.position) < 3:
                container_menu.toggle(c)
                return
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
    if inventory_menu.enabled or building_menu.enabled or escape_menu.enabled or container_menu.enabled:
        return
    if held_keys["e"]:
        mine_timer += time.dt
        if mine_timer >= PLAYER_MINE_INTERVAL:
            for node in nodes:
                if distance(player.position, node.position) < 3 and node.miner is None:
                    resources[node.resource_type] += 1
                    hud.update_text()
                    inventory_menu.update_text()
                    mine_timer = 0
                    break
    else:
        mine_timer = 0
    if build_mode == "miner" and mouse.left:
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
        build_mode = None
    elif build_mode == 'container' and mouse.left:
        for m in miners:
            if distance(player.position, m.position) < 3 and m.container is None:
                cost = {'stone': 5}
                if resources['stone'] >= cost['stone']:
                    resources['stone'] -= cost['stone']
                    hud.update_text()
                    inventory_menu.update_text()
                    cont = StorageContainer(m.position + Vec3(1,0,0))
                    containers.append(cont)
                    m.container = cont
                break
        build_mode = None


app.run()
