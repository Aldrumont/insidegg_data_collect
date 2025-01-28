import RPi.GPIO as GPIO
import time

# GPIO setup
PINS = {"rele1": 16, "rele2": 20, "rele3": 12, "rele4": 21}

# Configuração dos GPIOs
GPIO.setmode(GPIO.BCM)
GPIO.setup(list(PINS.values()), GPIO.OUT)

# Inicializa todos os relés como desligados
GPIO.output(list(PINS.values()), GPIO.HIGH)

def turn_rele(rele, state):
    """
    Liga ou desliga o relé especificado.
    
    Args:
        rele (str): Nome do relé a ser acionado.
        state (bool): True para ligar, False para desligar.
    """
    GPIO.output(PINS[rele], GPIO.LOW if state else GPIO.HIGH)
    print(f"Relé {rele} {'ligado' if state else 'desligado'}.")

try:
    while True:
        for rele in PINS.keys():
            # Liga o relé atual
            turn_rele(rele, True)
            time.sleep(1)  # Espera 1 segundo
            # Desliga o relé atual
            turn_rele(rele, False)

except KeyboardInterrupt:
    print("Encerrando o programa...")

finally:
    # Desliga todos os relés ao finalizar
    GPIO.output(list(PINS.values()), GPIO.HIGH)
    GPIO.cleanup()
    print("GPIOs liberados e relés desligados.")
