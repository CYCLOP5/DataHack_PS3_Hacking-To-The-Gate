import cv2
import mediapipe as mp
import squatpaks as sp
import tensorflow as tf
import numpy as np
from utils import landmarks_list_to_array, label_params, label_final_results

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

model = tf.keras.models.load_model("working_model_1")


class VideoCamera(object):
    def __init__(self):
        # self.video = cv2.VideoCapture(0)
        self.video = cv2.VideoCapture("/home/cyclops/Desktop/datahon/squats.mp4")

    def __del__(self):
        self.video.release()


def gen(camera):
    cap = camera.video
    i = 0
    reps = 0
    sets = 1
    prev_rep_time = 0
    with mp_pose.Pose(
        min_detection_confidence=0.4,  # more lenient for  squat coz squats are very hard lmao
        min_tracking_confidence=0.4,
    ) as pose:
        while cap.isOpened():
            success, image = cap.read()
            image = cv2.flip(image, 1)

            if not success:
                print("empty camera frame.")
                break

            image_height, image_width, _ = image.shape

            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False

            dim = (image_width // 5, image_height // 5)

            resized_image = cv2.resize(image, dim)

            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            results = pose.process(resized_image)

            params = sp.get_params(results)
            flat_params = np.reshape(params, (5, 1))

            output = model.predict(flat_params.T)

            output[0][0] *= 0.7
            output[0][1] *= 1.7
            output[0][2] *= 4
            output[0][3] *= 0
            output[0][4] *= 5

            output = output * (1 / np.sum(output))

            output_name = ["c", "k", "h", "r", "x", "i"]

            output[0][2] += 0.1

            # print(output[0][2], output[0][3])

            label = ""
            for i in range(1, 4):
                label += output_name[i] if output[0][i] > 0.5 else ""

            if label == "":
                label = "c"

            label += "x" if output[0][4] > 0.15 and label == "c" else ""

            label_final_results(image, label)

            i += 1

            mp_drawing.draw_landmarks(
                image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS
            )

            coords = landmarks_list_to_array(results.pose_landmarks, image.shape)
            label_params(image, params, coords)
            if label == "k":
                reps += 1
                if reps == 1:
                    prev_rep_time = cv2.getTickCount()
                elif reps == 6:
                    sets += 1
                    reps = 0
                    current_rep_time = cv2.getTickCount()
                    time_diff = (
                        current_rep_time - prev_rep_time
                    ) / cv2.getTickFrequency()
                    prev_rep_time = current_rep_time
                    print("Set:", sets)
                    print("Time taken between reps:", time_diff, "seconds")
            cv2.imshow("Posture", image)
            if cv2.waitKey(10) & 0xFF == ord("q"):
                break

        cap.release()
        cv2.destroyAllWindows()


gen(VideoCamera())
