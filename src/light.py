import time
import atexit
import random
from tools import Tools
import RPi.GPIO as GPIO

class Light:
    def __init__(self, pin=12, frequency=100):
        self.tools = Tools()
        self.pin = pin
        self.frequency = frequency
        self.talking = False

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)

        self.pwm = GPIO.PWM(self.pin, self.frequency)
        self.pwm.start(0)  

        atexit.register(self.cleanup)

    def start_talking(self):
        self.talking = True

    def stop_talking(self):
        self.talking = False
        self.pwm.ChangeDutyCycle(0)

    def flicker(self):
        if self.talking:
            brightness = random.randint(20, 100)
            self.pwm.ChangeDutyCycle(brightness)
            time.sleep(random.uniform(0.05, 0.2))
        else:
            self.pwm.ChangeDutyCycle(0)
            time.sleep(0.1)

    def max_brightness(self):
        self.talking = False
        self.pwm.ChangeDutyCycle(100)

    def cleanup(self):
        self.tools.printandlog("Pulizia GPIO e spegnimento luce")
        self.pwm.stop()
        GPIO.cleanup()

    def flicker_during_talk(duration):
        light.start_talking()
        start_time = time.time()
        while time.time() - start_time < duration:
            light.flicker()
        light.stop_talking()
        light.max_brightness()  # Torna al massimo alla fine

if __name__ == "__main__":
    light = Light()
    try:
        light.start_talking()
        while True:
            light.flicker()
    except KeyboardInterrupt:
        print("\nCtrl+C premuto: metto luce al massimo")
        light.max_brightness()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nSecondo Ctrl+C premuto: pulisco e spengo")
            light.cleanup()
