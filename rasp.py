import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
from RpiMotorLib import RpiMotorLib

# Configurar os pinos do GPIO
PINS = {
    "verde": 16,
    "vermelho": 20,
    "branco": 12,
    "azul": 21
}
direction= 19 # Direction (DIR) GPIO Pin
step = 13 # Step GPIO Pin
EN_pin = 26 # enable pin (LOW to enable)

# Declare a instance of class pass GPIO pins numbers and the motor type
mymotortest = RpiMotorLib.A4988Nema(direction, step, (40,40,40), "DRV8825")

GPIO.setmode(GPIO.BCM)
GPIO.setup(list(PINS.values()), GPIO.OUT)
GPIO.setup(EN_pin,GPIO.OUT) # set enable pin as output
GPIO.output(list(PINS.values()), GPIO.HIGH)

# Callback quando uma mensagem PUBLISH é recebida do servidor.
def on_message(client, userdata, message):
    print(f"Recebida mensagem '{message.payload.decode()}' no tópico '{message.topic}'")

    command = message.payload.decode().lower()

    if command in PINS.keys():
        estado_atual = GPIO.input(PINS[command])
        novo_estado = GPIO.HIGH if estado_atual == GPIO.LOW else GPIO.LOW
        GPIO.output(PINS[command], novo_estado)
        acao = "aceso" if novo_estado == GPIO.LOW else "apagado"  # Lembre-se, a lógica está invertida
        print(f"LED {command} {acao}.")
    elif command == "apagar":
        GPIO.output(list(PINS.values()), GPIO.HIGH)
        print("Todos os LEDs apagados.")

    if command == "motor":
        # Assuming you want to run the motor for a certain number of steps and then stop
        if not getattr(on_message, "motor_running", False):
            # If motor is not running, start it
            GPIO.output(EN_pin, GPIO.LOW)
            mymotortest.motor_go(False, "Full", 10000, 0.0005, True, 0.05)
            on_message.motor_running = True
            print("Motor started.")
        else:
            # If motor is running, stop it
            GPIO.output(EN_pin, GPIO.HIGH)
            on_message.motor_running = False
            print("Motor stopped.")

# Configurações do MQTT
BROKER = "test.mosquitto.org"
PORT = 1883
TOPIC = "aldrumont/insidegg"

client = mqtt.Client()
client.on_message = on_message

client.connect(BROKER, PORT, 60)
client.subscribe(TOPIC)

# Loop para continuar processando mensagens
try:
    client.loop_forever()
except KeyboardInterrupt:
    print("Desconectado pelo usuário")
finally:
    GPIO.cleanup()
    print("GPIO limpo e desconectado do broker.")
