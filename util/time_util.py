##

#
def convertTime(timeInSec):
    hr = int(timeInSec//(60*60))
    mn = int((timeInSec-(hr*60*60))//60)
    sec = int((timeInSec-((hr*60*60)+mn*60))//1)
    ms = str(round(timeInSec-int(timeInSec), 3))[2:]
    return "%s:%s:%s,%s"%(hr, mn, sec, ms)

def findFirstFound(cap, fps, prefix):
    times = []
    for f in range(0, frame_count, int(fps * max_time)):
        cap.set(1, f)
        ret, frame = cap.read()
        tempText = ''
        if ret == True:
            foundText = pytesseract.image_to_string(frame)
            matchText = findFirstPrefix(prefix, foundText)
            if tempText != matchText:
                print(newText + "\t" + convertTime(cap.get(cv2.CAP_PROP_POS_MSEC) / 1000))
                times.append(convertTime(cap.get(cv2.CAP_PROP_POS_MSEC) / 1000))#append the timestamp    