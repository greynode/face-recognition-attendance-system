from flask import Flask,Response, render_template
import base64
import cv2
import face_recognition
import numpy as np

app = Flask(__name__)
@app.route('/')
def gen():
    
    videoc = cv2.VideoCapture(0)


    krish_image = face_recognition.load_image_file("C:/Users/Lenovo/OneDrive - Kumaraguru College of Technology/Desktop/fr/Picture2.png")
    krish_face_encoding = face_recognition.face_encodings(krish_image)[0]


    known_face_encodings = [
    krish_face_encoding]
    
    known_face_names = [
    "bharath"
    ]

    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True
    

    while True:
  
        ret, frame = videoc.read()

   
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        
        rgb_small_frame = small_frame[:, :, ::-1]

      
        if process_this_frame:
     
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:
      
                matches = face_recognition.compare_faces(known_face_encodings, face_encodings)
                name = "Unknown"

   
                face_distances = face_recognition.face_distance(known_face_encodings, face_encodings)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]

                face_names.append(name)

        process_this_frame = not process_this_frame


       
        for (top, right, bottom, left), name in zip(face_locations, face_names):
   
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

         
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

      
        cv2.imshow('Video', frame)
        ret, jpeg = cv2.imencode('.jpg',frame)
        frame = jpeg.tobytes()
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

       
        videoc.release()
        cv2.destroyAllWindows()
        frame = jpeg.tobytes()
        yield (b'--frame\r\n'
        b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/snap')
def snap():
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        cap.release()
        imgst = base64.b64encode(frame)
        print(imgst)
        return imgst 

@app.route('/video_feed')
def video_feed():
    return Response(gen(),
                        mimetype='multipart/x-mixed-replace; boundary=frame')
            
if __name__== "__main__":
    app.run(port=5000, debug=True)
