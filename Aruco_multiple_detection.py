import numpy as np
import cv2
import cv2.aruco as aruco
import glob
import matplotlib.pyplot as plt
import math

def q_centroid(corner):
    corner=corner[0]
    a1=(corner[0][1]-corner[2][1])/(corner[0][0]-corner[2][0])
    a2=(corner[1][1]-corner[3][1])/(corner[1][0]-corner[3][0])
    b1=(corner[0][1]*corner[2][0]-corner[2][1]*corner[0][0])/(corner[0][0]-corner[2][0])
    b2=(corner[1][1]*corner[3][0]-corner[3][1]*corner[1][0])/(corner[1][0]-corner[3][0])

    xc=(b2-b1)/(a2-a1)
    yc=(a1*b2-a2*b1)/(a2-a1)

    return xc, yc   

cv_file = cv2.FileStorage("calib_images/test2.yaml", cv2.FILE_STORAGE_READ)
mtx = cv_file.getNode("camera_matrix").mat()
dist = cv_file.getNode("dist_coeff").mat()
cv_file.release()

file_name="test_4k_3.jpg"

frame = cv2.imread("Resources/"+file_name)
# operations on the frame
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

"""
mtx[0][2]=1920
mtx[1][2]=1080
mtx[0][0]=8000
mtx[1][1]=8000

dist[0][0:5]=[0,0,0,0,0] """

# set dictionary size depending on the aruco marker selected
aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_250)

# detector parameters can be set here (List of detection parameters[3])
parameters = aruco.DetectorParameters_create()
parameters.adaptiveThreshConstant = 10
parameters.cornerRefinementMethod = aruco.CORNER_REFINE_SUBPIX

# lists of ids and the corners belonging to each id
corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)

# font for displaying text (below)
font = cv2.FONT_HERSHEY_SIMPLEX

# check if the ids list is not empty
# if no check is added the code will crash
if np.all(ids != None):
    aruco.drawDetectedMarkers(frame, corners)
    for j in range(0,ids.size):
        #criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.001)
        #corners[j] = cv2.cornerSubPix(gray,corners[j],(5,5),(-1,-1),criteria)


        rvec, tvec , _= aruco.estimatePoseSingleMarkers([corners[j]], 12, mtx, dist) # 10.35
        aruco.drawAxis(frame, mtx, dist, rvec[0], tvec[0], 8)
        xc,yc=q_centroid(corners[j])
        cv2.circle(frame,(xc,yc),10,(255,255,0))
        print(rvec[0],tvec[0])
    
cv2.imwrite("Resources/Output/"+file_name[:-4]+"-wm"+file_name[-4:],frame)

plt.figure()
frame[:,:,(0,2)]=frame[:,:,(2,0)]
plt.imshow(frame)
plt.show()
cv2.destroyAllWindows()
print("Detection finished")

 

