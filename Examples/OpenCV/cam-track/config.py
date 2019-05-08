# cam-track-py version 1.1 configuration file
# For Non RPI platforms like Windows or Unix (non RPI)
# set WEBCAM = True since no RPI camera will be avail
#-----------------------------------------------------------------------------------------------

# Global Variable Settings
# ========================

window_on = True      # True=Display OpenCV Windows (GUI desktop reqd) False=Terminal Only
verbose = False         # True=Turn on logging messages False=Turn Off logging messages
loggingToFile = False  # if verbose=True then send logging messages to a log file (cam-track.log)
log_only_moves = True  # Log True=Only Cam Moves False=All
fps_on = True         # Display fps (not implemented)

# Sets the maximum x y pixels that are allowed to reduce effect of objects moving in frame
cam_move_x = 50        # Max number of x pixels in one move
cam_move_y = 25         # Max number of y pixels in one move

vid_from_file = False  # Make sure you edit CAMERA_WIDTH and HEIGHT to suit vid size
vid_path = '/home/pi/cam-track/cam-track-1.mp4'   # Specifies path of video to use.

# Camera Settings
# ===============
WEBCAM = False        # default = False False=PiCamera True=USB WebCamera

# Web Camera Settings
# -------------------
WEBCAM_SRC = 0        # default= 0   USB opencv connection number
WEBCAM_WIDTH = 320    # default= 320 USB Webcam Image width
WEBCAM_HEIGHT = 240   # default= 240 USB Webcam Image height
WEBCAM_HFLIP = False  # default= False USB Webcam flip image horizontally
WEBCAM_VFLIP = True  # default= False USB Webcam flip image vertically

# Pi Camera Settings
# ------------------
CAMERA_WIDTH = 320    # default= 320 Pi Camera Image width
CAMERA_HEIGHT = 240   # default= 240 Pi Camera Image width
CAMERA_HFLIP = False  # default= False pi Camera image horiz flip
CAMERA_VFLIP = False   # default= False pi Camera image vert flip
CAMERA_ROTATION = 0   # default= 0  Rotate pi Camera image 0, 90, 180, 270 only valid values
CAMERA_FRAMERATE = 4  # default= 35 framerate of video stream. 
                      # Can be 100+ with new R2 RPI camera module
FRAME_COUNTER = 1000  # default= 1000 image counter for reporting fps

# OpenCV Settings
# ---------------
show_search_rect = True  # show outline of current search box on main window
show_search_wind = False # True=Show search_rect GUI window  False=Window not Shown
show_circle = True       # Show a circle otherwise show bounding rectangle on window
CIRCLE_SIZE = 3          # diameter of circle to show location in window
WINDOW_BIGGER = 2.0      # Increase the display window size multiplier default=2.0
LINE_THICKNESS = 1       # Thickness of bounding line in pixels default=1
CV_FONT_SIZE = .25       # size of font on opencv window default=.25
red = (0,0,255)          # opencv line colours
green = (0,255,0)
blue = (255,0,0)

# OpenCV MatchTemplate Settings
# -----------------------------
MAX_SEARCH_THRESHOLD = .96 # default=.97 Accuracy for best search result of search_rect in stream images
MATCH_METHOD = 3
            # Valid MatchTemplate COMPARE_METHOD Int Values
            # ---------------------------------------------
            # 0 = cv2.TM_SQDIFF  = 0
            # 1 = cv2.TM_SQDIFF_NORMED = 1
            # 2 = cv2.TM_CCORR = 2
            # 3 = cv2.TM_CCORR_NORMED = 3    Default
            # 4 = cv2.TM_CCOEFF = 4
            # 5 = cv2.TM_CCOEFF_NORMED = 5
            #
            # For other comparison methods 
            # see http://docs.opencv.org/3.1.0/d4/dc6/tutorial_py_template_matching.html

# Search rectangle variables
# Calculated from other variable values
# -------------------------------------
image_cx = int(CAMERA_WIDTH/2)   # x center of image
image_cy = int(CAMERA_HEIGHT/2)  # y center of image
sw_w = int(CAMERA_WIDTH/4)       # search window width
sw_h = int(CAMERA_HEIGHT/4)      # search window height
sw_buf_x = int(sw_w/4)           # buffer to left/right of image
sw_buf_y = int(sw_h/4)           # buffer to top/bot of image
sw_x = int(image_cx - sw_w/2)    # top x corner of search rect
sw_y = int(image_cy - sw_h/2)    # top y corner of search rect
sw_xy = (sw_x,sw_y)              # initialize cam position tracker
