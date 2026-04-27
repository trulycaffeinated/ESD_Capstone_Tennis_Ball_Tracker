# ==========================================================
# Snickerdoodle Python Server (Stereo Processing)
# ==========================================================

import socket
import numpy as np
import cv2
import struct
import os

HOST = '0.0.0.0'
PORT = 9999

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(1)

print("Waiting for MATLAB connection...")
conn, addr = server.accept()
print("Connected to {}".format(addr))


# receive exact bytes
def recv_exact(sock, size):
    data = ''
    while len(data) < size:
        packet = sock.recv(size - len(data))
        if not packet:
            return None
        data += packet
    return data


# grayscale centroid detection
def find_centroid(gray):
    # Simple threshold
    _, thresh = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY)

    moments = cv2.moments(thresh)

    if moments["m00"] == 0:
        return 0.0, 0.0

    u = moments["m10"] / moments["m00"]
    v = moments["m01"] / moments["m00"]

    return float(u), float(v)
    
def get_HSV_centroid(image):
    # 1. Convert to HSV
    HSV = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # 2. Define the "Tennis Ball Yellow" range
    # These values usually work well for neon yellow/green balls
    lower_yellow = np.array([25, 40, 40])
    upper_yellow = np.array([90, 255, 255])
    
    #Creates a mask Ball is white, everything else black
    ballMask = cv2.inRange(HSV, lower_yellow, upper_yellow)
    
    # Cleans up noise
    ballMask = cv2.medianBlur(ballMask, 3)
    
    # Detects circle on the mask instead of the raw image
    circle = cv2.HoughCircles(ballMask, cv2.HOUGH_GRADIENT, dp=1.0, minDist=20,
                               param1=50, param2=8, minRadius=1, maxRadius=15)

    if circle is None:
        raise Exception("No ball found in HSV range")

    circle = np.uint16(np.around(circle))
    foundCircle = circle[0][0]
    
    u, v, radius = foundCircle[0], foundCircle[1], foundCircle[2]
    centerCoord = (u, v)
    
    # Return the mask as the 'debug' image so you can see what the computer "sees"
    return u, v, ballMask, centerCoord, radius

#draws indicator around ball
def draw_detection(img, center, radius):
    out = img.copy()
    cv2.circle(out, (int(center[0]), int(center[1])), int(radius), (0, 255, 0), 2)
    cv2.circle(out, (int(center[0]), int(center[1])), 3, (0, 0, 255), -1)
    return out

def test(name, func, imageL, imageR):

    print("\nTesting:", name)

    try:

        uLeft, vLeft, debuggedImgL, centerL, rL = func(imageL)
        uRight, vRight, deguggedImgR, centerR, rR = func(imageR)

        print("Left center:", centerL, " radius:", rL)
        print("Right center:", centerR, " radius:", rR)

        outL = draw_detection(imageL, centerL, rL)
        outR = draw_detection(imageR, centerR, rR)

        if not os.path.exists("output"):
            os.makedirs("output")

        cv2.imwrite("output/" + name + "_left.png", outL)
        cv2.imwrite("output/" + name + "_right.png", outR)

        cv2.imwrite("output/" + name + "_debug_left.png", debuggedImgL)
        cv2.imwrite("output/" + name + "_debug_right.png", deguggedImgR)

        cv2.imshow(name + " Left", outL)
        cv2.imshow(name + " Right", outR)

    except Exception as e:
        print("Error:", str(e))

while True:
    try:
        # receive header
        header = recv_exact(conn, 8)
        if header is None:
            print("Connection closed.")
            break

        width, height = struct.unpack('<II', header)

        # receive image stack
        frame_size = int(width * height * 6)

        data = recv_exact(conn, frame_size)
        if data is None:
            print("Failed to receive image data.")
            break

        frame = np.frombuffer(data, dtype=np.uint8)
        print("Expected bytes: ", width * height * 6)
        print("Received bytes: ", len(data))
        frame = frame.reshape((6, width, height))

        # split left and right
        left  = np.transpose(frame[0:3], (2,1,0))  # H x W x 3
        right = np.transpose(frame[3:6], (2,1,0))
        
        # receive methodID
        method_id_bytes = conn.recv(1)
        if method_id_bytes is None:
            print("Failed to receive method ID")
            break
        method_id = struct.unpack('B', method_id_bytes)[0]
        
        print("Method ID: ", method_id)
        
        if method_id == 0:
            # HSV processing
            process_mode = "HSV"

        elif method_id == 1:
            # Grayscale
            process_mode = "Grayscale"

        elif method_id == 2:
            # Binarize
            process_mode = "Binarize"

        elif method_id == 3:
            # YCbCr
            process_mode = "YCbCr"

        else:
            process_mode = "HSV"  # fallback
            
        if process_mode == "HSV":
            uL, vL, maskL = get_HSV_centroid(left)
            uR, vR, maskR = get_HSV_centroid(right)
            
            left_gray = maskL
            right_gray = maskR
            

        elif process_mode == "Grayscale":
            left_gray  = cv2.cvtColor(left,  cv2.COLOR_BGR2GRAY)
            right_gray = cv2.cvtColor(right, cv2.COLOR_BGR2GRAY)

            uL, vL = find_centroid(left_gray)
            uR, vR = find_centroid(right_gray)

        elif process_mode == "Binarize":
            left_gray  = cv2.cvtColor(left,  cv2.COLOR_BGR2GRAY)
            right_gray = cv2.cvtColor(right, cv2.COLOR_BGR2GRAY)

            uL, vL = find_centroid(left_gray)
            uR, vR = find_centroid(right_gray)

        elif process_mode == "YCbCr":
            # TEMP fallback
            left_gray  = cv2.cvtColor(left,  cv2.COLOR_BGR2GRAY)
            right_gray = cv2.cvtColor(right, cv2.COLOR_BGR2GRAY)

            uL, vL = find_centroid(left_gray)
            uR, vR = find_centroid(right_gray)

        else:
            # SAFETY FALLBACK (VERY IMPORTANT)
            left_gray  = cv2.cvtColor(left,  cv2.COLOR_BGR2GRAY)
            right_gray = cv2.cvtColor(right, cv2.COLOR_BGR2GRAY)

            uL, vL = find_centroid(left_gray)
            uR, vR = find_centroid(right_gray)

        # Send images
        conn.sendall(left_gray.tostring())
        conn.sendall(right_gray.tostring())

        # Send centroid data (4 floats)
        conn.sendall(struct.pack('ffff', uL, vL, uR, vR))

    except Exception as e:
        print("Error:", e)
        break

# CLEANUP
conn.close()
server.close()
print("Server closed.")
