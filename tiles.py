from typyboi.items import Weapon
from typyboi.enemies import Enemy
from typyboi.actions import MoveNorth, MoveEast, MoveSouth, MoveWest, ViewInventory, EquipWeapon, Flee, Attack
 
class MapTile:
    def __init__(self, x, y, flavor_text = ''):
        self.x = x
        self.y = y
        self.flavor_text = flavor_text
    
    def get_adjacent_moves(self, world):
        adjacent_moves = []
        x = self.x
        y = self.y
        # Check north
        if(world.tile_exists(x, y + 1)):
            adjacent_moves.append(MoveNorth())
        # Check east
        if(world.tile_exists(x + 1, y)):
            adjacent_moves.append(MoveEast())
        #Check south
        if(world.tile_exists(x, y - 1)):
            adjacent_moves.append(MoveSouth())
        #Check west
        if(world.tile_exists(x - 1, y)):
            adjacent_moves.append(MoveWest())

        return adjacent_moves

    def available_actions(self, world):
        moves = self.get_adjacent_moves(world)
        moves.append(ViewInventory())
        moves.append(EquipWeapon())
        return moves
 
    def modify_player(self, player):
        pass

class LootRoom(MapTile):
    def __init__(self, x, y, flavor_text = "", item_list = [], gold = 0):
        self.item_list = item_list
        self.gold = gold
        super().__init__(x, y, flavor_text)
 
    def add_loot(self, player):
        for item in self.item_list:
            player.inventory.add_item(item)
        player.inventory.add_gold(self.gold)
        self.item_list = []
        self.gold = 0
 
    def modify_player(self, player):
        self.add_loot(player)

class EnemyRoom(MapTile):
    def __init__(self, x, y, room_text, enemy = None):
        self.enemy = enemy
        self.room_text = room_text
        super().__init__(x, y, room_text)
 
    def modify_player(self, the_player):
        if self.enemy.is_alive():
            the_player.hp -= self.enemy.damage
            self.flavor_text = (
                'A {} attacks!\n'
                'Enemy HP: {}\n'
                'Enemy {} does {} damage. You have {} HP remaining.\n' 
                ).format(self.enemy.name, self.enemy.hp, self.enemy.name, self.enemy.damage, the_player.hp)
        else:
            self.flavor_text = self.room_text

    def available_actions(self, world):
        if self.enemy.is_alive():
            moves = []
            moves.append(Attack(enemy=self.enemy))
            moves.append(Flee(tile=self))
            return moves
        else:
            moves = self.get_adjacent_moves(world)
            moves.append(ViewInventory())
            moves.append(EquipWeapon())
            return moves
 
