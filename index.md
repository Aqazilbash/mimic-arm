# Mimic Arm: Milestone 1

Team: Alex Qazilbash, Pepper Wang, Liam Brennan, Ophelia Lonzo, Maddy Fahey

---

## Code Architecture

We’ve written pseudocode for camera calibration and calculating hand position, and we’ve determined that we will be using Mediapipe for gesture detection and Cv2 for processing camera input.

---

**Requirements:** Numpy, Cv2, Mediapipe, Matplotlib

**Reference Frames**
* Camera Frame
* World Frame
   * Origin is center of hand space
* Robot Frame
   * Identical to World Frame (in that no translation between the two is needed), the hand location in the world frame will be the same location the robot attempts to move the end effector to

**Camera translation**
* Intrinsic calibration - need K matrix
   * Find from camera documentation, or with Zhang's method (checkerboard)

**Calibration Process (do once)**
* For each camera:
   * 10+ pictures of checkerboard is laid out on floor/table in the hand space, moved around & tilted
   * for each image:
      * Run cv.findChessboardCorners()
      * Increase accuracy with cv.cornerSubPix()
      * Add object points (3d coords) and image points (2d coords) to arrays
      * For confirmation, display corners with cv.drawChessboardCorners()
   * cv.calibrateCamera() takes in these object points & image points, returns camera matrix, distortion coefficients, rotation & translation vectors, etc
* cv.stereoCalibrate()
* cv.stereoRectify()
* Find Camera Frame -> World Frame transformation using solvePnP on rectified left image

**Class CameraSystem**
* undistort_image
   * Takes a frame from left side camera, on this frame, runs cv.getOptimalNewCameraMatrix(), then cv.undistort(), using camera calibration data gathered at start
* Get_3d_hand_location
   * Returns: the 3-dimensional location of the hand in the world frame, this is the location to be passed into arm inverse kinematics
   * Calls: get_2d_hand_location, get_hand_depth
* Get_2d_hand_location
   * Returns: the (x,y) (or (x,z)) coordinates for the center of the hand
   * Runs mediapipe hand detection on the undistorted image to get image points (x,y) position of hand in space
* get_hand_depth
   * Returns: depth value, the distance between camera and hand
   * Stereo Matching
      * Finds the 2D location of the hand on the left side camera (PL)
      * Uses this window as template to find matching window of the same size in the right side camera image
      * Uses sum of squared differences to identify most similar window
      * Takes center of matching window as PR
      * With PL and PR, finds difference between horizontal components as disparity
   * Finds Z (distance between camera center and point) by computing (focal length / physical size of pixel in camera center) * (Baseline dist. btw. left and right cameras / Disparity)
* hand_closed
   * Returns: boolean value, True if hand is closed, False if open
   * Uses mediapipe to determine state

**Arm_IK**
Use the existing Interbotix Python API 
* Python-ROS interface built on top of the Interbotix ROS interface 
  * Launch
    * ros2 launch interbotix_xsarm_control xsarm_control.launch.py robot_model:=wx250s
  *  Input
      * 3D hand location in the world frame (same as robot frame) from get_3d_hand_location
 * Functions
    * set_ee_pose_components(x, y, z)
      * moves the end effector to a pose, IK solved for us
    * gripper.open() / gripper.close()
      * driven by hand_closed
    * go_to_home_pose()
      * returns the arm to its home position

 

## Simulation

We want to use the simulator made by Trossen Robotics that runs in ROS Gazebo to test our code before running it on the real arm. This is so that we can verify our code works and won’t damage the arm or move in a way that could be unsafe, as well as allowing us to test code while other teams are using the arm.

## Camera system

To capture video feed of the user’s hand, we will be using a RealSense D435 parallel stereo camera. We will perform intrinsic calibration with [OpenCV’s camera calibration code](https://docs.opencv.org/4.13.0/dc/dbb/tutorial_py_calibration.html), and perform extrinsic calibration (depth estimation) by template matching and calculating similarity.

We are considering either mounting the camera on a frame so it points downwards onto a table, or having it point horizontally at the user.

## Project Goals

### Updated MVP and Stretch Goals

Our MVP remains the same from our initial proposal, which is to get the robot arm to match human movements using computer vision to a reasonable degree of precision, enough to consistently pick up and move basic objects.

Our primary stretch goal is to improve precision to perform more complex tasks, like playing an Operation-style game or assembling a sandwich.

### Milestone 2 Plan

For Milestone 2, we intend to have our MVP working in simulation, with our program reliably identifying a user’s hand position and using inverse kinematics to recreate that position with the simulated WidowX arm.

### Considerations and Challenges

Some risks to reaching this milestone include:
* Compatibility: The simulator uses an older version of Ubuntu and different ROS distributions
* The physical robot arm cannot lift very high
* Latency
