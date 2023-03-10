# Импортируем необходимые библиотеки

import cv2
import dlib
from scipy.spatial import distance
import time


img_descriptor = []
detector = dlib.cnn_face_detection_model_v1("mmod_human_face_detector.dat")
sp = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
facerec = dlib.face_recognition_model_v1('dlib_face_recognition_resnet_model_v1.dat')

def get_descript():
    img = cv2.imread('path to image')
    dets = detector(img)
    for k, d in enumerate(dets):
        print("Detection {}: Left: {} Top: {} Right: {} Bottom: {}".format(
            k, d.rect.left(), d.rect.top(), d.rect.right(), d.rect.bottom()))
        shape = sp(img, d.rect)
        img_descriptor.append(facerec.compute_face_descriptor(img,  shape))


# Создаем функцию для обнаружения человека на видео
def detect_person_in_video():
    # Открываем видео
    video = cv2.VideoCapture(0)
    video.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  # Ширина кадров в видеопотоке.
    video.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    video.set(cv2.CAP_PROP_FPS, 30)
    prev_frame_time = 0
    # used to record the time at which we processed current frame
    new_frame_time = 0


    while True:
        tr, image = video.read()
        dets = detector(image)
        # font which we will be using to display FPS
        font = cv2.FONT_HERSHEY_SIMPLEX
        # time when we finish processing for this frame
        new_frame_time = time.time()

        fps = 1 / (new_frame_time - prev_frame_time)
        prev_frame_time = new_frame_time

        # converting the fps into integer
        fps = int(fps)

        # converting the fps to string so that we can display it on frame
        # by using putText function
        fps = str(fps)
        cv2.putText(image, fps, (7, 70), font, 3, (0, 255, 0), 3, cv2.LINE_AA)

        for i, det in enumerate(dets):
            cv2.rectangle(image, (det.rect.left(), det.rect.top()), (det.rect.right(), det.rect.bottom()), [0, 255, 0], 4)
            shape = sp(image, det.rect)
            face_descriptor = facerec.compute_face_descriptor(image, shape)
            if (distance.euclidean(img_descriptor[0], face_descriptor) < 0.6):
                cv2.putText(image, "person",
                            (det.rect.left(), det.rect.bottom() + 25),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            1,
                            (255, 255, 255),
                            4
                            )
            else:
                cv2.putText(image, "unknow",
                            (det.rect.left(), det.rect.bottom() + 25),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            1,
                            (0, 0, 255),
                            4
                            )

        # Для показа результата на видео
        cv2.imshow("detect_person_in_video is running", image)

        k = cv2.waitKey(20)
        # Закрываем видео по нажатию клавиши "q"
        if k == ord("q"):
            print("Q pressed, closing the app")
            break

get_descript()
detect_person_in_video()



