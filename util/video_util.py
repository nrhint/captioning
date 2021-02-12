##
import cv2
import pytesseract
import time

from data.Subtitle import Subtitle

#
def readTextFromVideo(url, prefix):

    result = Subtitle

    cap = cv2.VideoCapture(url)# + '.mp4')
    fps = cap.get(cv2.CAP_PROP_FPS)  # OpenCV2 version 2 used "CV_CAP_PROP_FPS"
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = frame_count / fps

    print('fps = ' + str(fps))
    print('number of frames = ' + str(frame_count))
    print('duration (S) = ' + str(duration))
    minutes = int(duration / 60)
    seconds = duration % 60
    print('duration (M:S) = ' + str(minutes) + ':' + str(seconds))
    # Display the resulting frame
    frameWidth = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frameHeight = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    print('frame (W:H) = ' + str(frameWidth) + ':' + str(frameHeight))

    timestamps = [cap.get(cv2.CAP_PROP_POS_MSEC)]
    calc_timestamps = [0.0]

    #cap.set(cv2.CV_CAP_PROP_FPS, 600)

    startProcess = time.time()#Use for speed testing

    lastText = ""

    for f in range(0, frame_count, int(fps * 10)):
        '''
    Ideas for improvment:
    Having the captions 10 seconds apart is not that great. It would be better if
    they were closer together. One option is to increase the number of frames
    checked while that would work but that will take longer. Another option is to
    keep going 10 seconds but then when it changes go back 5 seconds then change
    by 2.5 seconds then go by 1.25 seconds then finally go by 0.625. This is 5
    iterations and would be much faster than going through more frames. This would
    add 5 times the frames but aldo you couls adjust the algroythm to make it so
    that you are reading every 100 frames if you are careful and make sure that
    you do not skip verses.
        '''

        cap.set(1, f)
    #while(cap.isOpened()):
        # Capture frame-by-frame
        ret, frame = cap.read()

        if ret == True:

            # Convert the image to gray scale
            ####pytesseract does not reccognise the text right if the image is a grayscale. Removed unneeded action. There is also little to no time difference between the grayscale and the color image passed into pytesserace####
            #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 
            
            # Performing OTSU threshold 
            #ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV) 

            # Specify structure shape and kernel size.  
            # Kernel size increases or decreases the area  
            # of the rectangle to be detected. 
            # A smaller value like (10, 10) will detect  
            # each word instead of a sentence. 
            #rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 18)) 
            
            # Appplying dilation on the threshold image 
            #dilation = cv2.dilate(thresh1, rect_kernel, iterations = 1) 
            
            # Finding contours 
            #contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE) 

            # Extracted text is then written into the text file 
            #for cnt in contours: 
                #x, y, w, h = cv2.boundingRect(cnt) 
                #print("x: " + str(x) + ",y: " + str(y) + ",w: " + str(w) + ",h: " + str(h))
                
                # Drawing a rectangle on copied image 
                #rect = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2) 
                
                # Cropping the text block for giving input to OCR 
            #cropped = frame[y:y + h, x:x + w]
            cropped = frame[50:200, 850:1150]

                # Open the file in append mode 
                #file = open("recognized.txt", "a") 
                
                # Apply OCR on the cropped image 
            newText = pytesseract.image_to_string(cropped) 
            print(newText)
            if prefix in newText and lastText != newText:
                if ':' in newText:
                    print(newText + "\t" + convertTime(cap.get(cv2.CAP_PROP_POS_MSEC) / 1000))
                    print(f)
                    times.append(convertTime(cap.get(cv2.CAP_PROP_POS_MSEC) / 1000))#append the timestamp
                    lastText = newText
                elif newText[-1] == 'H':
                    times.append['0:0:0,000']#If the verse is the heading the timestamp should start at the very beginning of the video.


        # Break the loop
        else:
            times.append(convertTime(duration))#Append the end timestamp
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()

    endProcess = time.time()

    print('It took %s seconds to process the video'%(endProcess-startProcess))

    return result