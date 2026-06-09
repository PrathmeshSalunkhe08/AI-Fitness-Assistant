import cv2
from module_posture.posture_state import posture_state

from module_posture.bicep_curl import analyze_bicep
from module_posture.shoulder_press import analyze_shoulder_press
from module_posture.squat import analyze_squat
from module_posture.pushup import analyze_pushup

def generate_frames():
    cap = cv2.VideoCapture(0)

    reps = 0
    last_exercise = None  # 🔑 THIS FIXES EVERYTHING

    while True:
        success, frame = cap.read()
        if not success:
            break

        exercise = posture_state["exercise"]

        # 🔄 RESET WHEN EXERCISE CHANGES
        if exercise != last_exercise:
            reps = 0
            last_exercise = exercise

        if exercise == "bicep":
            frame, reps, feedback, wrong = analyze_bicep(frame, reps)

        elif exercise == "shoulder":
            frame, reps, feedback, wrong = analyze_shoulder_press(frame, reps)

        elif exercise == "squat":
            frame, reps, feedback, wrong = analyze_squat(frame, reps)

        elif exercise == "pushup":
            frame, reps, feedback, wrong = analyze_pushup(frame, reps)

        else:
            wrong = False
            feedback = ""

        posture_state["wrong"] = wrong
        posture_state["feedback"] = feedback
        posture_state["reps"] = reps

        cv2.putText(frame, f"Reps: {reps}",
                    (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1, (0, 255, 0), 2)

        ret, buffer = cv2.imencode(".jpg", frame)
        frame = buffer.tobytes()

        yield (b"--frame\r\n"
               b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n")
