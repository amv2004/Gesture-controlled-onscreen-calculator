import cv2 as cv
from cvzone.HandTrackingModule import HandDetector
from time import sleep

cap=cv.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)
detector=HandDetector(detectionCon=0.8)
expr=""
res=""
keys=[['1','2','3','+'],['4','5','6','-'],['7','8','9','*'],['C','0','=','/']]
buttons=[]
class Button():
    def __init__(self,pos,text,size=[85,85]):
        self.pos=pos
        self.text=text
        self.size=size
for i in range(len(keys)):
    for j,key in enumerate(keys[i]):
        buttons.append(Button([j*100+50,i*100+50],key))
def draw(img,buttons,expr,res):
    for b in buttons:
        x,y=b.pos
        w,h=b.size
        cv.rectangle(img,b.pos,(x+w,y+h),(0,255,255),cv.FILLED)
        cv.putText(img,b.text,(x+20,y+65),cv.FONT_HERSHEY_PLAIN,4,(255,255,255),4)
    cv.rectangle(img,(50,475),(450,550),(50,50,50),cv.FILLED)
    cv.putText(img,expr,(60,525),cv.FONT_HERSHEY_PLAIN,4,(255,255,255),4)
    cv.rectangle(img,(50,575),(450,650),(0,0,255),cv.FILLED)
    cv.putText(img,res,(60,625),cv.FONT_HERSHEY_PLAIN,4,(255,255,255),4)
    return img
while True:
    _,img=cap.read()
    hands,img=detector.findHands(img,draw=True)
    img=draw(img,buttons,expr,res)
    if hands:
        lmList=hands[0]['lmList']
        for b in buttons:
            x,y=b.pos
            w,h=b.size 
            if x<lmList[8][0]<x+w and y<lmList[8][1]<y+h:
                cv.rectangle(img,b.pos,(x+w,y+h),(0,255,0),cv.FILLED)
                cv.putText(img,b.text,(x+20,y+65),cv.FONT_HERSHEY_PLAIN,4,(255,255,255),4)
                l,_,_=detector.findDistance(lmList[8][:2],lmList[12][:2],img)
                if l<30:
                    if b.text=='=':
                        try:
                            res=str(eval(expr))
                        except:
                            res="Error"
                    elif b.text=='C':
                        res=""
                        expr=""
                    else:
                        expr+=b.text
                    cv.rectangle(img,b.pos,(x+w,y+h),(255,255,0),cv.FILLED)
                    cv.putText(img,b.text,(x+20,y+65),cv.FONT_HERSHEY_PLAIN,4,(255,255,255),4)
                    sleep(1)
    cv.imshow('Calculator',img)
    if cv.waitKey(1) & 0xff==ord('x'):
        break
cap.release()
cv.destroyAllWindows()
                        
