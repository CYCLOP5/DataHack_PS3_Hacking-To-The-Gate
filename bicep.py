import cv2
import numpy as np
import mediapipe as mp
import time

left_count = -1
right_count = -1
set_count = 0
rep_count = 0
last_curl_time = time.time()
set_start_time = time.time()
last_curl_angle = None
last_curl_time = None


def calc_angle(a, b, c):
    """
    a shoulder
    b elbow
    c wrist

    ab bc angle
    """
    a = np.array([a.x, a.y])
    b = np.array([b.x, b.y])
    c = np.array([c.x, c.y])

    ab = np.subtract(a, b)
    bc = np.subtract(b, c)

    theta = np.arccos(
        np.dot(ab, bc) / np.multiply(np.linalg.norm(ab), np.linalg.norm(bc))
    )
    theta = 180 - 180 * theta / 3.14
    return np.round(theta, 2)


def infer():
    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose
    both_flag = None
    both_count = 0

    cap = cv2.VideoCapture(0)
    pose = mp_pose.Pose(min_detection_confidence=0.7, min_tracking_confidence=0.5)
    while cap.isOpened():
        _, frame = cap.read()

        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False

        results = pose.process(image)

        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        try:
            landmarks = results.pose_landmarks.landmark
            left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]
            left_elbow = landmarks[mp_pose.PoseLandmark.LEFT_ELBOW]
            left_wrist = landmarks[mp_pose.PoseLandmark.LEFT_WRIST]
            right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER]
            right_elbow = landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW]
            right_wrist = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST]

            left_angle = calc_angle(left_shoulder, left_elbow, left_wrist)
            right_angle = calc_angle(right_shoulder, right_elbow, right_wrist)

            cv2.putText(
                image,
                str(left_angle),
                tuple(
                    np.multiply([left_elbow.x, left_elbow.y], [640, 480]).astype(int)
                ),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (255, 255, 255),
                2,
                cv2.LINE_AA,
            )
            cv2.putText(
                image,
                str(right_angle),
                tuple(
                    np.multiply([right_elbow.x, right_elbow.y], [640, 480]).astype(int)
                ),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (255, 255, 255),
                2,
                cv2.LINE_AA,
            )

            if left_angle > 160 and right_angle > 160:
                both_flag = "down"
                last_curl_angle = None
                last_curl_time = time.time()

            if (left_angle < 50 or right_angle < 50) and both_flag == "down":
                both_count += 1
                both_flag = "up"
                current_time = time.time()
                time_diff = current_time - last_curl_time
                last_curl_time = current_time
                rep_count += 1
                print("Rep count:", rep_count)
                if rep_count % 6 == 0:
                    set_count += 1
                    print("Set count:", set_count)
                    set_time_diff = current_time - set_start_time
                    set_start_time = current_time
                    print("Time between sets:", set_time_diff)
                    cv2.putText(
                        image,
                        "Set Count: " + str(set_count),
                        (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (255, 255, 255),
                        2,
                        cv2.LINE_AA,
                    )
                    cv2.putText(
                        image,
                        "Rep Count: " + str(rep_count),
                        (10, 60),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (255, 255, 255),
                        2,
                        cv2.LINE_AA,
                    )
                    angle_diff = abs(last_curl_angle - left_angle)
                    work = angle_diff / 360.0  #  1 rep = 360 degrees
                    power = work / time_diff
                    print("Power:", power)

                last_curl_angle = left_angle

        except:
            pass

        cv2.rectangle(image, (0, 0), (1024, 73), (10, 10, 10), -1)
        if both_flag == "down":
            cv2.putText(
                image,
                "Curl=" + str(both_count),
                (10, 60),
                cv2.FONT_HERSHEY_SIMPLEX,
                2,
                (255, 255, 255),
                2,
                cv2.LINE_AA,
            )
        else:
            cv2.putText(
                image,
                "both flag=" + str(both_flag),
                (10, 120),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 255, 255),
                2,
                cv2.LINE_AA,
            )

        mp_drawing.draw_landmarks(
            image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS
        )

        cv2.imshow("hey i ned", image)

        if cv2.waitKey(10) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    infer()
