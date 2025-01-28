from evdev import InputDevice, categorize, ecodes, list_devices


def find_device_path(device_name):
    # List all input devices
    devices = [InputDevice(path) for path in list_devices()]
    for device in devices:
        if device_name :
            return device.path
    return None

# Replace 'eventX' with the appropriate event number
device_name = "NB Speaker"
device_path = find_device_path(device_name)

if device_path:
    print(f"Device '{device_name}' found at: {device_path}")
else:
    print(f"Device '{device_name}' not found")
    
device = InputDevice(device_path)

print(f"Listening to input from {device.path}, {device.name}, {device.phys}")

for event in device.read_loop():
    if event.type == ecodes.EV_KEY:
        categorized_event = categorize(event)
        print(categorized_event)
        keycode = categorized_event.keycode
        if 'PAUSE' or 'PLAY' in keycode:
            print(f"Key Play/Pause pressed")
        elif 'NEXT' in keycode:
            print(f"Key Next pressed")
        elif 'PREVIOUS' in keycode:
            print(f"Key Previous pressed")
        
