from flask import Flask,render_template,Response
import cv2
import mediapipe as mp

app=Flask(__name__)


def generate_frames(camera,mphand,hand,mpdraw):
    while True:
            
        ## read the camera frame
        success,frame=camera.read()

        # start
        framer = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hand.process(framer)

        if result.multi_hand_landmarks:
            for handlms in result.multi_hand_landmarks:
                mpdraw.draw_landmarks(frame, handlms, mphand.HAND_CONNECTIONS)
                sum1 = 0
                for id, lm in enumerate(handlms.landmark):

                    h, w, c = frame.shape
                    cx , cy = int(lm.x*w), int(lm.y*h)
                    print(id,cx,cy)

                    if id==3:
                        c3x = cx
                        c3y = cy

                    if id==4:
                        c4x = cx
                        c4y = cy
                        cv2.circle(frame, (cx, cy), 10,(255,0,255),cv2.FILLED )
                        if c4y<c3y-20:
                            sum1=sum1+1
                    if id==7:
                        c7x = cx
                        c7y = cy

                    if id==8:
                        c8x = cx
                        c8y = cy
                        cv2.circle(frame, (cx, cy), 10, (255, 0, 255), cv2.FILLED)
                        cv2.line(frame, (c4x, c4y), (c8x, c8y), (69, 255, 0), 3)
                        if c8y<c7y:
                            sum1=sum1+1

                    if id==11:
                        c11x = cx
                        c11y = cy

                    if id==12:
                        c12y = cy
                        cv2.line(frame, (c4x, c4y), (cx, cy), (69, 255, 0), 3)
                        if c12y<c11y:
                            sum1=sum1+1
                    if id==15:
                        c15x = cx
                        c15y = cy

                    if id == 16:
                        c16y = cy
                        cv2.line(frame, (c4x, c4y), (cx, cy), (69, 255, 0), 3)
                        if c16y<c15y:
                            sum1=sum1+1

                    if id==19:
                        c19x = cx
                        c19y = cy

                    if id == 20:
                        c20y = cy
                        cv2.line(frame, (c4x, c4y), (cx, cy), (69, 255, 0), 3)
                        if c20y<c19y:
                            sum1=sum1+1

                        cv2.putText(frame,str(sum1),(10,70),cv2.FONT_HERSHEY_PLAIN,3,(255,0,255),3)



        #end

        ret,buffer=cv2.imencode('.jpg',frame)
        frame=buffer.tobytes()

        yield(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video')
def video():
    camera=cv2.VideoCapture(0)
    mphand = mp.solutions.hands
    hand = mphand.Hands()
    mpdraw = mp.solutions.drawing_utils
    mp_face_draw = mp.solutions.drawing_styles
    return Response(generate_frames(camera,mphand,hand,mp_face_draw,mpdraw),mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__=="__main__":
    app.run(debug=True)
