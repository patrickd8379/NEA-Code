#Format: track = [[sectionNumber, colourOnTerrainImage, terrain, inTrackLimits],...]
#trackSectors = [sectionNumber, sectionNumber, sectionNumber]

#TERRAIN
track = [1, "Track"]
grass = [0.5, "Grass"]
gravel = [0.3, "Gravel"]
wall = [0, "Wall"]

#TRACKS
track1 = [[1, (0,0,0), wall, False], [2, (239, 228, 176), gravel, False], [3, (34, 177, 76), grass, False], [4, (237, 28, 36), track, True], [5, (255, 242, 0), track, True], [6, (127, 127, 127), track, True]]
track1Sectors = [4, 5, 6]
track2 = [[1,(0,0,0), wall, False], [2, (239, 228, 176), gravel, False], [3, (34, 177, 76), grass, False],  [4, (237, 28, 36), track, True], [5, (255, 242, 0), track, True], [6, (255, 255, 255), track, True]]
track2Sectors = [4, 5, 6]
track3 = [[1, (0,0,0), wall, False], [2, (239, 228, 176), gravel, False], [3, (34, 177, 76), grass, False], [4, (112, 146, 190), track, False],[5, (237, 28, 36), track, True], [6, (255, 242, 0), track, True], [7, (255, 255, 255), track, True]]
track3Sectors = [5, 6, 7]
