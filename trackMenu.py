import pygame, sys, math, os, tracks
from main import *

currentSetup = DEFAULTSETUP

track1Button = pygame.Rect(25, 100, 185, 219)
track1Preview = pygame.image.load(os.path.join('images', 'track1preview.png')).convert_alpha()

track2Button = pygame.Rect(283, 100, 185, 219)
track2Preview = pygame.image.load(os.path.join('images', 'track2preview.png')).convert_alpha()

track3Button = pygame.Rect(540, 100, 185, 219)
track3Preview = pygame.image.load(os.path.join('images', 'track3preview.png')).convert_alpha()

screen.fill(blue)
drawText("Track Menu", font, black, screen, 20, 20)

inTrackMenu = True

while inTrackMenu:
    click = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                mainMenu()
                inTrackMenu = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                click = True
    mx, my = pygame.mouse.get_pos()
    if track1Button.collidepoint((mx, my)):
        pygame.draw.rect(screen, yellowDark, track1Button)
        screen.blit(track1Preview, (30,105))
        if click == True: #Track 1 is selected and loaded
            trackName = "track1"
            trackLeaderboard = "track1leaderboard.txt"
            trackImage = pygame.image.load(os.path.join('images', 'track1.png')).convert_alpha()
            trackImage = pygame.transform.scale(trackImage, (3656, 2704))
            trackTerrain = pygame.image.load(os.path.join('images', 'track1terrain.png')).convert_alpha()
            trackTerrain = pygame.transform.scale(trackTerrain, (3656, 2704))
            track = Track(trackName, trackLeaderboard, trackImage, trackTerrain, 1000, 1000, tracks.track1, tracks.track1Sectors)
            exec(open(SETUPMENU).read()) #Go to the setup menu with the track that has been opened
            inTrackMenu = False
    else:
        pygame.draw.rect(screen, yellow, track1Button)
        screen.blit(track1Preview, (30,105))
    if track2Button.collidepoint((mx, my)):
        pygame.draw.rect(screen, yellowDark, track2Button)
        screen.blit(track2Preview, (288,105))
        if click == True: #Track 2 is selected and loaded
            trackName = "track2"
            trackLeaderboard = "track2leaderboard.txt"
            trackImage = pygame.image.load(os.path.join('images', 'track2.png')).convert_alpha()
            trackImage = pygame.transform.scale(trackImage, (4570, 3380))
            trackTerrain = pygame.image.load(os.path.join('images', 'track2terrain.png')).convert_alpha()
            trackTerrain = pygame.transform.scale(trackTerrain, (4570, 3380))
            track = Track(trackName, trackLeaderboard, trackImage, trackTerrain, 1000, 200, tracks.track2, tracks.track2Sectors)
            exec(open(SETUPMENU).read())
            inTrackMenu = False
    else:
        pygame.draw.rect(screen, yellow, track2Button)
        screen.blit(track2Preview, (288,105))
    if track3Button.collidepoint((mx, my)):
        pygame.draw.rect(screen, yellowDark, track3Button)
        screen.blit(track3Preview, (545,105))
        if click == True: #Track 3 is selected and loaded
            trackName = "track3"
            trackLeaderboard = "track3leaderboard.txt"
            trackImage = pygame.image.load(os.path.join('images', 'track3.png')).convert_alpha()
            trackImage = pygame.transform.scale(trackImage, (3656, 2704))
            trackTerrain = pygame.image.load(os.path.join('images', 'track3terrain.png')).convert_alpha()
            trackTerrain = pygame.transform.scale(trackTerrain, (3656, 2704))
            track = Track(trackName, trackLeaderboard, trackImage, trackTerrain, 600, 170, tracks.track3, tracks.track3Sectors)
            exec(open(SETUPMENU).read())
            inTrackMenu = False
    else:
        pygame.draw.rect(screen, yellow, track3Button)
        screen.blit(track3Preview, (545,105))

    pygame.display.update()
    clock.tick(60)
