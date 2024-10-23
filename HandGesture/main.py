from re import X
from tkinter import W
import cv2 
import numpy as np
import handtraking_module as htm
import math
import time
import osascript
import pyautogui as pg
from subprocess import call

#############################################################

#############################################################
wCam, hCam = 640, 480
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
detector = htm.HandDetector()
screen_width=1512.0
screen_height=982.0
frame_r = 100
smoothing =5
ploc_x ,ploc_y =0,0
cloc_x, cloc_y =0,0
count = 0
count_screen =0
#############################################################

##############################################################
def fingerup(lm_list):
    finger_up = []
    if lm_list[4][1] >= lm_list[2][1]:
        finger_up.append(1)
    else:
        finger_up.append(0)
    tip_num = [8,12,16,20]
    for i in tip_num:
        if lm_list[i][2] <= lm_list[i-2][2]:
            finger_up.append(1)
        else:
            finger_up.append(0)
    return finger_up
##############################################################

#############################################################

while True:
    success, img = cap.read()
    img = detector.check_hand(img)
    img = cv2.flip(img,1)

    lm_list = detector.find_position(img)
    if len(lm_list) !=0:
        finger_up = fingerup(lm_list)
        
#############################################################
#curser 
#############################################################
        x1,y1 = lm_list[8][1], lm_list[8][2]
        x2,y2 = lm_list[12][1], lm_list[12][2]
        length = math.hypot(x2-x1,y2-y1)
        if finger_up[1] ==1 and sum(finger_up) == 1:
            cv2.rectangle(img,(frame_r,frame_r),(wCam - frame_r,hCam - frame_r),(255,0,0), 2)
            cv2.circle(img, (x1,y1), 10,(0,255,0), cv2.FILLED)

            x3 = np.interp(x1,(frame_r,wCam-frame_r),(0,screen_width))
            y3 = np.interp(y1,(frame_r,hCam-frame_r),(0,screen_height))
            cloc_x = ploc_x +(x3 - ploc_x) / smoothing 
            cloc_y = ploc_y +(y3 - ploc_y) / smoothing 

            pg.moveTo(screen_width - cloc_x,cloc_y)
            ploc_x, ploc_y = cloc_x,cloc_y

        if finger_up[1] ==1 and finger_up[2] ==1 and sum(finger_up) ==2 and length>50:
            pg.click(button='left')
        if finger_up[1] ==1 and finger_up[2] ==1 and sum(finger_up) ==2 and x2>=x1:
            pg.scroll(1) 
        if finger_up[1] ==1 and finger_up[2] ==1 and finger_up[0] ==1 and sum(finger_up) ==3 and x2>=x1:
            pg.scroll(-1) 
        if finger_up[1] ==1 and finger_up[2] ==1 and finger_up[0]==1 and x2< x1 and sum(finger_up) ==3:
            pg.click(button='right')
            
#############################################################
# video recoder  --- spider man 
#############################################################

        screen_rec = '''tell application "QuickTime Player"
                        activate
                        set newScreenRecording to new screen recording
                            tell newScreenRecording
                                start
                                delay 10 
                                stop
                            end tell
                        end tell'''
        if finger_up[1] ==1 and finger_up[4]==1 and sum(finger_up) ==2:
            count +=1
            print(count)
            if count > 20:
                osascript.osascript(screen_rec)
                count =0

#############################################################
#Screenshots --- open
#############################################################

        if sum(finger_up)==5:
            count+=1
            print(count)
            if count >= 20:
                count_screen +=1
                cmd = 'do shell script "screencapture ~/Desktop/screenshot'+str(int(time.time()))+'.png"'
                # # cmd = 'do shell script "screencapture ~/Desktop/screenshot'+str(count_screen)+'.png"'
                # cmd = 'do shell script "screencapture ~/Desktop/screenshot.png"' q
                osascript.osascript(cmd)
                dia = 'display dialog "ss taken successfully" with title "Alert"'
                osascript.osascript(dia)
                print("success")
                # call(["screencapture", "screenshot.jpg"])
                count=0

#############################################################
#brithness   ---- sum = 4 -- sum = 3 
#############################################################

        bright_inc = '''
                tell application "System Events"
                    key code 144
                end tell
                '''
        bright_dec = '''
                tell application "System Events"
                    key code 145
                end tell
                '''
        if finger_up[0] == 0 and sum(finger_up) ==4:
            count+=1
            if count > 20:
                dia = 'display dialog "Brightness inc successfully" with title "Alert"'
                osascript.osascript(bright_inc)
                osascript.osascript(dia)
                count=0

        if finger_up[0] ==0 and finger_up[1] ==0 and sum(finger_up) ==3:
            count+=1
            if count>20:
                dia = 'display dialog "Brightness dec successfully" with title "Alert"'
                osascript.osascript(bright_dec)
                osascript.osascript(dia)
                count=0

#############################################################
#volume    thump or index 
#############################################################

        if finger_up[0] ==1 and finger_up[1]==1 and sum(finger_up) ==2:
            x0,y0 = lm_list[4][1], lm_list[4][2]
            x1, y1 = lm_list[8][1], lm_list[8][2]
            cv2.circle(img, (x0,y0), 10,(255,0,0), cv2.FILLED)
            cv2.circle(img, (x1,y1), 10,(255,0,0), cv2.FILLED)
            cv2.line(img, (x0,y0),(x1,y1),(0,255,0),3)
            count+=1
            print(count)
            if count > 20:
                length = math.hypot(x1-x0,y1-y0)
                vol = np.interp(length,[0,100],[0,100])
                set_vol = "set volume output volume " + str(vol)
                count = 0 

#############################################################

    cv2.imshow('Img',img)
    if cv2.waitKey(4) & 0xFF == ord("q"):
        break
