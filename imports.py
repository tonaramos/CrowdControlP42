import subprocess
import sys

def install(package):
    subprocess.call([sys.executable, "-m", "pip", "install", package])

install('boto3')
install('opencv-python')
install('numpy')
install('pyautogui')
