import cv2 as cv
import serial



def send(byte):
	if (ser.isOpen()):
		print("send ok")
		ser.write(byte.encode('utf-8'))
	else:
		print('send no')


def is_inside(o,i):
    
    ox, oy, ow, oh =o
    ix, iy, iw, ih =i
    return ox >ix and oy >iy and ox + ow < ix +iw and oy + oh < iy + ih
def draw_person(image,person):
    
    x,y,w,h=person
    cv.rectangle(image,(x,y),(x+w,y+h),(0,255,255),2)


cap = cv.VideoCapture(0)
cap.set(3,320)
cap.set(4,240)
i = 0

ser = serial.Serial('../dev/ttyUSB0',115200)

while(cap.isOpened()):
	Vshow = cap.read()
	i = i+1
	if i == 30:	
		i = 0
		img = cv.bilateralFilter(Vshow[1],10,35,40)
		#img = cv.medianBlur(frame, 3)
		#img = cv.GaussianBlur(frame,(5,5),0)
		hog=cv.HOGDescriptor()
		hog.setSVMDetector(cv.HOGDescriptor_getDefaultPeopleDetector())
		found, w = hog.detectMultiScale(img)
		found_filtered=[]
		for ri, r in enumerate(found): 
		     for qi,q in enumerate(found):
		         if ri !=qi and is_inside(r,q):
		             break
		         else:
		             found_filtered.append(r)
		for person in found_filtered:
		     draw_person(img,person)
		     
		
		print(len(found))
		cv.imshow("Cap_test",img)
		cv.waitKey(0)

		if (len(found)):
			send('1')
		else:
			send('0')
			

		
ser.close()
cap.release()
cv.destroyAllWindows()
