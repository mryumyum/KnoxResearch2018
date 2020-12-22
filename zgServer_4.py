from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit

import time
import serial
import eventlet
eventlet.monkey_patch()

app = Flask(__name__)
socketio = SocketIO(app, async_mode = 'eventlet')

@app.route('/')
def home():
	return(render_template('zgTCT_2.html'))

@socketio.on('sendNumber')
def on_sendNumber(json):
    print('received json: ' + str(json))

@socketio.on('connect')
def test_connect():
    print("Website is connected!")
	
@app.route("/send", methods=['POST'])
def send():
	if request.method == 'POST':
		temp = request.form['temp']
		ser = serial.Serial(port='COM1', baudrate=19200, timeout=5)
		print('Serial port opened')
		time.sleep(2)
		cmdToSend = '<SV,'+temp+'>'
		print('Writing: ', cmdToSend)
		ser.write(str(cmdToSend).encode())
		time.sleep(1)
		ser.flush()
		bytesToRead = ser.inWaiting()
		readOut = ser.read(bytesToRead).decode('utf-8')
		time.sleep(1)
		print('readOut = ', readOut)
		return(render_template('zgTCT_2.html', temp = temp))
		
	else:
		return('Please go back and enter a command...', 400)

@socketio.on('reqUpdate')
def on_reqUpdate():
	ser = serial.Serial(port='COM1', baudrate=19200, timeout=5)
	time.sleep(2)
	readOut = ser.read(bytesToRead).decode('utf-8')
	print('Received update request from client')
	jsonData = '{"currentTemp":"' + str(readOut) + '"}'
	print("Current Temp = ", jsonData)
	emit('updated', jsonData)
		
if __name__ == "__main__":
    socketio.run(app, debug=True)