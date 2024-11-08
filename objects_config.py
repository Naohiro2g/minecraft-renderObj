from mcje.vec3 import Vec3
import param_MCJE as param

OBJECTS_CONFIG = {
    "cessna": {
        "COORDSSCALE": 2,
        "STARTCOORD": Vec3(-75, 25 + param.Y_SEA + 50, -60),
        "CLEARAREA1": Vec3(-30, 15 + param.Y_SEA + 50, -30),
        "CLEARAREA2": Vec3(-100, 65 + param.Y_SEA + 50, -90),
        "DEFAULTBLOCK": [param.SEA_LANTERN_BLOCK, None],
        "MATERIALS": {
            "Default_Material": [param.WHITE_WOOL, 0],
            "red": [param.RED_WOOL, 0],
            "black": [param.BLACK_WOOL, 0],
            "yellow": [param.YELLOW_WOOL, 0],
            "white": [param.WHITE_WOOL, 0],
            "dkgrey": [param.GRAY_WOOL, 8],
            "glass": [param.GLASS, 5]
        },
        "SWAPYZ": False,
        "OBJ_FILE": "cessna.obj"
    },
    "City_ground-Notts": {
        "COORDSSCALE": 2,
        "STARTCOORD": Vec3(0, -1 + param.Y_SEA + 1, 0),
        "CLEARAREA1": Vec3(-50, -1 + param.Y_SEA + 1, -50),
        "CLEARAREA2": Vec3(50, 20 + param.Y_SEA + 1, 50),
        "DEFAULTBLOCK": ['dirt', None],
        "MATERIALS": {
            "Default_Material": [param.BLACK_WOOL, None],
            "Asphalt_Old": [param.GRAY_WOOL, 7],
            "GhostWhite": [param.WHITE_WOOL, 0],
            "Brick_Flemish_Bond": ['bricks', None],
            "Concrete_Brushed": [param.STONE, None],
            "Metal_Brushed": [param.IRON_BLOCK, None],
            "Roofing_Metal_Standing_Seam_Blue": [param.LIGHT_GRAY_WOOL, 8],
            "White": [param.WHITE_WOOL, 0],
            "Metal_Brushed1": [param.IRON_BLOCK, None],
            "Rouge3141": [param.LIGHT_GRAY_WOOL, 14],
            "roof": [param.LIGHT_GRAY_WOOL, 8],
            "Metal_Aluminum_Anodized": [param.IRON_BLOCK, None],
            "Translucent_Glass_Safety": [param.GLASS, None],
            "Translucent_Glass_Safety1": [param.GLASS, None],
            "Safety_Glass2": [param.GLASS, None],
            "Red": [param.RED_WOOL, 14],
            "goal_net1": [param.WHITE_WOOL, 0],
            "Black": [param.BLACK_WOOL, 15]
        },
        "SWAPYZ": False,
        "OBJ_FILE": "City_Ground-Notts.obj"
    },
    "Football": {
        "COORDSSCALE": 0.5,
        "STARTCOORD": Vec3(0, 0 + param.Y_SEA, 0),
        "CLEARAREA1": Vec3(-30, -20 + param.Y_SEA, -30),
        "CLEARAREA2": Vec3(30, 20 + param.Y_SEA, 30),
        "DEFAULTBLOCK": [param.SEA_LANTERN_BLOCK, None],
        "MATERIALS": {
            "Default_Material": [param.WHITE_WOOL, 0],
            "01___Default": [param.GOLD_BLOCK, 0],
            "02___Default": [param.SEA_LANTERN_BLOCK, 0],
            "glass": [param.GLASS, 5]
        },
        "SWAPYZ": False,
        "OBJ_FILE": "Football.obj"
    },
    "head": {
        "COORDSSCALE": 5,
        "STARTCOORD": Vec3(0, -690 + param.Y_SEA, 0),
        "CLEARAREA1": Vec3(-30, -690 + param.Y_SEA, -30),
        "CLEARAREA2": Vec3(30, -600 + param.Y_SEA, 30),
        "DEFAULTBLOCK": [param.WHITE_WOOL, None],
        "MATERIALS": {
            "initialShadingGroup": [param.GLOWSTONE, 0]
        },
        "SWAPYZ": False,
        "OBJ_FILE": "head.obj"
    },
    "NY_LIL": {
        "COORDSSCALE": 0.1,
        "STARTCOORD": Vec3(-185, 0 + param.Y_SEA, 140),
        "CLEARAREA1": Vec3(-130, 0 + param.Y_SEA, -130),
        "CLEARAREA2": Vec3(130, 0 + param.Y_SEA, 130),
        "DEFAULTBLOCK": [param.IRON_BLOCK, None],
        "MATERIALS": {
            "Default_Material": [param.WHITE_WOOL, 0],
            "Color_A01": [param.RED_WOOL, 0],
            "0131_Silver": [param.IRON_BLOCK, None],
            "0075_ForestGreen": [param.GREEN_WOOL, 0],
            "0137_Black": [param.BLACK_WOOL, 0],
            "Black": [param.BLACK_WOOL, 0],
            "Medium_Brown": [param.BROWN_WOOL, 0],
            "0056_Yellow": [param.YELLOW_WOOL, 0],
            "0020_Red": [param.RED_WOOL, 0],
            "0102_RoyalBlue": [param.BLUE_WOOL, 0],
            "Color_E01": [param.YELLOW_WOOL, 0],
            "Color_E02": [param.YELLOW_WOOL, 4],
            "Color_B01": [param.ORANGE_WOOL, 1],
            "Charcoal": [param.GRAY_WOOL, 7],
            "Material2": [param.WHITE_WOOL, 0],
            "Beige2": ["sandstone", None],
            "DarkGoldenrod": [param.GOLD_BLOCK, None],
            "Beige1": ["sandstone", None],
            "jean_blue": [param.LIGHT_BLUE_WOOL, 3],
            "Gold1": [param.GOLD_BLOCK, None],
            "WhiteSmoke": [param.LIGHT_GRAY_WOOL, 8],
            "0118_Thistle": [param.PINK_WOOL, 6],
            "Color_D23": [param.GRAY_WOOL, 7],
            "Color_B23": [param.BROWN_WOOL, 12],
            "Color_009": [param.BLACK_WOOL, 15],
            "Color_D01": [param.ORANGE_WOOL, 1],
            "Color_A06": [param.RED_WOOL, 14],
            "Color_D03": [param.YELLOW_WOOL, 4],
            "0063_GreenYellow": [param.LIME_WOOL, 5]
        },
        "SWAPYZ": False,
        "OBJ_FILE": "NY_LIL.obj"
    },
    "RaspberryPi": {
        "COORDSSCALE": 2000,
        "STARTCOORD": Vec3(0, param.Y_SEA + 0, 0),
        "CLEARAREA1": Vec3(-50, param.Y_SEA + 0, -150),
        "CLEARAREA2": Vec3(220, param.Y_SEA + 40, 50),
        "DEFAULTBLOCK": [param.GRASS_BLOCK, None],
        "MATERIALS": {
            "Default_Material": [param.WHITE_WOOL, 0],
            "Material1": [param.LIME_WOOL, 0],
            "Goldenrod": [param.YELLOW_WOOL, 0],
            "0136_Charcoal": [param.GRAY_WOOL, 0],
            "Gray61": [param.GRAY_WOOL, 0],
            "Charcoal": [param.GRAY_WOOL, 0],
            "Color_002": [param.LIGHT_GRAY_WOOL, 0],
            "Color_008": [param.YELLOW_WOOL, 0],
            "Plastic_Green": [param.LIME_WOOL, 0],
            "MB_Pastic_White": [param.WHITE_WOOL, 0],
            "IO_Shiny": [param.IRON_BLOCK, 0],
            "Material4": [param.GRASS_BLOCK, 0],
            "Gainsboro3": [param.LIME_WOOL, 0],
            "CorrogateShiny1": [param.IRON_BLOCK, 0],
            "Gold": [param.GOLD_BLOCK, 0],
            "0129_WhiteSmoke": [param.WHITE_WOOL, 0],
            "Color_005": [param.WHITE_WOOL, 0],
            "USB_IO": [param.BLUE_WOOL, 0],
            "_Metal": [param.IRON_BLOCK, 0],
            "0132_LightGray": [param.LIGHT_GRAY_WOOL, 0]
        },
        "SWAPYZ": False,
        "OBJ_FILE": "RaspberryPi.obj"
    },
    "rocket": {
        "COORDSSCALE": 2,
        "STARTCOORD": Vec3(0, 63 + param.Y_SEA, 0),
        "CLEARAREA1": Vec3(-60, 63 + param.Y_SEA, -60),
        "CLEARAREA2": Vec3(60, 63 + param.Y_SEA, 60),
        "DEFAULTBLOCK": [param.SEA_LANTERN_BLOCK, None],
        "MATERIALS": {
            "Default_Material": [param.WHITE_WOOL, 0],
            "black": [param.BLACK_WOOL, 0],
            "red": [param.RED_WOOL, 0],
            "yellow": [param.YELLOW_WOOL, 0],
            "green": [param.GREEN_WOOL, 0],
            "blue": [param.BLUE_WOOL, 0],
            "brown": [param.BROWN_WOOL, 0],
            "lightgrey": [param.LIGHT_GRAY_WOOL, 0],
            "grey": [param.GRAY_WOOL, 0],
            "orange": [param.ORANGE_WOOL, 0]
        },
        "SWAPYZ": False,
        "OBJ_FILE": "rocket.obj"
    },
    "shuttle": {
        "COORDSSCALE": 10,
        "STARTCOORD": Vec3(0, 0, param.Y_SEA + 90),
        "CLEARAREA1": Vec3(-70, -20, param.Y_SEA + 90),
        "CLEARAREA2": Vec3(70, 20, param.Y_SEA + 120),
        "DEFAULTBLOCK": [param.SEA_LANTERN_BLOCK, 0],
        "MATERIALS": {
            "glass": [param.GLASS, None],
            "bone": [param.WHITE_WOOL, 0],
            "fldkdkgrey": [param.GRAY_WOOL, 7],
            "redbrick": [param.RED_WOOL, 14],
            "black": [param.BLACK_WOOL, 15],
            "brass": [param.ORANGE_WOOL, 1],
            "dkdkgrey": [param.GRAY_WOOL, 7]
        },
        "SWAPYZ": True,
        "OBJ_FILE": "shuttle.obj"
    },
    "skyscraper": {
        "COORDSSCALE": 1.4,
        "STARTCOORD": Vec3(0, 10 + param.Y_SEA, 15),
        "CLEARAREA1": Vec3(-30, -3 + param.Y_SEA, -15),
        "CLEARAREA2": Vec3(30, 65 + param.Y_SEA, 35),
        "DEFAULTBLOCK": [param.IRON_BLOCK, None],
        "MATERIALS": {
            "glass": [param.GLASS, None],
            "bone": [param.WHITE_WOOL, 0],
            "bluteal": [param.GREEN_WOOL, 7],
            "blutan": [param.GRAY_WOOL, 7],
            "tan": [param.YELLOW_WOOL, 14],
            "black": [param.BLACK_WOOL, 15],
            "brass": [param.GOLD_BLOCK, 1],
            "ltbrown": [param.ORANGE_WOOL, 1],
            "brown": [param.BROWN_WOOL, 7]
        },
        "SWAPYZ": False,
        "OBJ_FILE": "skyscraper.obj"
    },
    "traffic_cone": {
        "COORDSSCALE": 5,
        "STARTCOORD": Vec3(0, 1 + param.Y_SEA, 0),
        "CLEARAREA1": Vec3(-80, 1 + param.Y_SEA, -80),
        "CLEARAREA2": Vec3(80, 200 + param.Y_SEA, 80),
        "DEFAULTBLOCK": [param.SEA_LANTERN_BLOCK, None],
        "MATERIALS": {
            "Default_Material": [param.WHITE_WOOL, 0],
            "orange": [param.ORANGE_WOOL, 0],
            "white": [param.WHITE_WOOL, 5]
        },
        "SWAPYZ": False,
        "OBJ_FILE": "traffic_cone.obj"
    },
    "USS_Enterprise": {
        "COORDSSCALE": 20,
        "STARTCOORD": Vec3(0, 180 + param.Y_SEA, 0),
        "CLEARAREA1": Vec3(-60, 180 + param.Y_SEA, -60),
        "CLEARAREA2": Vec3(60, 180 + param.Y_SEA, 60),
        "DEFAULTBLOCK": [param.SEA_LANTERN_BLOCK, None],
        "MATERIALS": {
            "Default_Material": [param.WHITE_WOOL, 0],
            "orange": [param.ORANGE_WOOL, 0],
            "white": [param.WHITE_WOOL, 5]
        },
        "SWAPYZ": False,
        "OBJ_FILE": "USS_Enterprise_NCC-1701_7.obj"
    }
}
