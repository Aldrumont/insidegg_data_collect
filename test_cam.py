#!/usr/bin/python3

# To run this example, update libcamera-dev to version 0.0.12.

import time

from picamera2 import Picamera2, Preview

picam2 = Picamera2()
picam2.start_preview(Preview.QTGL)

preview_config = picam2.create_preview_configuration()
picam2.configure(preview_config)

picam2.start()
time.sleep(1)

# AfMode: Set the AF mode (manual, auto, continuous)
# LensPosition: Manual focus, Set the lens position.
for i in range (0, 20,1):
    picam2.set_controls({"AfMode": 0, "LensPosition": i})
    time.sleep(5)
    print("Lens position: {}".format(picam2.get_control_value("LensPosition")))
    


