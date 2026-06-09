import cv2
import mediapipe as mp
from .utils import calculate_angle

mp_pose = mp.solutions.pose
mp_draw = mp.solutions.drawing_utils

pose = mp_pose.Pose(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

stage = "up"   # up / down
def analyze_squat(frame, reps):
    global stage

    wrong = False
    feedback = ""

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = pose.process(rgb)

    if not result.pose_landmarks:
        cv2.putText(frame, "Stand in view", (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        return frame, reps, "Stand in view", True

    lm = result.pose_landmarks.landmark

    shoulder = lm[mp_pose.PoseLandmark.RIGHT_SHOULDER]
    hip      = lm[mp_pose.PoseLandmark.RIGHT_HIP]
    knee     = lm[mp_pose.PoseLandmark.RIGHT_KNEE]
    ankle    = lm[mp_pose.PoseLandmark.RIGHT_ANKLE]

    knee_angle = calculate_angle(hip, knee, ankle)
    hip_below_knee = hip.y > knee.y

    # ---------------- BAD FORM CHECKS ----------------
    if abs(shoulder.x - hip.x) > 0.30:
        wrong = True
        feedback = "Keep your chest upright"

    elif abs(knee.x - ankle.x) > 0.15:
        wrong = True
        feedback = "Keep knees aligned with toes"

    elif knee_angle > 100 and hip_below_knee:
        wrong = True
        feedback = "Go lower for full squat"

    # ---------------- REP LOGIC ----------------
    if not wrong:
        if knee_angle < 95 and hip_below_knee:
            stage = "down"

        elif knee_angle > 165 and stage == "down":
            reps += 1
            stage = "up"

    # ---------------- DRAW ----------------
    color = (0, 0, 255) if wrong else (0, 255, 0)

    mp_draw.draw_landmarks(
        frame,
        result.pose_landmarks,
        mp_pose.POSE_CONNECTIONS,
        mp_draw.DrawingSpec(color=color, thickness=3),
        mp_draw.DrawingSpec(color=color, thickness=3)
    )

    cv2.putText(frame, f"Reps: {reps}", (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    cv2.putText(frame, f"Knee Angle: {int(knee_angle)}", (20, 80),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 3)

    cv2.putText(frame,
                "WRONG FORM" if wrong else "GOOD FORM",
                (20, 130),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.1,
                color,
                3)

    # 🔴 SHOW FEEDBACK WHEN WRONG
    if wrong:
        cv2.putText(frame, feedback, (20, 180),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 0, 255),
                    3)

    return frame, reps, feedback, wrong
