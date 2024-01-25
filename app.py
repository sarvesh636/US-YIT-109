from flask import Flask, render_template, Response
from camera import VideoCamera
import pymysql
import time
import pyautogui
import math

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'path',
    'cursorclass': pymysql.cursors.DictCursor
}


app = Flask(__name__)
@app.route('/')
def index():
    return render_template('hackathon.html')


def get_accelerometer_data():
    current_position = pyautogui.position()

    accel_data = {
        'x': current_position[0],
        'y': current_position[1],
    }

    return accel_data

def get_gyroscope_data():
    current_position = pyautogui.position()

    gyro_data = {
        'x': current_position[0],
        'y': current_position[1],
    }

    return gyro_data

def get_vibration_data():
    vibration_data = math.sin(time.time())  

    return vibration_data





@app.route('/new_page')
def new_page():

    print("Simulating Accelerometer, Gyroscope, and Vibration Sensor Data:")
    while True:
            accel_data = get_accelerometer_data()
            gyro_data = get_gyroscope_data()
            vibration_data = get_vibration_data()

            print(f"Accelerometer Data: {accel_data}")
            print(f"Gyroscope Data: {gyro_data}")
            print(f"Vibration Data: {vibration_data}")

            if accel_data['x'] >700:
                return render_template('index.html')
            else:
                time.sleep(2) 
        
    

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n'+frame+b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')



@app.route('/connect' ,methods=['GET'])
def connect():
       try:
            connection = pymysql.connect(**db_config)

            with connection.cursor() as cursor:
                sql = "SELECT * FROM location"
                cursor.execute(sql)

                data = cursor.fetchall()

            connection.close()

            result = [{'coordinates': [float(item['latitude']), float(item['longitude'])],'issue_type': item['issue_type']} for item in data]

            return render_template('connect.html', data=result)
       
       except Exception as e:
        return render_template('error.html', error=str(e))



if __name__ == '__main__':
    app.run(host="0.0.0.0",port="5000")
