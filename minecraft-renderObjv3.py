# www.stuffaboutcode.com
# Raspberry Pi, Minecraft - Create 3D Model from Obj file
# Version 2 - draws complete faces rather than wireframes and uses materials
# rewrited by naohiro2g

import datetime
import time
import sys

from mcje.minecraft import Minecraft
from mcje.vec3 import Vec3
import param_MCJE as param
from param_MCJE import PLAYER_ORIGIN as po
from objects_config import OBJECTS_CONFIG


# class to create 3d filled polygons
class MinecraftDrawing:
    def __init__(self, minecraft_connection):
        self.mc = minecraft_connection

    # draw point
    def drawPoint3d(self, x, y, z, blockType):
        self.mc.setBlock(x, y, z, blockType)
        # time.sleep(0.001)
        # print("x = " + str(x) + ", y = " + str(y) + ", z = " + str(z))

    # draws a face, when passed a collection of vertices which make up a polyhedron
    def drawFace(self, vertices, blockType):
        # get the edges of the face
        edgesVertices = []
        # persist first vertex
        firstVertex = vertices[0]
        # loop through vertices and get edges
        vertexCount = 0
        lastVertex = None
        for vertex in vertices:
            vertexCount += 1
            if vertexCount > 1:
                # got 2 vertices, get the points for the edge
                edgesVertices = edgesVertices + self.getLine(lastVertex.x, lastVertex.y, lastVertex.z,
                                                             vertex.x, vertex.y, vertex.z)
                # print("x = " + str(lastVertex.x) + ", y = " + str(lastVertex.y) + ", z = " + str(lastVertex.z)
                #              + " x2 = " + str(vertex.x) + ", y2 = " + str(vertex.y) + ", z2 = " + str(vertex.z))
            # persist the last vertex found
            lastVertex = vertex
        # get edge between the last and first vertices
        edgesVertices = edgesVertices + self.getLine(lastVertex.x, lastVertex.y, lastVertex.z,
                                                     firstVertex.x, firstVertex.y, firstVertex.z)

        # sort edges vertices
        def keyX(point):
            return point.x

        def keyY(point):
            return point.y

        def keyZ(point):
            return point.z

        edgesVertices.sort(key=keyZ)
        edgesVertices.sort(key=keyY)
        edgesVertices.sort(key=keyX)

        # not very performant but wont have gaps between in complex models
        for vertex in edgesVertices:
            vertexCount += 1
            # got 2 vertices, draw lines between them
            if (vertexCount > 1):
                self.drawLine(lastVertex.x, lastVertex.y, lastVertex.z,
                              vertex.x, vertex.y, vertex.z, blockType)
                # print("x = " + str(lastVertex.x) + ", y = " + str(lastVertex.y) + ", z = " + str(lastVertex.z)
                #       + " x2 = " + str(vertex.x) + ", y2 = " + str(vertex.y) + ", z2 = " + str(vertex.z))
            # persist the last vertex found
            lastVertex = vertex

    # draw's all the points in a collection of vertices with a block
    def drawVertices(self, vertices, blockType):
        for vertex in vertices:
            self.drawPoint3d(vertex.x, vertex.y, vertex.z, blockType)

    # draw line
    def drawLine(self, x1, y1, z1, x2, y2, z2, blockType):
        self.drawVertices(self.getLine(x1, y1, z1, x2, y2, z2), blockType)

    # returns points on a line
    def getLine(self, x1, y1, z1, x2, y2, z2):
        # return step
        def ZSGN(a):
            if a < 0:
                return -1
            elif a > 0:
                return 1
            elif a == 0:
                return 0

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
            if (ax >= max(ay, az)):
                yd = ay - (ax >> 1)
                zd = az - (ax >> 1)
                loop = True
                while (loop):
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
            elif (ay >= max(ax, az)):
                xd = ax - (ay >> 1)
                zd = az - (ay >> 1)
                loop = True
                while (loop):
                    vertices.append(Vec3(x, y, z))
                    if (y == y2):
                        loop = False
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
            elif (az >= max(ax, ay)):
                xd = ax - (az >> 1)
                yd = ay - (az >> 1)
                loop = True
                while (loop):
                    vertices.append(Vec3(x, y, z))
                    if (z == z2):
                        loop = False
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
    V = []  # vertex
    T = []  # texcoords
    N = []  # normals
    F = []  # face indexies
    MF = []  # materials to faces

    currentMaterial = defaultBlock
    filename = "objects/" + filename
    fh = open(filename, encoding='utf-8')
    for line in fh :
        if line[0] == '#':
            continue
        line = line.strip().split(' ')
        if line[0] == 'v':  # vertex
            V.append(line[1:])
        elif line[0] == 'vt':  # tex-coord
            T.append(line[1:])
        elif line[0] == 'vn':  # normal vector
            N.append(line[1:])
        elif line[0] == 'f':  # face
            face = line[1:]
            for i, f in enumerate(face):
                face[i] = f.split('/')
                # OBJ indices are 1 based not 0 based hence the -1
                # convert indices to integer
                for j, index in enumerate(face[i]):
                    if index != "":
                        face[i][j] = int(index) - 1
            # append the material currently in use to the face
            F.append(face)
            MF.append(currentMaterial)
        elif line[0] == 'usemtl':  # material
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
    if swapYZ:
        swap = y
        y = z
        z = swap
    return x, y, z


def load_object_conf(object_name, scale_ratio=1):
    obj_conf = OBJECTS_CONFIG[object_name]
    obj_conf["COORDSSCALE"] *= scale_ratio
    vertices, textures, normals, faces, materials =  \
        load_obj(obj_conf["OBJ_FILE"],
                 obj_conf["DEFAULTBLOCK"],
                 obj_conf["MATERIALS"])
    obj_conf.update({
        "vertices": vertices,
        "textures": textures,
        "normals": normals,
        "faces": faces,
        "materials": materials
    })
    return obj_conf


def render_object(mc, object_name, scale_ratio):
    mc.postToChat("Hi, Minecraft 3d model maker, www.stuffaboutcode.com")
    config = load_object_conf(object_name, scale_ratio)
    print(object_name, "loaded in scale", scale_ratio)

    # clear a suitably large area
    mc.setBlocks(config["CLEARAREA1"].x, config["CLEARAREA1"].y, config["CLEARAREA1"].z,
                 config["CLEARAREA1"].x, config["CLEARAREA1"].y, config["CLEARAREA1"].z, param.AIR)
    time.sleep(2)

    # Create minecraft drawing class
    mcDrawing = MinecraftDrawing(mc)

    # draw the object
    faceCount = 0
    # loop through faces
    for face in config["faces"]:
        faceVertices = []
        # loop through vertex's in face and call drawFace function
        for vertex in face:
            # strip co-ords from vertex line
            vertexX, vertexY, vertexZ = getVertexXYZ(
                config["vertices"][vertex[0]],
                config["COORDSSCALE"],
                config["STARTCOORD"],
                config["SWAPYZ"])
            faceVertices.append(Vec3(vertexX, vertexY, vertexZ))
        # draw the face
        mcDrawing.drawFace(
            faceVertices,
            config["materials"][faceCount][0])
        faceCount += 1
    mc.postToChat("Model complete, www.stuffaboutcode.com")


# main program
if __name__ == "__main__":
    # OBJECT_NAME = "traffic_cone"
    OBJECT_NAME = "Football"
    SCALE_RATIO = 1.0

    # Connect to minecraft and open a session as player with origin location
    mc = Minecraft.create(address=param.ADRS_MCR, port=param.PORT_MCR)
    result = mc.setPlayer(param.PLAYER_NAME, po.x, po.y, po.z)
    if "Error" in result:
        sys.exit(result)
    else:
        print(result)

    print(datetime.datetime.now())
    render_object(mc, object_name=OBJECT_NAME, scale_ratio=SCALE_RATIO)
    print(datetime.datetime.now())
