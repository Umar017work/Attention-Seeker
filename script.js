import { FaceLandmarker, FilesetResolver } from "https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision/vision_bundle.mjs";

const video = document.getElementById("webcam");
const alertVideo = document.getElementById("alert-video");
const statusText = document.getElementById("status");

let faceLandmarker;
let runningMode = "VIDEO";
let webcamRunning = false;
let lastWebcamTime = -1;

// State management
let isPayingAttention = true;
let lastSeenTime = Date.now();
const DISTRACTION_TIMEOUT = 1000; // 1 second

// Ensure the alert video can play with an initial UI interaction override if necessary
document.body.addEventListener("click", () => {
    alertVideo.play().then(() => alertVideo.pause()).catch(() => { });
}, { once: true });

// Initialize MediaPipe Face Landmarker
async function initializeFaceLandmarker() {
    statusText.innerText = "⏳ Loading AI Models...";
    try {
        const vision = await FilesetResolver.forVisionTasks(
            "https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision/wasm"
        );
        faceLandmarker = await FaceLandmarker.createFromOptions(vision, {
            baseOptions: {
                modelAssetPath: `https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/1/face_landmarker.task`,
                delegate: "GPU"
            },
            outputFaceBlendshapes: true,
            runningMode: runningMode,
            numFaces: 1
        });

        statusText.innerText = "📷 Waiting for Camera...";
        startCamera();
    } catch (error) {
        console.error(error);
        statusText.innerText = "❌ Error initializing AI";
    }
}

// Start User Webcam
async function startCamera() {
    try {
        const constraints = { video: true };
        const stream = await navigator.mediaDevices.getUserMedia(constraints);
        video.srcObject = stream;
        video.addEventListener("loadeddata", predictWebcam);
        webcamRunning = true;
    } catch (error) {
        console.error(error);
        statusText.innerText = "❌ Camera access denied";
    }
}

// Update UI state
function setAttentionState(isAttentive) {
    if (isAttentive === isPayingAttention) return; // No change

    isPayingAttention = isAttentive;

    if (isPayingAttention) {
        statusText.innerText = "👀 Paying Attention";
        statusText.className = "status-attention";
        alertVideo.classList.remove("active");
        alertVideo.pause();
    } else {
        statusText.innerText = "🚨 Attention Lost";
        statusText.className = "status-distracted";
        alertVideo.classList.add("active");
        alertVideo.play().catch(e => console.log("Autoplay prevented", e));
    }
}

// Main detection loop
async function predictWebcam() {
    if (video.currentTime !== lastWebcamTime) {
        lastWebcamTime = video.currentTime;

        const startTimeMs = performance.now();
        const results = faceLandmarker.detectForVideo(video, startTimeMs);

        let currentlyAttentive = false;

        if (results.faceLandmarks && results.faceLandmarks.length > 0) {
            const landmarks = results.faceLandmarks[0];
            const nose = landmarks[1];
            const leftCheek = landmarks[234];
            const rightCheek = landmarks[454];

            const distLeft = Math.abs(nose.x - leftCheek.x);
            const distRight = Math.abs(rightCheek.x - nose.x);
            const ratio = distLeft / (distRight || 0.0001);

            const isLookingAway = ratio < 0.4 || ratio > 2.5;

            if (!isLookingAway) {
                currentlyAttentive = true;
                lastSeenTime = Date.now();
            }
        }

        if (!currentlyAttentive) {
            if (Date.now() - lastSeenTime > DISTRACTION_TIMEOUT) {
                setAttentionState(false);
            }
        } else {
            setAttentionState(true);
        }
    }

    if (webcamRunning) {
        window.requestAnimationFrame(predictWebcam);
    }
}

// Start the app
initializeFaceLandmarker();
