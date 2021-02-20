##Nathan Hinton
##This file will provide a user interface for the people who will use it

run = True
state = 'init'
while run == True:
    if state == 'init':
        lastState = state
        print("\n=== Welcome! ===")
        print("Starting menu...")
        state = 'welcome'
############################################################
    elif state == 'welcome':
        lastState = state
        print('\nWhat would you like to do?')
        print('(1) Generate verse files and URL for video')
        print('(2) Generate srt files for D&C')
        print('(3) Generate a SRT file for your own video')
        print('(4) Generate srt files for the BOok of Mormon')
        i = input('Enter the number then press enter: ')
        if i == '1':
            state = 'URL'
        elif i == '2':
            state = 'D&C'
        elif i == '3':
            state = 'genOwn'
        elif i == '4':
            state = 'BofM'
        else:
            state = 'error'
############################################################
    elif state == 'URL':
        lastState = state
        print('\ninitalizing...')
        try:
            import m01generateVerseAndVideoURL
            print('finished!')
            state = 'welcome'
        except:
            state = 'error'
############################################################
    elif state == 'D&C':
        lastState = state
        print('\ninitalizing...')
        try:
            import m02captionFromURL
            print('finished!')
            state = 'welcome'
        except:
            state = 'error'
############################################################
    elif state == 'genOwn':
        lastState = state
        print('\ninitalizing...')
        print("WARNING! This is not developed...")
        try:
            import m03testingManualCaptioning
            print('finished!')
            state = 'welcome'
        except:
            state = 'error'
############################################################
    elif state == 'BofM':
        lastState = state
        print('\ninitalizing the Book of Mormon caption converter...')
        try:
            from m04bookOfMormonConverter import BofMConvert
            filePath = input('what is the file path of the SRT from the disk? ')
            fileName = input('What is the name of the file? ')
            convert = BofMConvert(filePath, fileName)
            if convert.status == 'Pass':
                convert.run()
                state = 'welcome'
            else:
                print(convert.status)
                state = 'error'
        except:
            state = 'error'
############################################################
    elif state == 'error':
        print('\nSorry, something did not work. Try checking your input to make sure that it is correct.')
        print('Do you want to resume current work?')
        print('(1) Yes, I want to try again.')
        print('(2) No, I want to ge back to main menu.')
        i = input('Enter the number then press enter: ')
        if i == '1':
            state = lastState
        elif i == '2':
            state = 'welcome'
        else:
            state = 'error'
############################################################
    else:
        print("\nTHERE WAS AN UNKNOWN ERROR!")
        print("Dump of vars: state = %s, lastState = %s"%(state, lastState))
        print("Something happened that was unexpected. The program will now restart...")
        state = 'init'


