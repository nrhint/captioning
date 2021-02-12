# captioning
captions the ASL videos for the book of mormon

<b>What the project does:</b>
  This is for adding captions fo the ASL Book of Mormon

<b>Why the project is useful:</b>
  This is usefuel because it will autogenerate the srt file then you cna batch un in the captions using another program or you can leave the files seperate. This will cut down on the time needed to caption each video as they are on average about 15 minuts long and captioning 60+ hours of video would take FOREVER.

<b>How users can get started with the project:</b>
  Eventaully this will be able to caption any video using a varity of methods. You can press a key to ste the timestamps for the captions of a videl. That way if you havd a play with a script then you could paste the script into a file then have enter seperated dialouge and the proram would take the timestamps of your key presses and allow you to add the captions for the speaker.

<b>Where users can get help with your project:</b>
  Right now, google... We do not have a lot of time so chances are google will have to help you

<b>Who maintains and contributes to the project:</b>
  Elder Hinton who is currently a missionary for The Church of Jesus Christ of Latter-day Saints is the founder of the idea and built the first prototype and draft. He then reached out to Ryan Hinton his dad for help and advice on how to proceed. Now a frind Brother Golf is helping with the coding and teaching Elder Hinton how to use git better.

<h1>Using the program:</h1><hr>
Starting off. This program has 3 parts. The test auto used an ocr to detect the changes in the text on the screen. This will automaticly mark down the timestamps. To use this you need to have pytesseract, pysecreenshot and pynput. You will need to open up the video in fullscreen and then press the 'p' key to start the timestampint. Every time the verse changes and at the end of the video press the 'v' key. Then when the video is over press the 'e' key. To do different videos you will need to open the main program and edit the filepath var and also edit the lenfth in the program. This will allow you to watch the video at a faster speed so that it does not take as long.