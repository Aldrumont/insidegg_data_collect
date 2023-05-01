import RPi.GPIO as GPIO
from RpiMotorLib import RpiMotorLib
import time
from threading import Thread


direction= 19 # Direction (DIR) GPIO Pin
step = 13 # Step GPIO Pin
EN_pin = 26 # enable pin (LOW to enable)
relay_pin = 6
run_button = 5
steps_by_turn = 5000
running_led = 21
buzzer_pin=18
max_idle_minutes=1
blink_led_flag = False

mymotortest = RpiMotorLib.A4988Nema(direction, step, (-1,-1,-1), "DRV8825")
# Declare a instance of class pass GPIO pins numbers and the motor type
GPIO.setmode(GPIO.BCM)
GPIO.setup(running_led,GPIO.OUT) # set enable pin as output
GPIO.setup(run_button,GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(EN_pin,GPIO.OUT) # set enable pin as output
GPIO.setup(buzzer_pin,GPIO.OUT) # set enable pin as output



def run_motor(turns=4):
    """ negativo step is Counter-Clockwise and positive step is Clockwise"""
    GPIO.output(EN_pin,GPIO.LOW) # pull enable to low to enable motor
    step_number = steps_by_turn*turns
    if step_number > 0:
        direction = True
    else:
        step_number*=-1
        direction = False 
    mymotortest.motor_go(direction, # True=Clockwise, False=Counter-Clockwise
                "Full" , # Step type (Full,Half,1/4,1/8,1/16,1/32)
                step_number, # number of steps
                .0005, # step delay [sec]
                False, # True = print verbose output 
                .05) # initial delay [sec]
    GPIO.output(EN_pin,GPIO.HIGH) # pull enable to low to enable motor

    # GPIO.cleanup() # clear GPIO allocations after run

def blink_led():
    while blink_led_flag:
        GPIO.output(running_led, 1)
        time.sleep(0.5)
        GPIO.output(running_led, 0)
        time.sleep(0.5)

def play_a_sound(repeat_number=2, sleep_time=0.25):
    for i in range(repeat_number):
        GPIO.output(buzzer_pin, 1)
        time.sleep(sleep_time)
        GPIO.output(buzzer_pin, 0)
        time.sleep(sleep_time)


GPIO.output(running_led, 1)

last_running_time = time.time()
while True:
    running = 0 #button not pressed

    if(GPIO.input(run_button) == 0):
        running = 1
        light_on = True
        play_a_sound(1,0.25)
        blink_led_flag = True
        t = Thread(name='LED_BLINK_THREAD', target=blink_led)
        t.start()

    if running:
        GPIO.setup(relay_pin,GPIO.OUT)
        GPIO.output(relay_pin, 1)
        run_motor(1)
        #salva fotos em paralelo
        running=0
        blink_led_flag = False
        play_a_sound()
        t.join()
        GPIO.output(running_led, 1)
        last_running_time = time.time()
    
    dif_last_running_time = time.time() - last_running_time
    if dif_last_running_time > max_idle_minutes*60 and not running and light_on:
        # GPIO.output(relay_pin, 0)
        play_a_sound(3,0.25)
        GPIO.cleanup(relay_pin)
        light_on = False
        
    
    time.sleep(0.1)



    



#desliga apenas se ficar 2 minutos sem clicar
        





