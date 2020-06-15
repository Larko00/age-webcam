import cv2
import requests
import time
from PIL import Image

capture = cv2.VideoCapture(0)
img_counter = 0

age = "N/A"
score = "N/A"
bbox = "N/A"
h_class = "N/A"


while(True):
     
    ret, frame = capture.read()

    if cv2.waitKey(1) == 27:
        break
    elif cv2.waitKey(1) == 32:
        img_name = "opencv_frame_{}.png".format(img_counter)
        cv2.imwrite("frame.png", frame)
        #print("{} written!".format(img_name))
        img_counter += 1

        # API REQUEST #
        client_id = '1t6QOQlElGzIOiEwAeIUw9iO'
        client_secret = 'VienftVyXRIZ8gh0zsYl830g0GEORlBDXk2V5jZcxkFurBIT'
        with open(f'frame.png','rb') as image:
            data = {'data': image}
            quality = requests.post('https://api.everypixel.com/v1/faces', files=data, auth=(client_id, client_secret)).json()
            #r_keywords = requests.post('https://api.everypixel.com/v1/keywords', files=data, auth=(client_id, client_secret)).json()
        print(quality)
        #print(r_keywords)

        faces = quality['faces']
        #keywords = r_keywords['keywords']
        #print(keywords[0])
        for item in faces:
            age = item['age']
            score = item['score']
            bbox1 = int(item['bbox'][0])
            bbox2 = int(item['bbox'][1])
            bbox3 = int(item['bbox'][2])
            bbox4 = int(item['bbox'][3])
            h_class = item['class']
        #print(bbox1)
        cv2.rectangle(frame, (bbox1, bbox2), (bbox3, bbox4), (0, 255, 0), 1) 
        # API REQUEST #

    #cv2.imwrite('frame.png', frame)

    # TEXT ON SCREEN
    cv2.putText(frame, f"Age : {age}", (0,20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0)) 
    cv2.putText(frame, f"Score : {score}", (0,40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0)) 
    cv2.putText(frame, f"Class : {h_class}", (0,60), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0)) 
    # TEXT ON SCREEN

    #cv2.putText(frame, f"Image counter : {img_counter}", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0)) 
    # SHOW THE LIVEFEED
    cv2.imshow('video', frame)


capture.release()
cv2.destroyAllWindows()