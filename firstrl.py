import tdl

def handle_keys():
	global playerx, playery
 
	user_input = tdl.event.key_wait()
 
	#movement keys
	if user_input.key == 'UP':
		playery -= 1
 
	elif user_input.key == 'DOWN':
		playery += 1
 
	elif user_input.key == 'LEFT':
		playerx -= 1
 
	elif user_input.key == 'RIGHT':
		playerx += 1

	if user_input.key == 'ENTER' and user_input.alt:
		#Alt+Enter: toggle fullscreen
		tdl.set_fullscreen(not tdl.get_fullscreen())
 
	elif user_input.key == 'ESCAPE':
		return True


SCREEN_WIDTH = 90
SCREEN_HEIGHT = 50
# LIMIT_FPS = 20

#############################################
# Initialization & Main Loop                #
#############################################

con = tdl.init(SCREEN_WIDTH, SCREEN_HEIGHT)
root = tdl.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="RogueLike", fullscreen=True)
tdl.set_font('terminal8x14_gs_ro.png', greyscale=True, altLayout=True)
# tdl.setFPS(LIMIT_FPS)

playerx = SCREEN_WIDTH//2
playery = SCREEN_HEIGHT//2

while not tdl.event.is_window_closed():
	root.draw_char(playerx, playery, '@', bg=None, fg=(255,255,255))
	root.blit(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0)
	tdl.flush()

	root.draw_char(playerx, playery, ' ', bg=None)

	exit_game = handle_keys()
	if exit_game:
		break