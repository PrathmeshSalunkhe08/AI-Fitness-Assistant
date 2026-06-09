import cv2
import mediapipe as mp
from .utils import calculate_angle

mp_pose = mp.solutions.pose
mp_draw = mp.solutions.drawing_utils

pose = mp_pose.Pose(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

stage = None  # down / up


def analyze_shoulder_press(frame, reps):
    global stage

    wrong = False
    feedback = "Press your arms straight up"

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = pose.process(rgb)

    if result.pose_landmarks:
        lm = result.pose_landmarks.landmark

        shoulder = lm[mp_pose.PoseLandmark.RIGHT_SHOULDER]
        elbow    = lm[mp_pose.PoseLandmark.RIGHT_ELBOW]
        wrist    = lm[mp_pose.PoseLandmark.RIGHT_WRIST]

        angle = calculate_angle(shoulder, elbow, wrist)

        # ❌ WRONG FORM
        if angle < 60:
            wrong = True
            stage = None

        # ✅ REP COUNT (SAME AS BICEP LOGIC)
        if not wrong:
            if angle < 90:
                stage = "down"
            elif angle > 160 and stage == "down":
                stage = "up"
                reps += 1

        color = (0, 0, 255) if wrong else (0, 255, 0)

        mp_draw.draw_landmarks(
            frame,
            result.pose_landmarks,
            mp_pose.POSE_CONNECTIONS,
            mp_draw.DrawingSpec(color=color, thickness=3),
            mp_draw.DrawingSpec(color=color, thickness=3)
        )

        cv2.putText(frame, f"Elbow Angle: {int(angle)}",
                    (20, 80),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1.1, (0, 255, 255), 3)

        cv2.putText(frame,
                    "WRONG FORM" if wrong else "GOOD FORM",
                    (20, 130),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1.1,
                    (0, 0, 255) if wrong else (0, 255, 0),
                    3)

    return frame, reps, feedback, wrong
