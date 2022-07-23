
import time
import cv2
from pyzbar.pyzbar import decode
import pyzbar.pyzbar as pyzbar
import httplib2
import os



def off():
	os.system("nmcli radio wifi off")

def on():
    os.system("nmcli radio wifi on")

        
def connect(ssid,password=""):
	if password=="":
		print(f"nmcli dev wifi connect {ssid}")
		os.system(f"nmcli dev wifi connect {ssid}")
	else:
		os.system(f"nmcli dev wifi connect {ssid} password {password}")        


def share(opt=""):
	if opt == "qr":
		os.system("nmcli dev wifi show-password")
		sh=0
	elif opt =="psk" or opt =="password" or  opt =="paskey":
		l = os.popen("nmcli dev wifi show-password").read()
		sh=l.split("\n")[2].split(":")[1]
	else:
		sh=os.popen("nmcli dev wifi show-password").read()
	return sh


def current_wifi():
    info = share()
    # print(type(info))
    if len(info) != 0:
        info = info.split("\n")
        # print(info)
        namein = info[0]
        nameinfo = namein.split(":")
        namewifi = nameinfo[-1]
        # print(name)
    return namewifi

   

def wifi_check():
    host = httplib2.HTTPConnectionWithTimeout("www.google.com",timeout=3)

    try:
        host.request("HEAD","/")
        host.close()
        return True
    except Exception as e:

        return False
  

   
def findWifi(cred):
    data = str(cred)
    data = data[2:-1]
    wifi = data.split(";")
    name = wifi[0]
    name = name.split(":")
    SSID = name[-1]
    #print("SSID:- ",SSID)
    Sec = wifi[1]
    Sec = Sec.split(":")
    Security_Type = Sec[-1]
    #print("Security Type:-", Security_Type)
    passw = wifi[2]
    passw = passw.split(":")
    Password = passw[-1]
    #print("Password:- ",Password)
    return SSID , Security_Type , Password
    

def box(Qr):
    x = Qr[0].rect[0]
    y = Qr[0].rect[1]
    w = Qr[0].rect[2]
    h = Qr[0].rect[3]
    return x,y,w,h

off()
cap = cv2.VideoCapture(0)
wifi_status = wifi_check()

# if wifi_status == False:
#     wifi.on()

#detector = cv2.QRCodeDetector()
while cap.isOpened():
    ret,frame = cap.read()
    frame = cv2.flip(frame,1) 
    wifi_status = wifi_check()
   
    # if wifi_status == True:
    #     currentWifi = current_wifi()
    #     print(currentWifi)

    Qr = decode(frame)
    if len(Qr) != 0:
        x,y,w,h = box(Qr)
        cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,255),3)


        # print("Detected")
    

    for obj in Qr:
        ssid, sec_type, password = findWifi(obj.data)
        # print(ssid,sec_type,password)
        cv2.putText(frame,"SSID:- "+ ssid,(400,50),cv2.FONT_ITALIC,0.5,(0,0,0),1)
        cv2.putText(frame,"Password:- "+ password,(400,75),cv2.FONT_ITALIC,0.5,(0,0,0),1)
        cv2.putText(frame,"Security Type:-  "+ sec_type,(400,100),cv2.FONT_ITALIC,0.5,(0,0,0),1)
        # print("detected")

        if  wifi_status == False:
            print("Connecting to wifi")
            on()
            connect(ssid,password)
            time.sleep(5)
            info = share()
            if len(info) != 0:
        
                info = info.split("\n")
                    # print(info)
                namein = info[0]
                nameinfo = namein.split(":")
                currentwifi = nameinfo[-1]
                print("connected to:-",currentwifi)
        else:
            print("Already connected to:-",ssid)    
            
                
           
            


        
        
    
    cv2.imshow("frame", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()