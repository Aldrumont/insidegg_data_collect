import time
from pathlib import Path

import cv2
import depthai as dai

# Start defining a pipeline
pipeline = dai.Pipeline()

# Define a source - color camera
camRgb = pipeline.createColorCamera()
camRgb.setResolution(dai.ColorCameraProperties.SensorResolution.THE_4_K)
camRgb.setPreviewSize(3840//4, 2160//4)
# Create RGB output
xoutRgb = pipeline.createXLinkOut()
xoutRgb.setStreamName("rgb")
camRgb.video.link(xoutRgb.input)

# Create encoder to produce JPEG images
videoEnc = pipeline.createVideoEncoder()
videoEnc.setDefaultProfilePreset(camRgb.getVideoSize(), camRgb.getFps(), dai.VideoEncoderProperties.Profile.MJPEG)
camRgb.video.link(videoEnc.input)

# Create JPEG output
xoutJpeg = pipeline.createXLinkOut()
xoutJpeg.setStreamName("jpeg")
videoEnc.bitstream.link(xoutJpeg.input)

last_time = time.time()

# Connect and start the pipeline
with dai.Device(pipeline) as device:

    # Output queue will be used to get the rgb frames from the output defined above
    qRgb = device.getOutputQueue(name="rgb", maxSize=30, blocking=False)
    qJpeg = device.getOutputQueue(name="jpeg", maxSize=30, blocking=True)

    # Make sure the destination path is present before starting to store the examples
    Path('images').mkdir(parents=True, exist_ok=True)
    last_execution_time = time.time()
    start_time = time.time()
    while time.time() - start_time < 30:
        if time.time() - last_execution_time > 1:
            #inRgb = qRgb.tryGet()  # Non-blocking call, will return a new data that has arrived or None otherwise

            #if inRgb is not None:
                #cv2.imshow("rgb", inRgb.getCvFrame())

            for encFrame in qJpeg.tryGetAll():
                with open(f"images/{int(time.time() * 10000)}.jpeg", "wb") as f:
                    f.write(bytearray(encFrame.getData()))
        
            last_execution_time = time.time()
        # if cv2.waitKey(1) == ord('q'):
            # break
