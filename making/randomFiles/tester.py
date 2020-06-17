from ahk import AHK

ahk = AHK()

ahk.mouse_move(x=100, y=100, blocking=True)  # Blocks until mouse finishes moving (the default)
ahk.mouse_move(x=150, y=150, speed=10, blocking=True) # Moves the mouse to x, y taking 'speed' seconds to move
print(ahk.mouse_position)  #  (150, 150)


# from ahk import AHK, Hotkey, ActionChain
# from time import sleep
#
# ahk = AHK()

# ahk = AHK()
#
# def end():
# 	hotkey.stop()
#
# def press_down():
# 	time = 0.005
# 	ahk.key_down('Left')  # Press down key
# 	sleep(time)
# 	ahk.key_up('Left')  # Release the key
#
# 	ac = ActionChain()
#
# 	# An Action Chain doesn't perform the actions until perform() is called on the chain
#
# 	ac.mouse_move(100, 100, speed=10)  # nothing yet
# 	ac.sleep(1)  # still nothing happening
# 	ac.mouse_move(500, 500, speed=10)  # not yet
# 	ac.perform()  # *now* each of the actions run in order
#
# def main():
#
# 	key_combo = '#n' # Define an AutoHotkey key combonation
# 	script = 'Run Notepad' # Define an ahk script
# 	hotkey = Hotkey(ahk, key_combo, script) # Create Hotkey
# 	hotkey.start()






main()
