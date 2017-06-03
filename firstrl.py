#!/usr/bin/env python3
 
import tdl
from random import randint
 
#actual size of the window
SCREEN_WIDTH = 132
SCREEN_HEIGHT = 40
 
#size of the map
MAP_WIDTH = 132
MAP_HEIGHT = 35
 
#parameters for dungeon generator
ROOM_MAX_SIZE = 10
ROOM_MIN_SIZE = 6
MAX_ROOMS = 20
 
REALTIME = False
LIMIT_FPS = 20  #20 frames-per-second maximum
 
 
color_dark_wall = 0x400040
color_dark_ground = 0x323296
color_floor_background = 0x002809
color_wall_foreground = 0x403000
color_white = 0xFFFFFF

class GameObject:
	#this is a generic object: the player, a wall, a monster, an item, the stairs...
	#it's always represented by a character on screen.

	#temp is in celsium
	temperature = 24
	burn_temperature = 100

	def __init__(self, x, y, char, color):
		self.x = x
		self.y = y
		self.char = char
		self.color = (randint(1,255),randint(1,255),randint(1,255))
 
	def move(self, dx, dy):
		#move by the given amount, if the destination is not blocked
		if not my_map[self.x + dx][self.y + dy].blocked:
			self.x += dx
			self.y += dy
 
	def draw(self):
		#draw the character that represents this object at its position
		con.draw_char(self.x, self.y, self.char, self.color, bg=None)
 
	def clear(self):
		#erase the character that represents this object
		con.draw_char(self.x, self.y, ' ', self.color, bg=None)

	def get_info(self):
		return {'temperature': self.temperature, 'burn_temperature': self.burn_temperature }


class ObjectBag(list):
	def __init__(self):
		self.player = None
		self.characters = []
		self.items = []
 
 
class Tile(GameObject):
	#a tile of the map and its properties
	def __init__(self, blocked, block_sight=None):
		self.blocked = blocked
 
		#by default, if a tile is blocked, it also blocks sight
		if block_sight is None: 
			block_sight = blocked
		self.block_sight = block_sight

class Item(GameObject):
	#any item and it properties
	def __init__(self, x, y, char, color=None, pickable=True):
		super().__init__(x, y, char, color)
		self.pickable = pickable

class Character(GameObject):
	#any npc and it properties
	def __init__(self, x, y, char, color):
		super().__init__(x, y, char, color)

class Player(Character):
	#any npc and it properties
	def __init__(self, x, y, char = '@', color = color_white):
		super().__init__(x, y, char, color)

class Npc(Character):
	#any npc and it properties
	def __init__(self, x, y, char=2, color=None, hostile=False):
		super().__init__(x, y, char, color)
		self.hostile = hostile

class Rect:
	#a rectangle on the map. used to characterize a room.
	def __init__(self, x, y, w, h):
		self.x1 = x
		self.y1 = y
		self.x2 = x + w
		self.y2 = y + h
 
	def center(self):
		center_x = (self.x1 + self.x2) // 2
		center_y = (self.y1 + self.y2) // 2
		return (center_x, center_y)
 
	def intersect(self, other):
		#returns true if this rectangle intersects with another one
		return (self.x1 <= other.x2 and self.x2 >= other.x1 and
				self.y1 <= other.y2 and self.y2 >= other.y1)
 
 
def create_room(room):
	global my_map
	#go through the tiles in the rectangle and make them passable
	for x in range(room.x1 + 1, room.x2):
		for y in range(room.y1 + 1, room.y2):
			my_map[x][y].blocked = False
			my_map[x][y].block_sight = False
 
def create_h_tunnel(x1, x2, y):
	global my_map
	for x in range(min(x1, x2), max(x1, x2) + 1):
		my_map[x][y].blocked = False
		my_map[x][y].block_sight = False
 
def create_v_tunnel(y1, y2, x):
	global my_map
	#vertical tunnel
	for y in range(min(y1, y2), max(y1, y2) + 1):
		my_map[x][y].blocked = False
		my_map[x][y].block_sight = False
 
def make_map():
	global my_map
 
	#fill map with "blocked" tiles
	my_map = [[ Tile(True)
		for y in range(MAP_HEIGHT) ]
			for x in range(MAP_WIDTH) ]
 
	rooms = []
	num_rooms = 0
 
	for r in range(MAX_ROOMS):
		#random width and height
		w = randint(ROOM_MIN_SIZE, ROOM_MAX_SIZE)
		h = randint(ROOM_MIN_SIZE, ROOM_MAX_SIZE)
		#random position without going out of the boundaries of the map
		x = randint(0, MAP_WIDTH-w-1)
		y = randint(0, MAP_HEIGHT-h-1)
 
		#"Rect" class makes rectangles easier to work with
		new_room = Rect(x, y, w, h)
 
		#run through the other rooms and see if they intersect with this one
		failed = False
		for other_room in rooms:
			if new_room.intersect(other_room):
				failed = True
				break
 
		if not failed:
			#this means there are no intersections, so this room is valid
 
			#"paint" it to the map's tiles
			create_room(new_room)
 
			#center coordinates of new room, will be useful later
			(new_x, new_y) = new_room.center()
 
			if num_rooms == 0:
				#this is the first room, where the player starts at
				player.x = new_x
				player.y = new_y
 
			else:
				#all rooms after the first:
				#connect it to the previous room with a tunnel    
 
				#center coordinates of previous room
				(prev_x, prev_y) = rooms[num_rooms-1].center()
 
				#draw a coin (random number that is either 0 or 1)
				if randint(0, 1):
					#first move horizontally, then vertically
					create_h_tunnel(prev_x, new_x, prev_y)
					create_v_tunnel(prev_y, new_y, new_x)
				else:
					#first move vertically, then horizontally
					create_v_tunnel(prev_y, new_y, prev_x)
					create_h_tunnel(prev_x, new_x, new_y)
 
			#finally, append the new room to the list
			rooms.append(new_room)
			num_rooms += 1

def draw_player():
	print(objects.player.get_info())
	objects.player.draw()

def draw_npcs():
	#draw all characters in the list
	for characters in objects.characters:
		characters.draw()

def draw_items():
	#draw all item in the list
	for item in objects.items:
		item.draw()
 
def render_all():
	#go through all tiles, and set their background color
	for y in range(MAP_HEIGHT):
		for x in range(MAP_WIDTH):
			wall = my_map[x][y].block_sight
			if wall:
				con.draw_char(x, y, 177, fg=color_wall_foreground, bg=color_dark_wall)
			else:
				con.draw_char(x, y, '.', fg=color_wall_foreground, bg=color_floor_background)
 
	#draw all items in the list (draw player last to draw him on top layer)
	draw_npcs()
	draw_items()
	draw_player()

	#blit the contents of "con" to the root console and present it
	root.blit(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0)
 
def handle_keys(realtime):
	# global playerx, playery
 
	if realtime:
		keypress = False
		for event in tdl.event.get():
			if event.type == 'KEYDOWN':
			   user_input = event
			   keypress = True
		if not keypress:
			return
 
	else: #turn-based
		user_input = tdl.event.key_wait()
 
	if user_input.key == 'ENTER' and user_input.alt:
		#Alt+Enter: toggle fullscreen
		tdl.set_fullscreen(tdl.get_fullscreen())
 
	elif user_input.key == 'ESCAPE':
		return True  #exit game
 
	#movement keys
	if user_input.key == 'KP8':
		player.move(0, -1)
 
	elif user_input.key == 'KP2':
		player.move(0, 1)
 
	elif user_input.key == 'KP4':
		player.move(-1, 0)
 
	elif user_input.key == 'KP6':
		player.move(1, 0)

	elif user_input.key == 'KP7':
		player.move(-1, -1)
	
	elif user_input.key == 'KP9':
		player.move(1, -1)
	
	elif user_input.key == 'KP1':
		player.move(-1, 1)
	
	elif user_input.key == 'KP3':
		player.move(1, 1)
#############################################
# Initialization & Main Loop				#
#############################################
 
tdl.set_font('terminal10x16_gs_ro.png', greyscale=True, altLayout=False)
root = tdl.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="Roguelike", fullscreen=False)
tdl.setFPS(LIMIT_FPS)
con = tdl.Console(SCREEN_WIDTH, SCREEN_HEIGHT)

#create object representing the player
player = Player(SCREEN_WIDTH//2, SCREEN_HEIGHT//2)

#the list of objects with those two
objects = ObjectBag()
objects.player = player

#create up to ten NPCs
npc_num = randint(1,10)
print('npc count: '+ str(npc_num))
for i in range(npc_num):
	objects.characters.append(Npc(SCREEN_WIDTH//2 - i, SCREEN_HEIGHT//2))

#create up to ten items
item_num = randint(1,10)
print('item count: '+ str(item_num))
for i in range(item_num):
	objects.items.append(Item(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - i, 256))
 
#generate map (at this point it's not drawn to the screen)
make_map()
 
 
while not tdl.event.is_window_closed():
 
	#draw all objects in the list
	render_all()
 
	tdl.flush()
 
	#erase all objects at their old locations, before they move
	for object in objects:
		object.clear()
 
	#handle keys and exit game if needed
	exit_game = handle_keys(REALTIME)
	if exit_game:
		break