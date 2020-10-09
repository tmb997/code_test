"""
Framework   : OpenCV Aruco
Description : Calibration using checkerboard 
Status      : Running
References  :
    1) https://stackoverflow.com/questions/31249037/calibrating-webcam-using-python-and-opencv-error?rq=1
    2) https://calib.io/pages/camera-calibration-pattern-generator
"""
import numpy as np
import cv2
import glob
import random
import os
import shutil

"""cv_file = cv2.FileStorage("calib_images/calib_file.yaml", cv2.FILE_STORAGE_READ)
mtx = cv_file.getNode("camera_matrix").mat()
dist = cv_file.getNode("dist_coeff").mat()
cv_file.release()"""


# Wait time to show calibration in 'ms'
WAIT_TIME = 100

# termination criteria for iterative algorithm
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# generalizable checkerboard dimensions
# https://stackoverflow.com/questions/31249037/calibrating-webcam-using-python-and-opencv-error?rq=1
cbrow = 6
cbcol = 7

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
# IMPORTANT : Object points must be changed to get real physical distance.
objp =np.zeros((cbrow * cbcol, 3), np.float32)
objp[:, :2] = 10*np.mgrid[0:cbcol, 0:cbrow].T.reshape(-1, 2)

# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.

images = glob.glob('calib_images/BVC_images/*.jpg')

N=100
random.shuffle(images)

for fname in images[:N]:
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    # Find the chess board corners
    criteria_2=  cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_NORMALIZE_IMAGE + cv2.CALIB_CB_FAST_CHECK
    ret, corners = cv2.findChessboardCorners(gray, (cbcol,cbrow),criteria_2)

    # If found, add object points, image points (after refining them)
    if ret == True:

        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.001)
        corners = cv2.cornerSubPix(gray,corners,(5,5),(-1,-1),criteria)

        objpoints.append(objp)

        corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
        imgpoints.append(corners2)

        # Draw and display the corners
        img = cv2.drawChessboardCorners(img, (cbcol, cbrow), corners2,ret)
        cv2.imshow('img',cv2.resize(img,(int(1920/2),int(1080/2))))
        cv2.waitKey(WAIT_TIME)
        print(fname[-10:])
    else:
        shutil.move(fname[:39]+"/"+fname[40:],"calib_images/Blender camera calibration/non_suitable/" + fname[40:])


print("Start Calibration")
cv2.destroyAllWindows()
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1],mtx,dist)
print("Finish Calibration")

# ---------- Saving the calibration -----------------
cv_file = cv2.FileStorage("calib_images/test2.yaml", cv2.FILE_STORAGE_WRITE)
cv_file.write("camera_matrix", mtx)
cv_file.write("dist_coeff", dist)

# note you *release* you don't close() a FileStorage object
cv_file.release()
print("Finish")

