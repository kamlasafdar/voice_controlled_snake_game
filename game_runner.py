import sys
import threading
from game import SnakeGame
from voice_control import start_listening
import pygame
import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"  # Prevent OpenMP conflict


# Read language from command-line argument (default: English)
language = sys.argv[1] if len(sys.argv) > 1 else "English"

pygame.init()
game = SnakeGame()

# Start voice control in a separate thread with selected language
threading.Thread(target=start_listening, args=(game.change_direction, game), daemon=True).start()

# Main game loop
while game.running:
    pygame.event.pump()
    game.update()
    game.render()
    game.clock.tick(1)  # Control speed

game.quit()
print("💀 Game Over")