from tools import Tools
import RPi.GPIO as GPIO

class Motion():
    def __init__(self):
        self.tools = Tools()
        self.motion_gpio = int(self.tools.load_config("motion_gpio","17"))

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.motion_gpio, GPIO.OUT) 

    def on(self):
        GPIO.output(self.motion_gpio, GPIO.HIGH)

    def off(self):
        GPIO.output(self.motion_gpio, GPIO.LOW)

    def cleanup(self):
        GPIO.cleanup()
