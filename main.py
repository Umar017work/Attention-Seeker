import cv2
import mediapipe as mp
import time

from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from ffpyplayer.player import MediaPlayer

# Initialize MediaPipe Face Landmarker
base_options = python.BaseOptions(model_asset_path='face_landmarker.task')
options = vision.FaceLandmarkerOptions(
    base_options=base_options,
    output_face_blendshapes=False,
    output_facial_transformation_matrixes=False,
    num_faces=1)
detector = vision.FaceLandmarker.create_from_options(options)

# Constants
NOSE_TIP_IDX = 1
LEFT_CHEEK_IDX = 234
RIGHT_CHEEK_IDX = 454
DISTRACTION_TIMEOUT = 1.0  # seconds
MEME_VIDEO_PATH = 'Cat_Vibing_To_Ievan_Polkka_Official_Video_HD_Cat_Vibing_To_Music_Cat_Vibing_Meme_720P.mp4'

# State
is_paying_attention = True
last_seen_time = time.time()
meme_cap = None
meme_player = None

def get_meme_frame():
    global meme_cap, meme_player
    if meme_cap is None or not meme_cap.isOpened():
        meme_cap = cv2.VideoCapture(MEME_VIDEO_PATH)
        meme_player = MediaPlayer(MEME_VIDEO_PATH)
    
    ret, frame = meme_cap.read()
    if not ret:
        # Loop the video
        meme_cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        ret, frame = meme_cap.read()
        if meme_player is not None:
            meme_player.close_player()
            meme_player = MediaPlayer(MEME_VIDEO_PATH)
            
    if meme_player is not None:
        audio_frame, val = meme_player.get_frame()
        
    return frame

quit_clicked = False

def mouse_callback(event, x, y, flags, param):
    global quit_clicked
    # Check if click is within the quit button area
    if event == cv2.EVENT_LBUTTONDOWN:
        # Button coords: x from 20 to 140, y from 20 to 60
        if 20 <= x <= 140 and 20 <= y <= 60:
            quit_clicked = True

def start_app():
    global is_paying_attention, last_seen_time, meme_cap, meme_player, quit_clicked

    cv2.namedWindow('Attention Seeker')
    cv2.setMouseCallback('Attention Seeker', mouse_callback)

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    print("Attention Seeker started. Press 'q' to quit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame. Exiting...")
            break

        # Flip frame horizontally for a mirror effect
        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
        
        results = detector.detect(mp_image)
        currently_attentive = False

        if results.face_landmarks:
            landmarks = results.face_landmarks[0]
            
            # Simple heuristic for head rotation like we used in JS
            nose_x = landmarks[NOSE_TIP_IDX].x
            left_cheek_x = landmarks[LEFT_CHEEK_IDX].x
            right_cheek_x = landmarks[RIGHT_CHEEK_IDX].x

            dist_left = abs(nose_x - left_cheek_x)
            dist_right = abs(right_cheek_x - nose_x)
            
            # Avoid division by zero
            if dist_right > 0.0001:
                ratio = dist_left / dist_right
                # If nose is too close to either cheek, head is turned
                is_looking_away = ratio < 0.4 or ratio > 2.5
                if not is_looking_away:
                    currently_attentive = True
                    last_seen_time = time.time()
            else:
                 # Extreme turn where right cheek and nose align horizontally 
                 pass

        current_time = time.time()
        
        # Determine attention state
        if not currently_attentive:
            if (current_time - last_seen_time) > DISTRACTION_TIMEOUT:
                is_paying_attention = False
        else:
            is_paying_attention = True

        # Render output
        display_frame = frame
        
        if not is_paying_attention:
            # Play meme video
            meme_frame = get_meme_frame()
            if meme_frame is not None:
                # Resize meme frame to fit webcam window
                meme_frame = cv2.resize(meme_frame, (frame.shape[1], frame.shape[0]))
                display_frame = meme_frame
                
                # Overlay Text warning
                cv2.putText(display_frame, "🚨 ATTENTION LOST", (50, 50), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3)
        else:
            # Show normal webcam and positive status
            if meme_cap is not None:
                meme_cap.release()
                meme_cap = None
            if meme_player is not None:
                meme_player.close_player()
                meme_player = None
                
            # Draw semi-transparent background for text
            overlay = display_frame.copy()
            cv2.rectangle(overlay, (40, 80), (380, 140), (0, 0, 0), -1)
            cv2.addWeighted(overlay, 0.5, display_frame, 0.5, 0, display_frame)
            
            cv2.putText(display_frame, "👀 Paying Attention", (50, 120), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2, cv2.LINE_AA)

        # Draw Quit Button Overlay
        button_color = (60, 60, 220) # BGR
        cv2.rectangle(display_frame, (20, 20), (140, 60), button_color, -1)
        cv2.rectangle(display_frame, (20, 20), (140, 60), (255, 255, 255), 2)
        cv2.putText(display_frame, "QUIT (Q)", (35, 47), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2, cv2.LINE_AA)

        cv2.imshow('Attention Seeker', display_frame)

        # Handle quit
        if cv2.waitKey(1) & 0xFF == ord('q') or quit_clicked:
            break

    cap.release()
    if meme_cap is not None:
         meme_cap.release()
    if meme_player is not None:
         meme_player.close_player()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    start_app()
