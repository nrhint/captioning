##Nathan Hinton
##This file will provide a user interface for the people who will use it

run = True
state = 'init'
while run == True:
    if state == 'init':
        lastState = state
        print("Welcome!")
        print("Starting menu...")
        state = 'welcome'
############################################################
    elif state == 'welcome':
        lastState = state
        print('What would you like to do?')
        print('(1) Generate srt files for D&C')
        print('(2) generate a SRT file for your own video')
        print('(3) convert a srt from the book of mormon disks')
        i = input('Enter the number then press enter: ')
        if i == '1':
            state = 'D&C'
        elif i == '2':
            state = 'genOwn'
        elif i == '3':
            state = 'BofM'
        else:
            state = 'error'
############################################################
    elif state == 'D&C':
        lastState = state
        print('initalizing...')
        import captionFromURL
        print('finished!')
        state = 'welcome'
############################################################
    elif state == 'genOwn':
        lastState = state
        print('initalizing...')
        print("WARNING! This is not developed...")
        import testingManualCaptioning
        print('finished!')
        state = 'welcome'
############################################################
    elif state == 'BofM':
        lastState = state
        print('initalizing the Book of Mormon caption converter...')
        from bookOfMormonConverter import BofMConvert
        filePath = input('what is the file path of the SRT from the disk? ')
        fileName = input('What is the name of the file? ')
        convert = BofMConvert(filePath, fileName)
        if convert.status == 'Pass':
            convert.run()
            state = 'welcome'
        else:
            print(convert.status)
            state = 'error'
############################################################
    elif state == 'error':
        print('Sorry, something did not work. Try checking your input to make sure that it is correct.')
        state = lastState
############################################################
    else:
        print("THERE WAS AN UNKNOWN ERROR!")
        print("Dump of vars: state = %s, lastState = %s"%(state, lastState))
        print("Something happened that was unexpected. The program will now restart...")
        state = 'init'


