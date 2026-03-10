# Attention Seeker 👀

**Attention Seeker** is a fun Python Desktop Application powered by Computer Vision. The application monitors your webcam in real-time using Google's MediaPipe model to detect your face orientation. If you look away from the screen for more than **1 second**, the program immediately snaps back your attention by playing a loud meme video!

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![OpenCV](https://img.shields.io/badge/OpenCV-v4+-green.svg)
![MediaPipe](https://img.shields.io/badge/MediaPipe-Latest-orange.svg)

[![Open in GitHub Desktop](https://img.shields.io/badge/Open%20in-GitHub%20Desktop-563D7C?style=for-the-badge&logo=github)](https://desktop.github.com/open-in-desktop?repo=Umar017work/Attention-Seeker)
[![Open in VS Code](https://img.shields.io/badge/Open%20in-VS%20Code-007ACC?style=for-the-badge&logo=visual-studio-code)](vscode://vscode.git/clone?url=https://github.com/Umar017work/Attention-Seeker)

---

## ✨ Features
- **Real-Time Head Pose Tracking**: Calculates the relative distance between your nose tip and cheeks to instantly know if you've lost focus.
- **Immediate Interruption**: If you dare look away or hide your face, the app immediately overtakes your screen with an attention-grabbing meme video (complete with synchronized audio).
- **Smooth Recovery**: Glance back at the screen, and the meme instantly pauses, restoring your webcam feed.
- **Sleek Overlay UI**: Modern transparent text boxes and an interactive quit button built natively via OpenCV mouse callbacks.

## 🚀 Installation & Setup

### Prerequisites
1. Python 3.8+ installed on your system.
2. A built-in or USB webcam connected.
3. Your own funny/loud `.mp4` video (e.g., Cat Vibing Meme).

### Quick Start

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/Attention-Seeker.git
   cd "Attention-Seeker"
   ```

2. **Install the required libraries:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Download the MediaPipe Model:**
   The application requires the MediaPipe Face Landmarker model. It will either download automatically or you can download `face_landmarker.task` and place it in the root folder.

4. **Add your Alert Video:**
   Ensure you place an MP4 file in the folder and update the `MEME_VIDEO_PATH` constant inside `main.py` to match its exact filename.

5. **Run the Application:**
   ```bash
   python main.py
   ```

## 🎮 How to Use
- Once started, the camera window will launch.
- A glowing green **"👀 Paying Attention"** status lets you know the tracker has engaged.
- Turn your head! The window will replace your feed with the meme video.
- Click the red **"QUIT"** button in the top left corner or press `Q` on your keyboard to exit the app safely.

## 🛠️ Built With
- `opencv-python` - For video capture, overlay drawings, and GUI handling.
- `mediapipe` - For high-performance, on-device facial tracking.
- `ffpyplayer` - For synchronized audio playback with the OpenCV video frames.
