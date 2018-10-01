# Simple python script to demonstrate queue implementation for sendind data to a webserver read via serial port or any other input source
from queue import Queue
from threading import Thread
import time
import requests #python -m pip install requests

# Set up some global variables
THREAD_COUNT = 1
API_ENDPOINT = "<URL for storing the data>"
dataQueue = Queue()


def postData(i, q):  
    while True:
        print('Looking for the next input')
        number = q.get()
        print('Sending Number: ', number)
        requestParams = {
            'number': number           
        }        
        response = requests.get(API_ENDPOINT, requestParams)         
        print('Server Response Status: ', response.status_code)
        if(response.status_code != 200):
            q.put(number)
        q.task_done()
        

# Set up some threads to fetch the enclosures
for i in range(THREAD_COUNT):
    worker = Thread(target=postData, args=(i, dataQueue,))
    worker.setDaemon(True)
    worker.start()

#Data can be read from serial port as well
while True:
    dataQueue.put(str(int(time.time())))
    time.sleep(2)

# Now wait for the queue to be empty, indicating that we have
# processed all of the downloads.
print ('*** Main thread waiting')
dataQueue.join()
print ('*** Complete Queue Processed')
