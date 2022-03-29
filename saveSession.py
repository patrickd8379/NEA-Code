import pygame, sys, math, os, main, leaderboardScreen, pauseMenu

def saveToLeaderboard(track, fastestLapString, setup):
    saving = True
    notSaving = False
    userName = ""
    leaderboard = open(track.leaderboard, "r+")

    if fastestLapString == "": #If no time was set
        notSaving = True

    while notSaving:
        main.screen.fill(main.blue)
        main.drawText("No valid laps were set in that session", main.font, main.black, main.screen, 200, 250)

        click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        mx, my = pygame.mouse.get_pos()

        endText = main.font.render("End Session", True, (0, 0, 0))
        endButton = pygame.Rect(main.screenWidth/2-100, 300, 200, 50)

        if endButton.collidepoint((mx, my)):
            pygame.draw.rect(main.screen, main.yellowDark, endButton)
            if click == True:
                notSaving = False
                displayLeaderboard(track, leaderboard, None, setup) #Go to the leaderboard with no new laps set
        else:
            pygame.draw.rect(main.screen, main.yellow, endButton)

        main.screen.blit(endText, (endButton.center[0]-60, endButton.center[1]-10))
        pygame.display.flip()
        main.clock.tick(60)

    while saving:
        main.screen.fill(main.blue)
        main.drawText("Save session to leaderboard", main.font, main.black, main.screen, 20, 20)
        main.drawText("Enter a user name", main.font, main.black, main.screen, main.screenWidth/2-100, 100)

        click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE and len(userName) > 0:
                    userName = userName [:-1]
                else:
                    userName += event.unicode

        userName = userName[:15]

        submitButton = pygame.Rect(main.screenWidth/2-100, 300, 200, 50)
        submitText = main.font.render("Submit", True, (0, 0, 0))

        userNameText = main.font.render(userName, True, (0, 0, 0))
        userNameBox = userNameText.get_rect()

        mx, my = pygame.mouse.get_pos()

        if submitButton.collidepoint((mx, my)):
            pygame.draw.rect(main.screen, main.yellowDark, submitButton)
            if click == True:
                if len(userName) < 1:
                    userName = "Unnamed"
                leaderLaps = leaderboard.readlines() #Get all the laps
                leaderLaps = [lap.rstrip("\n") for lap in leaderLaps] #Remove \ns from each line
                leaderLaps = [lap[5:] for lap in leaderLaps] #Start each line from the start of the lap time
                leaderboard.seek(0)
                leaderboard.truncate() #Empty the leaderboard
                positionFound = False
                position = 0
                totalLap = pauseMenu.getTotalLap(fastestLapString) #The integer value of the lap set in the session
                if len(leaderLaps) < 1: #If there are no previous times to compare to
                    positionFound = True
                else:
                    while positionFound == False and position < len(leaderLaps):
                        currentLap = leaderLaps[position].split(" | ") #The lap at that point in the leaderboard
                        currentLap = pauseMenu.getTotalLap(currentLap[0]) #Find the integer value of the lap time
                        if totalLap < currentLap and positionFound == False: #If the lap that has just been set is faster than the current lap on the leaderboard
                            positionFound = True
                        else:
                            position += 1
                #Insert the new lap at its position in the leaderboard
                leaderLaps.insert(position, str(fastestLapString + " | " + userName+ " | " + str(setup[0]) + str(setup[1]) + str(setup[2]) + str(setup[3]) + str(setup[4]) + str(setup[5])))
                leaderBoardPos = 1
                while len(leaderLaps) > 0: #While there are laps to add to the leaderboard
                    if leaderBoardPos < 10: #For single digit numbers
                        print(leaderLaps[0])
                        leaderboard.write(str(leaderBoardPos) + "  | " + leaderLaps[0] + "\n") #Put the lap into the leaderboard
                    else:
                        leaderboard.write(str(leaderBoardPos) + " | " + leaderLaps[0] + "\n")
                    leaderLaps.remove(leaderLaps[0])
                    leaderBoardPos += 1
                leaderboard.close()
                #Create a sting for the fastest lap in the session to show when viewing the leaderboard
                if position < 9:
                    sessionFastest = str(str(position+1) + "  | " + fastestLapString + " | " + userName+ " | " + str(setup[0]) + str(setup[1]) + str(setup[2]) + str(setup[3]) + str(setup[4]) + str(setup[5]))
                else:
                    sessionFastest = str(str(position+1) + " | " + fastestLapString + " | " + userName+ " | " + str(setup[0]) + str(setup[1]) + str(setup[2]) + str(setup[3]) + str(setup[4]) + str(setup[5]))
                leaderboardScreen.runLeaderboard(track, sessionFastest) #Show the leaderboard with the lap the user set
                saving = False
        else:
            pygame.draw.rect(main.screen, main.yellow, submitButton)

        main.screen.blit(submitText, (submitButton.center[0]-30, submitButton.center[1]-10))
        main.screen.blit(userNameText, ((main.screenWidth/2-userNameBox.width/2), (main.screenHeight/2-userNameBox.height/2)))
        pygame.display.flip()
        main.clock.tick(60)
