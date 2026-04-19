import subprocess
import sys
from PIL import ImageGrab
import time

calc = subprocess.Popen([sys.executable, "app.py"])
time.sleep(1.5)

frames = []
print("Gravando por 5 segundos... clique nos botoes!")

for i in range(30):
    frame = ImageGrab.grab()
    frames.append(frame)
    time.sleep(5 / 30)

frames[0].save(
    "calculadora.gif",
    save_all=True,
    append_images=frames[1:],
    loop=0,
    duration=167
)

calc.terminate()
print("GIF salvo como calculadora.gif!")
