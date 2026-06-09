import cv2
import mediapipe as mp
from .utils import calculate_angle

mp_pose = mp.solutions.pose
mp_draw = mp.solutions.drawing_utils

pose = mp_pose.Pose(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

stage = None  # up / down


def analyze_pushup(frame, reps):
    global stage

    wrong = False
    feedback = ""

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = pose.process(rgb)

    if result.pose_landmarks:
        lm = result.pose_landmarks.landmark

        shoulder = lm[mp_pose.PoseLandmark.RIGHT_SHOULDER]
        elbow    = lm[mp_pose.PoseLandmark.RIGHT_ELBOW]
        wrist    = lm[mp_pose.PoseLandmark.RIGHT_WRIST]
        hip      = lm[mp_pose.PoseLandmark.RIGHT_HIP]

        elbow_angle = calculate_angle(shoulder, elbow, wrist)

        # ---------------- BODY ORIENTATION CHECK ----------------
        body_horizontal = abs(shoulder.y - hip.y) < 0.12

        if not body_horizontal:
            wrong = True
            feedback = "Get into push-up position"
            stage = None

        # ---------------- PUSH-UP REP LOGIC ----------------
        if body_horizontal and not wrong:

            if elbow_angle > 155:
                stage = "up"

            elif elbow_angle < 95 and stage == "up":
                stage = "down"
                reps += 1

        # ---------------- VISUAL FEEDBACK ----------------
        color = (0, 0, 255) if wrong else (0, 255, 0)

        mp_draw.draw_landmarks(
            frame,
            result.pose_landmarks,
            mp_pose.POSE_CONNECTIONS,
            mp_draw.DrawingSpec(color=color, thickness=3),
            mp_draw.DrawingSpec(color=color, thickness=3)
        )

        cv2.putText(
            frame,
            f"Elbow Angle: {int(elbow_angle)}",
            (20, 80),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.1,
            (0, 255, 255),
            3
        )

        posture_text = "WRONG FORM" if wrong else "GOOD FORM"
        posture_color = (0, 0, 255) if wrong else (0, 255, 0)

        cv2.putText(
            frame,
            posture_text,
            (20, 130),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.1,
            posture_color,
            3
        )

    return frame, reps, feedback, wrong
