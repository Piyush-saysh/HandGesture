import cv2 
import mediapipe as mp 
import time 




class HandDetector():
    def __init__(self):
        self.mp_hand = mp.solutions.hands 
        self.hands = self.mp_hand.Hands() #this class only use rgb # 
        self.mp_points = mp.solutions.drawing_utils

    def check_hand(self, img):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.result = self.hands.process(imgRGB)
        # print(imgRGB)
        # print(result.multi_hand_landmarks)
        if self.result.multi_hand_landmarks:
                for handlandmark in self.result.multi_hand_landmarks:
                        # if id == 0:
                            # cv2.circle(img, (cx,cy),70,(255,0,255),cv2.FILLED)
                    self.mp_points.draw_landmarks(img, handlandmark,self.mp_hand.HAND_CONNECTIONS)
        return img
    def find_position(self, img, handNo= 0):
        lm_list = []
        if self.result.multi_hand_landmarks:
            my_hand = self.result.multi_hand_landmarks[handNo]    
            for id , lm in enumerate(my_hand.landmark):
                # print(id, lm)
                h, w, c = img.shape
                cx , cy = int(lm.x * w), int(lm.y *h) #for getting location of hand
                lm_list.append([id,cx,cy])
                # print(id, cx, cy )
        return lm_list


def main():
    cap = cv2.VideoCapture(0)
    detector = HandDetector()
    while True:
        success, img = cap.read()
        img = detector.check_hand(img)
        lm_list = detector.find_position(img)
        # if len(lm_list) != 0:
        #     print(lm_list)

        cv2.imshow("image", img)
        if cv2.waitKey(2) & 0xFF ==ord('q'):
            break

if __name__ == "__main__":
    main()