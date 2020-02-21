import socket
import sys
import requests
import requests_oauthlib
import json
import datetime
import time

ACCESS_TOKEN = 'access_token_here'

def get_heartbeat():
    t1 = datetime.datetime.now() + datetime.timedelta(hours=2)
    t1 = str(t1)[11:16]
    
    t2 = datetime.datetime.now() + datetime.timedelta(hours=2) - datetime.timedelta(minutes=20)
    t2 = str(t2)[11:16]
    url = "https://api.fitbit.com/1/user/7LNTMS/activities/heart/date/today/1d/1sec/time/"+t2+"/"+t1+".json"
    headers = {
        'Content-type': "application/x-www-form-urlencoded",
        'cache-control': "no-cache",
        'Authorization': "Bearer "+ ACCESS_TOKEN
        }
    response = requests.request("GET", url, headers=headers)
    print(response)
    return(response)

def get_avg_heartbeat():
    url = "https://api.fitbit.com/1/user/7LNTMS/activities/heart/date/2019-06-26/1d/1sec.json"
    headers = {
        'Content-type': "application/x-www-form-urlencoded",
        'cache-control': "no-cache",
        'Authorization': "Bearer "+ ACCESS_TOKEN
        }
    response = requests.request("GET", url, headers=headers)
    for line in response.iter_lines():
    	values = json.loads(line)
    	avg_HR = values['activities-heart'][0]['value']['restingHeartRate']
    return(avg_HR)

def send_heartbeat_to_spark(http_resp, tcp_connection):
    for line in http_resp.iter_lines():
        values = json.loads(line)
        hr_dataset = values['activities-heart-intraday']['dataset']
        for i in hr_dataset:
            time.sleep(1)
            flag = False
            if (i['value'] <= lower_HR or i['value'] >= upper_HR):
                flag = True
            time_value = ''+i['time']+" "+str(i['value']) + " " +str(flag)
            print((time_value + '\n').encode())
            print ("------------------------------------------")
            try:
                tcp_connection.send((time_value+'\n').encode())
                print("Data Sent")
            except:
                e = sys.exc_info()[0]
                print("Error: %s" % e)

avg_HR = get_avg_heartbeat()  
upper_HR = avg_HR*2.5
lower_HR = avg_HR/1.5

TCP_IP = "localhost"
TCP_PORT = 45001
conn = None
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)
print("Waiting for TCP connection...")
conn, addr = s.accept()
print("Connected... Starting getting Heart Rate.")
while True:
    time.sleep(1)
    resp = get_heartbeat()
    send_heartbeat_to_spark(resp, conn)

#while True:
#    time.sleep(5)
#    resp = get_heartbeat()
#    #send_heartbeat_to_spark(resp, conn)
#    for line in resp.iter_lines():
#        values = json.loads(line)
#        hr_dataset = values['activities-heart-intraday']['dataset']
#        for i in hr_dataset:
#            time.sleep(1)
#            flag = False
#            if (i['value'] <= lower_HR or i['value'] >= upper_HR):
#                flag = True
#            time_value = ''+i['time']+" "+str(i['value']) + " " +str(flag)
#            print((time_value + '\n').encode())
#            print ("------------------------------------------")
#            try:
#                conn.send(str(time_value).encode())
#                print("Data Sent")
#            except:
#                e = sys.exc_info()[0]
#                print("Error: %s" % e)


