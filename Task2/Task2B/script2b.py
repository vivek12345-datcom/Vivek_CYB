import cv2
import numpy as np

hsv_color_values = {"Red":[([0,70,50],[10,255,255]),([170,70,50],[180,255,255])],
                    "Green":[([35,50,50],[85,255,255])],
                    "Blue":[([100,150,0],[140,255,255])],
                    "Yellow":[([20,100,100],[30,255,255])]}

def map_arena():
    """
    Task 2B: Perspective Transformation and Coordinate Mapping
    """
    # Initialize the output dictionary
    result = {
        "corner_points_detected": [],
        "robot_pixel_coord": [],
        "robot_real_world_coord": []
    }
     
    target_image = cv2.imread('test_images/angled_arena.png')
    hsv_image = cv2.cvtColor(target_image,cv2.COLOR_BGR2HSV)
    cordinate_points = {}
    for color,ranges in hsv_color_values.items():
            combined_mask=np.zeros(hsv_image.shape[:2],dtype=np.uint8)

            for low_hsv, upp_hsv in ranges:
                lower = np.array(low_hsv) 
                upper = np.array(upp_hsv)

                mask = cv2.inRange(hsv_image, lower, upper)
                combined_mask=cv2.bitwise_or(combined_mask,mask)

                contours, _ = cv2.findContours(combined_mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
                largest_contour = max(contours, key=cv2.contourArea)
                M = cv2.moments(largest_contour)

                if M["m00"] != 0:
                 cX_ = int(M["m10"] / M["m00"])
                 cY_ = int(M["m01"] / M["m00"])
                 cordinate_points[color]=[cX_,cY_]
    result["corner_points_detected"]=[cordinate_points["Red"],
                                    cordinate_points["Green"],
                                    cordinate_points["Blue"],
                                    cordinate_points["Yellow"]]

    
    pts_src = np.float32(result["corner_points_detected"])
    pts_dst = np.float32([[0, 0], [500, 0], [500, 500], [0, 500]])
    matrix = cv2.getPerspectiveTransform(pts_src, pts_dst)
    flat_image = cv2.warpPerspective(target_image, matrix, (500,500))
    aruco_dict=cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
    detector=cv2.aruco.ArucoDetector(aruco_dict,cv2.aruco.DetectorParameters())
    corners,ids,_=detector.detectMarkers(flat_image)
    
        
    if ids[0]==1:
        pts=corners[0][0]

        cX=int(np.mean(pts[:,0]))
        cY=int(np.mean(pts[:,1]))
        result["robot_pixel_coord"]=[cX,cY]
        x_cm=round(cX*0.4,2)
        y_cm=round(cY*0.4,2)
        result["robot_real_world_coord"]=[x_cm,y_cm]
        

                    


    
    
    return result

if __name__ == "__main__":
    # Test your function
    output = map_arena()
    print("Task 2B Output:")
    print(output)
