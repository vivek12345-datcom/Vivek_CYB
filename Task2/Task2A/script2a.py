import cv2
import numpy as np
import glob

def localize_bot():
    """
    Task 2A: Camera Calibration and ArUco Pose Estimation
    """
    # Initialize the output dictionary with exact keys required by the evaluator
    result = {
        "camera_matrix_trace": 0.0,
        "markers": {}
    }
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 0.001)
    objpoints = []
    imgpoints = []

    objectp3D = np.zeros((9*6,3),np.float32)
    objectp3D[:, :2]= np.mgrid[0:9,0:6].T.reshape(-1,2)
    objectp3D*=2.5
    prev_img_shape = None


    images = glob.glob('calibration_images/*.png')
    

    for arena in images:
        image = cv2.imread(arena)
        gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

        ret , corners = cv2.findChessboardCorners(gray,(9,6),None)

        if ret == True:
            objpoints.append(objectp3D.copy())
            imagep2D = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
            imgpoints.append(imagep2D.copy())

        ret, mtx, dist, r_vecs, t_vecs = cv2.calibrateCamera(objpoints, imgpoints,gray.shape[::-1],None,None)    
        result["camera_matrix_trace"] = round(float(np.trace(mtx)), 2)





    

    
    test_img = cv2.imread('test_images/test_arena.jpg')
    fixed_image = cv2.undistort(test_img, mtx, dist, None, mtx)

    
    dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
    parameters = cv2.aruco.DetectorParameters()
    detector = cv2.aruco.ArucoDetector(dictionary, parameters)

    corners, ids, rejected = detector.detectMarkers(fixed_image)

    if ids is not None:
        marker_3d_edges = np.array([[-2.5,2.5,0],[2.5,2.5,0],[2.5,-2.5,0],[-2.5,-2.5,0]],dtype = np.float32)
            
        for i, marker in enumerate(ids):
            success, rvec, tvec = cv2.solvePnP(marker_3d_edges,corners[i][0],mtx,dist)
            distance = round(float(tvec[2][0]),1)
            offset = round(float(tvec[0][0]),1)

            result["markers"][f"id_{marker[0]}"]= { "distance_z": distance,"x_offset":offset }
    

    
    result["markers"] = dict(

        sorted(

            result["markers"].items(),

            key=lambda item: int(
                item[0].split("_")[1]
            ),
            reverse=True
        )

    )

   
    return result

if __name__ == "__main__":
    
    output = localize_bot()
    print("Task 2A Output:")
    print(output)
