import numpy as np
import face_recognition
import cv2
import os
from datetime import datetime, timedelta
import pandas as pd

from db_psycopg2 import WorkingTimeDatabase


now_date = datetime.now().strftime('%Y-%m-%d')
events_file_path = f'database_with_events/events_{now_date}.csv'
if not os.path.isfile(events_file_path):
    start_df = pd.DataFrame({'time': [], 'name': [], 'event_type': []})
    start_df.to_csv(events_file_path, index=False)

train_path = 'train_images'

images = []
classes = []
myList = os.listdir(train_path)


for cls in myList:
    curImg = cv2.imread(f'{train_path}/{cls}')
    images.append(curImg)
    classes.append(os.path.splitext(cls)[0])


def find_encodings(images_to_encode):
    encode_list = []
    for image in images_to_encode:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(image)[0]
        encode_list.append(encode)
    return encode_list


encode_list_of_known_faces = find_encodings(images)
print("Программа готова к работе")

cap = cv2.VideoCapture(0)

while True:
    database = WorkingTimeDatabase()

    success, img = cap.read()
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    faces_cur_frame = face_recognition.face_locations(imgS)
    encode_cur_frame = face_recognition.face_encodings(imgS, faces_cur_frame)

    for encode_face, face_loc in zip(encode_cur_frame, faces_cur_frame):
        matches = face_recognition.compare_faces(encode_list_of_known_faces, encode_face)
        face_distances = face_recognition.face_distance(encode_list_of_known_faces, encode_face)
        match_index = np.argmin(face_distances)

        if matches[match_index]:
            name = classes[match_index]
            y1, x2, y2, x1 = face_loc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

            database.write_event_to_csv(name, 'entrance')  # entrance or exit
            # database.write_event_to_csv(name, 'exit')  # entrance or exit

    cv2.imshow("WebCam", img)
    cv2.waitKey(10)
