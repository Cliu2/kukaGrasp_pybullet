import cv2
import datetime
import sys
import os
from pylibfreenect2 import Freenect2, SyncMultiFrameListener
from pylibfreenect2 import FrameType, Registration, Frame
from pylibfreenect2 import createConsoleLogger, setGlobalLogger
from pylibfreenect2 import LoggerLevel
import numpy as np


listener = None
registration = None
frames = None
registered = Frame(512, 424, 4)
undistorted = Frame(512, 424, 4)
fn = Freenect2()

def open_kinect():
    try:
        from pylibfreenect2 import OpenGLPacketPipeline
        pipeline = OpenGLPacketPipeline()
    except:
        try:
            from pylibfreenect2 import OpenCLPacketPipeline
            pipeline = OpenCLPacketPipeline()
        except:
            from pylibfreenect2 import CpuPacketPipeline
            pipeline = CpuPacketPipeline()
    # print("Packet pipeline:", type(pipeline).__name__)

    # Create and set logger
    logger = createConsoleLogger(LoggerLevel.Error)
    setGlobalLogger(logger)

    global fn
    num_devices = fn.enumerateDevices()
    if num_devices == 0:
        print("No device connected!")
        sys.exit(1)

    serial = fn.getDeviceSerialNumber(0)
    device = fn.openDevice(serial, pipeline=pipeline)

    global listener
    listener = SyncMultiFrameListener(FrameType.Color | FrameType.Ir | FrameType.Depth)

    # Register listeners
    device.setColorFrameListener(listener)
    device.setIrAndDepthFrameListener(listener)

    device.start()

    # NOTE: must be called after device.start()
    global registration
    registration = Registration(device.getIrCameraParams(),
                                device.getColorCameraParams())


def get_frame():
    global listener
    global registration
    global frames
    global registered
    global undistorted

    frames = listener.waitForNewFrame()

    color = frames["color"]
    ir = frames["ir"]
    depth = frames["depth"]

    registration.apply(color, depth, undistorted, registered,
                       None,
                       None)

    color_arr = cv2.resize(color.asarray(), (int(1920 / 3), int(1080 / 3)))
    ir_arr = ir.asarray()
    depth_arr = depth.asarray()
    registered_arr = registered.asarray(np.uint8)

    return color_arr, ir_arr, depth_arr, registered_arr

def getbutton(registered_arr, depth_arr):
    
    orange_low = np.array([14, 140, 100])
    orange_high = np.array([22, 255, 255])

    red_low_1 = np.array([165, 65, 120])
    red_high_1 = np.array([179, 150, 255])

    red_low_2 = np.array([0, 160, 20])
    red_high_2 = np.array([10, 255, 150])
   

    hsv = cv2.cvtColor(registered_arr, cv2.COLOR_BGR2HSV)

    orange = cv2.inRange(hsv, orange_low, orange_high)
    red1 = cv2.inRange(hsv, red_low_1, red_high_1)
    red2 = cv2.inRange(hsv, red_low_1, red_high_1)
    red = cv2.bitwise_or(red1, red2)

    kernel = np.ones((5,5), np.uint8)
    red = cv2.medianBlur(red, 5)
    orange = cv2.medianBlur(orange, 5)
    red = cv2.dilate(red, kernel, iterations=2)
    orange = cv2.dilate(orange, kernel, iterations=1)


    mix = np.zeros(orange.shape, np.uint8)
    rows, cols = red.shape
    
    for i in range(rows):
        for j in range(cols):
            if orange[i, j] == 255 and i-25 < rows:
                for k in range(25,35):
                    mix[i-k, j] = 255



    mix = cv2.bitwise_and(mix, red)
    mix2, contours, hierarchy = cv2.findContours(mix, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=lambda x: cv2.contourArea(x) ,reverse=True)

    if len(contours) > 0:
        cv2.drawContours(registered_arr, contours, 0, (255, 255, 0), 3)
        M = cv2.moments(contours[0])
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
        ave_depth = 0
        num = 0

        for i in range(rows):
            for j in range(cols):
                if cv2.pointPolygonTest(contours[0], (j, i), False) > 0:
                    if (not depth_arr[i, j] == 0) and depth_arr[i, j] < 1500:
                        ave_depth += depth_arr[i, j]
                        num += 1

        if num > 0:
            ave_depth = ave_depth/num

        cv2.imshow("Frame", registered_arr)
        cv2.waitKey(0)
        return cx, cy, ave_depth
    
    else:
        return -1, -1, -1

def save_img(dir_name, filename=None):
    open_kinect()
    color_arr, ir_arr, depth_arr, registered_arr=get_frame()

    # depth_arr = np.uint8(depth_arr / 2500. * 255)
    # depth_arr[depth_arr > 140] = 255
    # depth_arr[depth_arr == 0] = 255
    # registered_arr[depth_arr == 255] = [255, 255, 255, 0]
    # registered_arr = registered_arr[y:y+h, x:x+w]
    # color_arr = color_arr[y:y+h, x:x+w]
    # time = datetime.datetime.now()

    x, y, h, w = 180, 0, 360, 300
    rows, cols, _ = color_arr.shape
    #print(rows, cols)
    M = cv2.getRotationMatrix2D((cols/2,rows/2),-90,1)
    dst = cv2.warpAffine(color_arr,M,(cols,rows))
    dst = cv2.flip(dst, flipCode=1) # flipping the img
    dst = dst[y:y+h, x:x+w] # cropping the img

    _filename = None
    if filename is None:
        # use the time stamp 
        _filename = dir_name+'/'+str(int(datetime.datetime.now().timestamp()*1000)) + ".jpg"
    else:
        _filename = dir_name+'/'+filename+".jpg"
        
    # cv2.imwrite(_filename, registered_arr)
    # cv2.imwrite(_filename, dst)
    listener.release(frames)
    return dst[:,:,0:3]     #remove the alpha channel

if __name__=='__main__':
    for i in range(10):
        save_img('./kinect_img')