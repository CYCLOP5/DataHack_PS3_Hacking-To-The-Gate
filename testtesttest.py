import cv2
import mediapipe as mp

mp_pose = mp.solutions.pose

bench_press_landmarks = [(11, 12, 13), (23, 24, 25), (19, 20, 21)]
pushup_landmarks = [(11, 12, 13), (23, 24, 25)]
bicep_curl_landmarks = [(15, 16, 17), (23, 24, 25)]
lateral_raise_landmarks = [(15, 16, 17), (23, 24, 25)]
shoulder_press_landmarks = [(11, 12, 13), (15, 16, 17)]
squat_landmarks = [(11, 12, 13), (23, 24, 25)]
triceps_pushdown_landmarks = [(19, 20, 21), (23, 24, 25)]

exercise_names = ["Bench press", "Push-up", "Bicep curl", "Lateral raise", "Shoulder press", "Squat", "Triceps pushdown"]

exercise_count = [0] * len(exercise_names)

exercise_states = ["Not performing", "Performing"]

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    with mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        results = pose.process(frame)

    if results.pose_landmarks:

        pose_landmarks = results.pose_landmarks.landmark

        exercise_performed = [False] * len(exercise_names)

        for i in range(len(bench_press_landmarks)):
            exercise_performed[i] = all(pose_landmarks[landmark].visibility > 0.5 for landmark in bench_press_landmarks[i])

        for i in range(len(exercise_names)):
            if exercise_performed[i]:
                exercise_states[i-1] = exercise_states[1]
                exercise_count[i] += 1

        exercise_states = exercise_performed

        i += 1

    for i in range(len(exercise_names)):
        cv2.putText(frame, exercise_names[i] + ": " + " (" + str(exercise_count[i]) + ")", (10, 20 + i * 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    cv2.imshow("Fitness Tracker", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()

cv2.destroyAllWindows()