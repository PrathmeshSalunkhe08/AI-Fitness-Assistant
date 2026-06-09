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


def analyze_bicep(frame, reps):
    global stage

    wrong = False
    feedback = "Keep your elbow close to your body"

    # Mirror view
    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = pose.process(rgb)

    if result.pose_landmarks:
        lm = result.pose_landmarks.landmark

        # Landmarks
        shoulder = lm[mp_pose.PoseLandmark.RIGHT_SHOULDER]
        elbow = lm[mp_pose.PoseLandmark.RIGHT_ELBOW]
        wrist = lm[mp_pose.PoseLandmark.RIGHT_WRIST]

        # Angle calculation
        angle = calculate_angle(shoulder, elbow, wrist)

        # ================= WRONG POSTURE CHECK =================
        if abs(elbow.x - shoulder.x) > 0.12:
            wrong = True
            stage = None  # stop rep cheating

        # ================= REP COUNT =================
        if not wrong:
            if angle > 160:
                stage = "down"
            elif angle < 40 and stage == "down":
                stage = "up"
                reps += 1

        # ================= DRAW SKELETON =================
        color = (0, 0, 255) if wrong else (0, 255, 0)

        mp_draw.draw_landmarks(
            frame,
            result.pose_landmarks,
            mp_pose.POSE_CONNECTIONS,
            mp_draw.DrawingSpec(color=color, thickness=3, circle_radius=3),
            mp_draw.DrawingSpec(color=color, thickness=3)
        )

        # ================= ANGLE TEXT (NO BACKGROUND) =================
        # Outline (for visibility)
        cv2.putText(
            frame,
            f"Elbow Angle: {int(angle)}",
            (20, 80),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.2,
            (0, 0, 0),
            5,
            cv2.LINE_AA
        )

        # Main text
        cv2.putText(
            frame,
            f"Elbow Angle: {int(angle)}",
            (20, 80),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.2,
            (0, 255, 255),
            3,
            cv2.LINE_AA
        )

        # ================= POSTURE STATUS TEXT =================
        posture_text = "WRONG FORM" if wrong else "GOOD FORM"
        posture_color = (0, 0, 255) if wrong else (0, 255, 0)

        cv2.putText(
            frame,
            posture_text,
            (20, 130),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.1,
            posture_color,
            3,
            cv2.LINE_AA
        )

    return frame, reps, feedback, wrong
