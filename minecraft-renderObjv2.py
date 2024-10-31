#www.stuffaboutcode.com
#Raspberry Pi, Minecraft - Create 3D Model from Obj file
# Version 2 - draws complete faces rather than wireframes and uses materials

#import the minecraft.py module from the minecraft directory
# import minecraft.minecraft as minecraft
# #import minecraft block module
# import minecraft.block as block
#import time, so delays can be used
import time
#import datetime, to get the time!
import datetime

import sys

from mcje.minecraft import Minecraft
import param_MCJE as param
from param_MCJE import PLAYER_ORIGIN as po

from mcje.vec3 import Vec3

# class to create 3d filled polygons
class MinecraftDrawing:
    def __init__(self, mc):
        self.mc = mc

    # draw point
    def drawPoint3d(self, x, y, z, blockType, blockData=None):
        # self.mc.setBlock(x,y,z,blockType,blockData)
        self.mc.setBlock(x,y,z,blockType)
        # time.sleep(0.001)
        # print("x = " + str(x) + ", y = " + str(y) + ", z = " + str(z))

    # draws a face, when passed a collection of vertices which make up a polyhedron
    def drawFace(self, vertices, blockType, blockData=None):

        # get the edges of the face
        edgesVertices = []
        # persist first vertex
        firstVertex = vertices[0]
        # loop through vertices and get edges
        vertexCount = 0
        for vertex in vertices:
            vertexCount+=1
            if vertexCount > 1:
                # got 2 vertices, get the points for the edge
                edgesVertices = edgesVertices + self.getLine(lastVertex.x, lastVertex.y, lastVertex.z, vertex.x, vertex.y, vertex.z)
                #print "x = " + str(lastVertex.x) + ", y = " + str(lastVertex.y) + ", z = " + str(lastVertex.z) + " x2 = " + str(vertex.x) + ", y2 = " + str(vertex.y) + ", z2 = " + str(vertex.z)
            # persist the last vertex found
            lastVertex = vertex
        # get edge between the last and first vertices
        edgesVertices = edgesVertices + self.getLine(lastVertex.x, lastVertex.y, lastVertex.z, firstVertex.x, firstVertex.y, firstVertex.z)

        # sort edges vertices
        def keyX( point ): return point.x
        def keyY( point ): return point.y
        def keyZ( point ): return point.z
        edgesVertices.sort( key=keyZ )
        edgesVertices.sort( key=keyY )
        edgesVertices.sort( key=keyX )

        # not very performant but wont have gaps between in complex models
        for vertex in edgesVertices:
            vertexCount+=1
            # got 2 vertices, draw lines between them
            if (vertexCount > 1):
                self.drawLine(lastVertex.x, lastVertex.y, lastVertex.z, vertex.x, vertex.y, vertex.z, blockType, blockData)
                #print "x = " + str(lastVertex.x) + ", y = " + str(lastVertex.y) + ", z = " + str(lastVertex.z) + " x2 = " + str(vertex.x) + ", y2 = " + str(vertex.y) + ", z2 = " + str(vertex.z)
            # persist the last vertex found
            lastVertex = vertex

    # draw's all the points in a collection of vertices with a block
    def drawVertices(self, vertices, blockType, blockData=None):
        for vertex in vertices:
            self.drawPoint3d(vertex.x, vertex.y, vertex.z, blockType, blockData)

    # draw line
    def drawLine(self, x1, y1, z1, x2, y2, z2, blockType, blockData):
        self.drawVertices(self.getLine(x1, y1, z1, x2, y2, z2), blockType, blockData)

    # returns points on a line
    def getLine(self, x1, y1, z1, x2, y2, z2):

        # return maximum of 2 values
        def MAX(a,b):
            if a > b: return a
            else: return b

        # return step
        def ZSGN(a):
            if a < 0: return -1
            elif a > 0: return 1
            elif a == 0: return 0

        # list for vertices
        vertices = []

        # if the 2 points are the same, return single vertice
        if (x1 == x2 and y1 == y2 and z1 == z2):
            vertices.append(Vec3(x1, y1, z1))

        # else get all points in edge
        else:

            dx = x2 - x1
            dy = y2 - y1
            dz = z2 - z1

            ax = abs(dx) << 1
            ay = abs(dy) << 1
            az = abs(dz) << 1

            sx = ZSGN(dx)
            sy = ZSGN(dy)
            sz = ZSGN(dz)

            x = x1
            y = y1
            z = z1

            # x dominant
            if (ax >= MAX(ay, az)):
                yd = ay - (ax >> 1)
                zd = az - (ax >> 1)
                loop = True
                while(loop):
                    vertices.append(Vec3(x, y, z))
                    if (x == x2):
                        loop = False
                    if (yd >= 0):
                        y += sy
                        yd -= ax
                    if (zd >= 0):
                        z += sz
                        zd -= ax
                    x += sx
                    yd += ay
                    zd += az
            # y dominant
            elif (ay >= MAX(ax, az)):
                xd = ax - (ay >> 1)
                zd = az - (ay >> 1)
                loop = True
                while(loop):
                    vertices.append(Vec3(x, y, z))
                    if (y == y2):
                        loop=False
                    if (xd >= 0):
                        x += sx
                        xd -= ay
                    if (zd >= 0):
                        z += sz
                        zd -= ay
                    y += sy
                    xd += ax
                    zd += az
            # z dominant
            elif(az >= MAX(ax, ay)):
                xd = ax - (az >> 1)
                yd = ay - (az >> 1)
                loop = True
                while(loop):
                    vertices.append(Vec3(x, y, z))
                    if (z == z2):
                        loop=False
                    if (xd >= 0):
                        x += sx
                        xd -= az
                    if (yd >= 0):
                        y += sy
                        yd -= az
                    z += sz
                    xd += ax
                    yd += ay

        return vertices

def load_obj(filename, defaultBlock, materials) :
    V = [] #vertex
    T = [] #texcoords
    N = [] #normals
    F = [] #face indexies
    MF = [] #materials to faces

    currentMaterial = defaultBlock

    fh = open(filename)
    for line in fh :
        if line[0] == '#' : continue
        line = line.strip().split(' ')
        if line[0] == 'v' : #vertex
            V.append(line[1:])
        elif line[0] == 'vt' : #tex-coord
            T.append(line[1:])
        elif line[0] == 'vn' : #normal vector
            N.append(line[1:])
        elif line[0] == 'f' : #face
            face = line[1:]
            for i in range(0, len(face)) :
                face[i] = face[i].split('/')
                # OBJ indexies are 1 based not 0 based hence the -1
                # convert indexies to integer
                for j in range(0, len(face[i])) :
                    if face[i][j] != "":
                        face[i][j] = int(face[i][j]) - 1
            #append the material currently in use to the face
            F.append(face)
            MF.append(currentMaterial)

        elif line[0] == 'usemtl': # material

            usemtl = line[1]
            if (usemtl in materials.keys()):
                currentMaterial = materials[usemtl]
            else:
                currentMaterial = defaultBlock
                print("Warning: Couldn't find '" + str(usemtl) + "' in materials using default")

    return V, T, N, F, MF

# strips the x,y,z co-ords from a vertex line, scales appropriately, rounds and converts to int
def getVertexXYZ(vertexLine, scale, startCoord, swapYZ):
    # convert, round and scale
    if len(vertexLine) == 3:
        i = 0
    else:
        i = 1
    x = int((float(vertexLine[i]) * scale) + 0.5)
    y = int((float(vertexLine[i + 1]) * scale) + 0.5)
    z = int((float(vertexLine[i + 2]) * scale) + 0.5)
    # add startCoord to x,y,z
    x = x + startCoord.x
    y = y + startCoord.y
    z = z + startCoord.z
    # swap y and z coord if needed
    if swapYZ == True:
        swap = y
        y = z
        z = swap
    return x, y, z

# main program
if __name__ == "__main__":

    print(datetime.datetime.now())

    #Connect to minecraft by creating the minecraft object
    # - minecraft needs to be running and in a game
    # mc = minecraft.Minecraft.create()

    # Connect to minecraft and open a session as player with origin location
    mc = Minecraft.create(address=param.ADRS_MCR, port=param.PORT_MCR)
    result = mc.setPlayer(param.PLAYER_NAME, po.x, po.y, po.z)
    if ("Error" in result):
        sys.exit(result)
    else:
        print(result)


    #Create minecraft drawing class
    mcDrawing = MinecraftDrawing(mc)

    #Load objfile and set constants

    # COORDSSCALE = factor to scale the co-ords by
    # STARTCOORD = where to start the model, the relative position 0
    # CLEARAREA1/2 = 2 points the program should clear an area in between to put the model in
    # SWAPYZ = True to sway the Y and Z dimension
    # MATERIALS = a dictionary object which maps materials in the obj file to blocks in minecraft
    # DEFAULTBLOCK = the default type of block to build the model in, used if a material cant be found

    # Shuttle
    # COORDSSCALE = 10
    # STARTCOORD = Vec3(0, 0, param.Y_SEA + 90)
    # CLEARAREA1 = Vec3(-70, -20, param.Y_SEA + 90)
    # CLEARAREA2 = Vec3(70,   20, param.Y_SEA + 120)
    # DEFAULTBLOCK = [param.SEA_LANTERN_BLOCK,0]
    # MATERIALS = {"glass": [param.GLASS, None],
    #             "bone": [param.WHITE_WOOL, 0],
    #             "fldkdkgrey": [param.GRAY_WOOL, 7],
    #             "redbrick": [param.RED_WOOL, 14],
    #             "black": [param.BLACK_WOOL, 15],
    #             "brass": [param.ORANGE_WOOL, 1],
    #             "dkdkgrey": [param.GRAY_WOOL, 7]}
    # SWAPYZ = True
    # vertices,textures,normals,faces,materials = load_obj("shuttle.obj", DEFAULTBLOCK, MATERIALS)

    # Shyscraper
    # COORDSSCALE = 1.4
    # STARTCOORD = Vec3(0,10 + param.Y_SEA,15)
    # CLEARAREA1 = Vec3(-30, -3 + param.Y_SEA, -15)
    # CLEARAREA2 = Vec3(30, 65 + param.Y_SEA, 35)
    # DEFAULTBLOCK = [param.IRON_BLOCK, None]
    # # MATERIALS = {}
    # MATERIALS = {"glass": [param.GLASS, None],
    #             "bone": [param.WHITE_WOOL, 0],
    #             "bluteal": [param.GREEN_WOOL, 7],
    #             "blutan": [param.GRAY_WOOL, 7],
    #             "tan": [param.YELLOW_WOOL, 14],
    #             "black": [param.BLACK_WOOL, 15],
    #             "brass": [param.GOLD_BLOCK, 1],
    #             "ltbrown": [param.ORANGE_WOOL, 1],
    #             "brown": [param.BROWN_WOOL, 7]}
    # SWAPYZ = False
    # vertices,textures,normals,faces,materials = load_obj("skyscraper.obj", DEFAULTBLOCK, MATERIALS)

    # Head
    # COORDSSCALE = 4
    # STARTCOORD = Vec3(0,-431 + param.Y_SEA - 100, 0)
    # CLEARAREA1 = Vec3(-20, -500 + param.Y_SEA, -20)
    # CLEARAREA2 = Vec3(20, -531 + param.Y_SEA, 20)

    # COORDSSCALE = 5
    # STARTCOORD = Vec3(0,-690 + param.Y_SEA, 0)
    # CLEARAREA1 = Vec3(-30, -690 + param.Y_SEA, -30)
    # CLEARAREA2 = Vec3(30, -600 + param.Y_SEA, 30)

    # DEFAULTBLOCK = [param.WHITE_WOOL, None]
    # # MATERIALS = {"initialShadingGroup": [param.SEA_LANTERN_BLOCK, 0]}
    # MATERIALS = {"initialShadingGroup": [param.GLOWSTONE, 0]}
    # SWAPYZ = False
    # vertices,textures,normals,faces,materials = load_obj("head.obj", DEFAULTBLOCK, MATERIALS)

    # Cessna
    # COORDSSCALE = 2
    # STARTCOORD = Vec3(-75, 25 + param.Y_SEA + 50, -60)
    # CLEARAREA1 = Vec3(-30, 15 + param.Y_SEA + 50, -30)
    # CLEARAREA2 = Vec3(-100, 65 + param.Y_SEA + 50, -90)
    # DEFAULTBLOCK = [param.SEA_LANTERN_BLOCK, None]
    # # MATERIALS = {}
    # MATERIALS = {"Default_Material": [param.WHITE_WOOL, 0],
    #             "red": [param.RED_WOOL, 0],
    #             "black": [param.BLACK_WOOL, 0],
    #             "yellow": [param.YELLOW_WOOL, 0],
    #             "white": [param.WHITE_WOOL, 0],
    #             "dkgrey": [param.GRAY_WOOL, 8],
    #             "glass": [param.GLASS, 5]}
    # SWAPYZ = False
    # vertices,textures,normals,faces,materials = load_obj("cessna.obj", DEFAULTBLOCK, MATERIALS)

    # New York
    # COORDSSCALE = 0.1
    # STARTCOORD = Vec3(-185, 0 + param.Y_SEA, 140)
    # CLEARAREA1 = Vec3(-130, 0 + param.Y_SEA, -130)
    # CLEARAREA2 = Vec3(130, 0 + param.Y_SEA, 130)
    # DEFAULTBLOCK = [param.IRON_BLOCK, None]
    # MATERIALS = {"Default_Material": [param.WHITE_WOOL, 0],
    #             "Color_A01": [param.RED_WOOL, 0],
    #             "0131_Silver": [param.IRON_BLOCK, None],
    #             "0075_ForestGreen": [param.GREEN_WOOL, 0],
    #             "0137_Black": [param.BLACK_WOOL, 0],
    #             "Black": [param.BLACK_WOOL, 0],
    #             "Medium_Brown": [param.BROWN_WOOL, 0],
    #             "0056_Yellow": [param.YELLOW_WOOL, 0],
    #             "0020_Red": [param.RED_WOOL, 0],
    #             "0102_RoyalBlue": [param.BLUE_WOOL, 0],
    #             "Color_E01": [param.YELLOW_WOOL, 0],
    #             "Color_E02": [param.YELLOW_WOOL, 4],
    #             "Color_B01": [param.ORANGE_WOOL, 1],
    #             "Charcoal": [param.GRAY_WOOL, 7],
    #             "Material2": [param.WHITE_WOOL, 0],
    #             "Beige2": ["sandstone", None],
    #             "DarkGoldenrod": [param.GOLD_BLOCK, None],
    #             "Beige1": ["sandstone", None],
    #             "jean_blue": [param.LIGHT_BLUE_WOOL, 3],
    #             "Gold1": [param.GOLD_BLOCK, None],
    #             "WhiteSmoke": [param.LIGHT_GRAY_WOOL, 8],
    #             "0118_Thistle": [param.PINK_WOOL, 6],
    #             "Color_D23": [param.GRAY_WOOL, 7],
    #             "Color_B23": [param.BROWN_WOOL, 12],
    #             "Color_009": [param.BLACK_WOOL, 15],
    #             "Color_D01": [param.ORANGE_WOOL, 1],
    #             "Color_A06": [param.RED_WOOL, 14],
    #             "Color_D03": [param.YELLOW_WOOL, 4],
    #             "0063_GreenYellow": [param.LIME_WOOL, 5]}
    # SWAPYZ = False
    # vertices,textures,normals,faces,materials = load_obj("NY_LIL.obj", DEFAULTBLOCK, MATERIALS)

    # Nottingham Forest City Ground
    # COORDSSCALE = 2
    # STARTCOORD = Vec3(0, -1 + param.Y_SEA + 1, 0)
    # CLEARAREA1 = Vec3(-50, -1 + param.Y_SEA + 1, -50)
    # CLEARAREA2 = Vec3(50, 20 + param.Y_SEA + 1, 50)
    # DEFAULTBLOCK = ['dirt',None]
    # # MATERIALS = {"Default_Material": [param.SEA_LANTERN_BLOCK, 0]}
    # MATERIALS = {"Default_Material": [param.BLACK_WOOL,None],
    #             "Black": [param.BLACK_WOOL,15],
    #             "Asphalt_Old": [param.GRAY_WOOL,7],
    #             "GhostWhite": [param.WHITE_WOOL,0],
    #             "Brick_Flemish_Bond": ['bricks',None],
    #             "Concrete_Brushed": [param.STONE,None],
    #             "Metal_Brushed": [param.IRON_BLOCK,None],
    #             "Roofing_Metal_Standing_Seam_Blue": [param.LIGHT_GRAY_WOOL,8],
    #             "White": [param.WHITE_WOOL,0],
    #             "Metal_Brushed1": [param.IRON_BLOCK,None],
    #             "Rouge3141": [param.LIGHT_GRAY_WOOL,14],
    #             "roof": [param.LIGHT_GRAY_WOOL,8],
    #             "Metal_Aluminum_Anodized": [param.IRON_BLOCK,None],
    #             "Translucent_Glass_Safety": [param.GLASS, None],
    #             "Translucent_Glass_Safety1": [param.GLASS, None],
    #             "Safety_Glass2": [param.GLASS, None],
    #             "Red": [param.RED_WOOL,14],
    #             "goal_net1": [param.WHITE_WOOL,0],
    #             "Black": [param.BLACK_WOOL,15]}
    # SWAPYZ = False
    # vertices,textures,normals,faces, materials = load_obj("City_Ground-Notts.obj", DEFAULTBLOCK, MATERIALS)

    # Raspbery Pi
    # COORDSSCALE = 2000
    # STARTCOORD = Vec3(0, param.Y_SEA + 0, 0)
    # CLEARAREA1 = Vec3(-50, param.Y_SEA + 0, -150)
    # CLEARAREA2 = Vec3(220, param.Y_SEA + 40, 50)
    # DEFAULTBLOCK = [param.GRASS_BLOCK,None]
    # MATERIALS = {"Default_Material": [param.WHITE_WOOL, 0],
    #              "Material1": [param.LIME_WOOL, 0],
    #              "Goldenrod": [param.YELLOW_WOOL, 0],
    #              "0136_Charcoal": [param.GRAY_WOOL, 0],
    #              "Gray61": [param.GRAY_WOOL, 0],
    #              "Charcoal": [param.GRAY_WOOL, 0],
    #              "Color_002": [param.LIGHT_GRAY_WOOL, 0],
    #              "Color_008": [param.YELLOW_WOOL, 0],
    #              "Plastic_Green": [param.LIME_WOOL, 0],
    #              "MB_Pastic_White": [param.WHITE_WOOL, 0],
    #              "IO_Shiny": [param.IRON_BLOCK, 0],
    #              "Material4": [param.GRASS_BLOCK, 0],
    #              "Gainsboro3": [param.LIME_WOOL, 0],
    #              "CorrogateShiny1": [param.IRON_BLOCK, 0],
    #              "Gold": [param.GOLD_BLOCK, 0],
    #              "0129_WhiteSmoke": [param.WHITE_WOOL, 0],
    #              "Color_005": [param.WHITE_WOOL, 0],
    #              "USB_IO": [param.BLUE_WOOL, 0],
    #              "_Metal": [param.IRON_BLOCK, 0],
    #              "0132_LightGray": [param.LIGHT_GRAY_WOOL, 0]}
    # SWAPYZ = False
    # vertices,textures,normals,faces, materials = load_obj("RaspberryPi.obj", DEFAULTBLOCK, MATERIALS)


    # Football
    # COORDSSCALE = 1.5
    # STARTCOORD = Vec3(0, 25 + param.Y_SEA, 0)
    # CLEARAREA1 = Vec3(-30, 25 + param.Y_SEA, -30)
    # CLEARAREA2 = Vec3(30, 65 + param.Y_SEA, 30)
    # DEFAULTBLOCK = [param.SEA_LANTERN_BLOCK, None]
    # # MATERIALS = {}
    # # MATERIALS = {"Default_Material": [param.WHITE_WOOL, 0],
    # #             "01___Default": [param.BLACK_WOOL, 0],
    # #             "02___Default": [param.WHITE_WOOL, 0],
    # #             "glass": [param.GLASS, 5]}
    # MATERIALS = {"Default_Material": [param.WHITE_WOOL, 0],
    #             "01___Default": [param.GOLD_BLOCK, 0],
    #             "02___Default": [param.SEA_LANTERN_BLOCK, 0],
    #             "glass": [param.GLASS, 5]}
    # SWAPYZ = False
    # vertices,textures,normals,faces,materials = load_obj("Football.obj", DEFAULTBLOCK, MATERIALS)

    # traffic_cone
    COORDSSCALE = 30
    STARTCOORD = Vec3(0, 1 + param.Y_SEA, 0)
    CLEARAREA1 = Vec3(-60, 1 + param.Y_SEA, -60)
    CLEARAREA2 = Vec3(60, 100 + param.Y_SEA, 60)
    DEFAULTBLOCK = [param.SEA_LANTERN_BLOCK, None]
    MATERIALS = {"Default_Material": [param.WHITE_WOOL, 0],
                "orange": [param.ORANGE_WOOL, 0],
                "white": [param.WHITE_WOOL, 5]}
    SWAPYZ = False
    vertices,textures,normals,faces,materials = load_obj("traffic_cone.obj", DEFAULTBLOCK, MATERIALS)



    print("obj file loaded")

    #Post a message to the minecraft chat window
    mc.postToChat("Hi, Minecraft 3d model maker, www.stuffaboutcode.com")

    # clear a suitably large area
    mc.setBlocks(CLEARAREA1.x, CLEARAREA1.y, CLEARAREA1.z, CLEARAREA2.x, CLEARAREA2.y, CLEARAREA2.z, param.AIR)
    time.sleep(10)

    faceCount = 0
    # loop through faces
    for face in faces:
        faceVertices = []

        # loop through vertex's in face and call drawFace function
        for vertex in face:
            #strip co-ords from vertex line
            vertexX, vertexY, vertexZ = getVertexXYZ(vertices[vertex[0]], COORDSSCALE, STARTCOORD, SWAPYZ)

            faceVertices.append(Vec3(vertexX,vertexY,vertexZ))

        # draw the face
        mcDrawing.drawFace(faceVertices, materials[faceCount][0], materials[faceCount][1])
        faceCount = faceCount + 1

    mc.postToChat("Model complete, www.stuffaboutcode.com")

    print(datetime.datetime.now())
