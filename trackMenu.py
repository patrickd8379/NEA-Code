import pygame, sys, math, os, main, tracks, main, mainMenu, setupMenu

class Track(): #Properties of the track
    def __init__(self, trackName, trackLeaderboard, trackImage, trackTerrain, x, y, trackSections, trackSectors):
        self.name = trackName
        self.leaderboard = trackLeaderboard
        self.image = trackImage
        self.terrain = trackTerrain
        self.spawnPoint = (x, y)
        self.sections = trackSections
        self.sectors = trackSectors

    def getTrackLeaderboard():
        return self.trackLeaderboard

def runTrackMenu():

    track1Button = pygame.Rect(25, 100, 185, 219)
    track1Preview = pygame.image.load(os.path.join('images', 'track1preview.png')).convert_alpha()

    track2Button = pygame.Rect(283, 100, 185, 219)
    track2Preview = pygame.image.load(os.path.join('images', 'track2preview.png')).convert_alpha()

    track3Button = pygame.Rect(540, 100, 185, 219)
    track3Preview = pygame.image.load(os.path.join('images', 'track3preview.png')).convert_alpha()

    main.screen.fill(main.blue)
    main.drawText("Track Menu", main.font, main.black, main.screen, 20, 20)

    inTrackMenu = True

    currentSetup = main.DEFAULTSETUP

    track = None

    while inTrackMenu:
        click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    mainMenu.runMainMenu()
                    inTrackMenu = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
        mx, my = pygame.mouse.get_pos()
        if track1Button.collidepoint((mx, my)):
            pygame.draw.rect(main.screen, main.yellowDark, track1Button)
            main.screen.blit(track1Preview, (30,105))
            if click == True: #Track 1 is selected and loaded
                trackName = "track1"
                trackLeaderboard = "track1leaderboard.txt"
                trackImage = pygame.image.load(os.path.join('images', 'track1.png')).convert_alpha()
                trackImage = pygame.transform.scale(trackImage, (3656, 2704))
                trackTerrain = pygame.image.load(os.path.join('images', 'track1terrain.png')).convert_alpha()
                trackTerrain = pygame.transform.scale(trackTerrain, (3656, 2704))
                track = Track(trackName, trackLeaderboard, trackImage, trackTerrain, 1000, 1000, tracks.track1, tracks.track1Sectors)
                inTrackMenu = False
                setupMenu.runSetupMenu(track, currentSetup) #Go to the setup menu with the track that has been opened
        else:
            pygame.draw.rect(main.screen, main.yellow, track1Button)
            main.screen.blit(track1Preview, (30,105))
        if track2Button.collidepoint((mx, my)):
            pygame.draw.rect(main.screen, main.yellowDark, track2Button)
            main.screen.blit(track2Preview, (288,105))
            if click == True: #Track 2 is selected and loaded
                trackName = "track2"
                trackLeaderboard = "track2leaderboard.txt"
                trackImage = pygame.image.load(os.path.join('images', 'track2.png')).convert_alpha()
                trackImage = pygame.transform.scale(trackImage, (3656, 2704))
                trackTerrain = pygame.image.load(os.path.join('images', 'track2terrain.png')).convert_alpha()
                trackTerrain = pygame.transform.scale(trackTerrain, (3656, 2704))
                track = Track(trackName, trackLeaderboard, trackImage, trackTerrain, 1000, 160, tracks.track2, tracks.track2Sectors)
                inTrackMenu = False
                setupMenu.runSetupMenu(track, currentSetup)
        else:
            pygame.draw.rect(main.screen, main.yellow, track2Button)
            main.screen.blit(track2Preview, (288,105))
        if track3Button.collidepoint((mx, my)):
            pygame.draw.rect(main.screen, main.yellowDark, track3Button)
            main.screen.blit(track3Preview, (545,105))
            if click == True: #Track 3 is selected and loaded
                trackName = "track3"
                trackLeaderboard = "track3leaderboard.txt"
                trackImage = pygame.image.load(os.path.join('images', 'track3.png')).convert_alpha()
                trackImage = pygame.transform.scale(trackImage, (3656, 2704))
                trackTerrain = pygame.image.load(os.path.join('images', 'track3terrain.png')).convert_alpha()
                trackTerrain = pygame.transform.scale(trackTerrain, (3656, 2704))
                track = Track(trackName, trackLeaderboard, trackImage, trackTerrain, 200, 170, tracks.track3, tracks.track3Sectors)
                inTrackMenu = False
                setupMenu.runSetupMenu(track, currentSetup)
        else:
            pygame.draw.rect(main.screen, main.yellow, track3Button)
            main.screen.blit(track3Preview, (545,105))

        pygame.display.update()
        main.clock.tick(60)
