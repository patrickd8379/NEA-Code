import pygame, sys, math, os, tracks, main, trackMenu
def runMainMenu():
    while True: #While on main menu
        click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT: #If the user quits the game
                pygame.quit() #End the program
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit() #End program if esc pressed
                    sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True #Left click on mouse is considered a click

        main.screen.fill(main.blue)
        main.drawText("Main Menu", main.font, main.black, main.screen, 20, 20)

        startButton = pygame.Rect((main.screenWidth/2)-50, 350, 100, 50)

        mx, my = pygame.mouse.get_pos()

        if startButton.collidepoint((mx, my)): #If the mouse is in contact with the button
            pygame.draw.rect(main.screen, main.yellowDark, startButton) #Change the colour of the button
            if click == True:
                import trackMenu
                trackMenu.runTrackMenu() #Go to the track menu
        else:
            pygame.draw.rect(main.screen, main.yellow, startButton)

        main.drawText("Start", main.font, main.black, main.screen, (main.screenWidth/2)-25, 365)

        pygame.display.update()
        main.clock.tick(60)

runMainMenu()
