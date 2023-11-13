#!/usr/bin/python3
import time

from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
import subprocess

#functio to convert h264 to mp4
def convert_h264_to_mp4(h264_file, mp4_file):
    #eg ffmpeg -framerate 24 -i test.h264 -c:v copy -f mp4 test.mp4
    # overwrite output file if it exists
    try:
        print('Converting {} to {}...'.format(h264_file, mp4_file))
        subprocess.run(['ffmpeg', '-y', '-framerate', '24', '-i', h264_file, '-c:v', 'copy', '-f', 'mp4', mp4_file], check=True)
        print('Done.')
        return True
    except Exception as e:
        print('Error converting {} to {}: {}'.format(h264_file, mp4_file, e))
        return False





picam2 = Picamera2()
video_config = picam2.create_video_configuration()
picam2.configure(video_config)

encoder = H264Encoder(10000000)

picam2.start_recording(encoder, 'test.h264', pts='timestamp.txt')
time.sleep(10)
picam2.stop_recording()

success = convert_h264_to_mp4('test.h264', 'test.mp4')
if success:
    print('Success!')
else:
    print('Failed.')