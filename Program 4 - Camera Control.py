import picamera
import io
import time 
from PIL import Image

time.sleep(1)
camera = picamera.PiCamera()
camera.framerate = 10
camera.start_recording('/home/pi/Desktop/all10fr_check.h264')
time.sleep(40)
camera.stop_recording()
print('Recording over')






##outputs = [io.BytesIO() for i in range(40)]
##start=time.time()
##camera.capture_sequence(outputs,'jpeg', use_video_port = True)
##finish = time.time()
##print('captured 40 images at %.2ffps' % (40/(finish - start)))
##
##print(outputs)
##
##im = outputs[1].read()
##img = Image.frombuffer("I;16", (5,1), im, "raw", "I;12")
##img.show()
