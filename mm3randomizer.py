import struct
import random

GAME_PATH = "MegaMan3.nes"

# The NES palette has 64 different colors, but many of them are repeats. This list excludes the duplicate instances of black.
VIABLE_COLORS = [0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x10, 0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17, 0x18, 0x19, 0x1A, 0x1B, 0x1C, 0x1D, 0x20, 0x21, 0x22, 0x23, 0x24, 0x25, 0x26, 0x27, 0x28, 0x29, 0x2A, 0x2B, 0x2C, 0x2D, 0x30, 0x31, 0x32, 0x33, 0x34, 0x35, 0x36, 0x37, 0x38, 0x39, 0x3A, 0x3B, 0x3C, 0x3D]

# The following lists are subsets of the total available color palette. NBW/NB/NW exclude black/white; dark and light color lists are self-explanatory, containing the darker or lighter half of available NES colors.
VIABLE_COLORS_NBW = [0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x10, 0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17, 0x18, 0x19, 0x1A, 0x1B, 0x1C, 0x21, 0x22, 0x23, 0x24, 0x25, 0x26, 0x27, 0x28, 0x29, 0x2A, 0x2B, 0x2C, 0x2D, 0x31, 0x32, 0x33, 0x34, 0x35, 0x36, 0x37, 0x38, 0x39, 0x3A, 0x3B, 0x3C, 0x3D]
DARK_COLORS = [0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17, 0x18, 0x19, 0x1A, 0x1B, 0x1C, 0x1D]
DARK_COLORS_NB = [0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17, 0x18, 0x19, 0x1A, 0x1B, 0x1C]
LIGHT_COLORS = [0x21, 0x22, 0x23, 0x24, 0x25, 0x26, 0x27, 0x28, 0x29, 0x2A, 0x2B, 0x2C, 0x30, 0x31, 0x32, 0x33, 0x34, 0x35, 0x36, 0x37, 0x38, 0x39, 0x3A, 0x3B, 0x3C, 0x3D]
LIGHT_COLORS_NW = [0x21, 0x22, 0x23, 0x24, 0x25, 0x26, 0x27, 0x28, 0x29, 0x2A, 0x2B, 0x2C, 0x31, 0x32, 0x33, 0x34, 0x35, 0x36, 0x37, 0x38, 0x39, 0x3A, 0x3B, 0x3C, 0x3D]

# Change this seed for a specific generated ROM.
#random.seed(54)


def edit_nes_byte(file_path, offset, new_value):
    with open(file_path, "rb+") as f:
        f.seek(offset)
        # Write one byte
        f.write(struct.pack('B', new_value))


def read_nes_byte(file_path, offset):
    with open(file_path, "rb+") as f:
        f.seek(offset)
        value = f.read(1)
        return value.hex()


def scramble_stage_order():
# This shuffles the first eight stages to different positions on the stage select screen. Currently disabled because this causes problems with boss selection.
    # stage_list = [0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07]
    # random.shuffle(stage_list)
    # edit_nes_byte(GAME_PATH, 0x31CF1, stage_list[0])
    # edit_nes_byte(GAME_PATH, 0x31CF2, stage_list[1])
    # edit_nes_byte(GAME_PATH, 0x31CF3, stage_list[2])
    # edit_nes_byte(GAME_PATH, 0x31CF4, stage_list[3])
    # edit_nes_byte(GAME_PATH, 0x31CF6, stage_list[4])
    # edit_nes_byte(GAME_PATH, 0x31CF7, stage_list[5])
    # edit_nes_byte(GAME_PATH, 0x31CF8, stage_list[6])
    # edit_nes_byte(GAME_PATH, 0x31CF9, stage_list[7])
    pass


def scramble_sprite_palettes():
# This scrambles the color schemes for the enemies and bosses in the game. Black and white are not replaced to maintain some level of graphical integrity. Light colors are replaced with other light colors and dark colors are replaced with other dark colors.
    for i in range(0x2040, 0x220F):
        if int(read_nes_byte(GAME_PATH, i), 16) not in [0x0F, 0x20, 0x30]:
            if(int(read_nes_byte(GAME_PATH, i), 16) in LIGHT_COLORS):
                edit_nes_byte(GAME_PATH, i, random.choice(LIGHT_COLORS_NW))
            else:
                edit_nes_byte(GAME_PATH, i, random.choice(DARK_COLORS_NB))


def scramble_stage_palettes():
# This scrambles the color schemes for the stages in the game. Black and white are not replaced to maintain some level of graphical integrity, and black and white are excluded from the possible color options to prevent extreme eyesore.
    # Needle Man
    for i in range(0xA92, 0xAA1):
        if int(read_nes_byte(GAME_PATH, i), 16) not in [0x0F, 0x20, 0x30]:
            if int(read_nes_byte(GAME_PATH, i), 16) not in [0x0F, 0x20, 0x30]:
                if(int(read_nes_byte(GAME_PATH, i), 16) in LIGHT_COLORS):
                    edit_nes_byte(GAME_PATH, i, random.choice(LIGHT_COLORS_NW))
                else:
                    edit_nes_byte(GAME_PATH, i, random.choice(DARK_COLORS))

    # Magnet Man
    for i in range(0x2A92, 0x2AB5):
        if int(read_nes_byte(GAME_PATH, i), 16) not in [0x0F, 0x20, 0x30]:
            if(int(read_nes_byte(GAME_PATH, i), 16) in LIGHT_COLORS):
                edit_nes_byte(GAME_PATH, i, random.choice(LIGHT_COLORS_NW))
            else:
                edit_nes_byte(GAME_PATH, i, random.choice(DARK_COLORS))
    # This check is made for the sky colors at the beginning so they don't look incoherent.
    edit_nes_byte(GAME_PATH, 0x2AA0, int(read_nes_byte(GAME_PATH, 0x2A9B), 16))
    edit_nes_byte(GAME_PATH, 0x2AA1, int(read_nes_byte(GAME_PATH, 0x2A9C), 16))

    # Gemini Man
    for i in range(0x4A92, 0x4ADE):
        if i not in [0x4AA2, 0x4AA3, 0x4AA4, 0x4AA5, 0x4AB6, 0x4AB7, 0x4AB8, 0x4AB9, 0x4ACA, 0x4ACB, 0x4ACC, 0x4ACD]: # Animated tile values, do not change
            if int(read_nes_byte(GAME_PATH, i), 16) not in [0x0F, 0x20, 0x30]:
                if(int(read_nes_byte(GAME_PATH, i), 16) in LIGHT_COLORS):
                    edit_nes_byte(GAME_PATH, i, random.choice(LIGHT_COLORS_NW))
                else:
                    edit_nes_byte(GAME_PATH, i, random.choice(DARK_COLORS_NB))
    # Animated tiles
    # Gemini Man's animations are more complicated than the rest of the stages and are stored in a different way as well
    # Flashing stringy things in the background of the cave segments
    gemini_string_color = random.randint(0x11, 0x1C)
    edit_nes_byte(GAME_PATH, 0x4AAF, gemini_string_color + 0x10)
    edit_nes_byte(GAME_PATH, 0x4AB0, gemini_string_color)
    edit_nes_byte(GAME_PATH, 0x4AB1, gemini_string_color)
    edit_nes_byte(GAME_PATH, 0x4AC3, gemini_string_color + 0x10)
    edit_nes_byte(GAME_PATH, 0x4AC4, gemini_string_color)
    edit_nes_byte(GAME_PATH, 0x4AC5, gemini_string_color)
    edit_nes_byte(GAME_PATH, 0x4AD7, gemini_string_color + 0x10)
    edit_nes_byte(GAME_PATH, 0x4AD8, gemini_string_color)
    edit_nes_byte(GAME_PATH, 0x4AD9, gemini_string_color)
    edit_nes_byte(GAME_PATH, 0x125D1, gemini_string_color + 0x10)
    edit_nes_byte(GAME_PATH, 0x125D2, gemini_string_color)
    edit_nes_byte(GAME_PATH, 0x125D3, gemini_string_color)
    edit_nes_byte(GAME_PATH, 0x125D4, gemini_string_color)
    edit_nes_byte(GAME_PATH, 0x125D5, gemini_string_color + 0x10)
    edit_nes_byte(GAME_PATH, 0x125D6, gemini_string_color)
    edit_nes_byte(GAME_PATH, 0x125D7, gemini_string_color)
    edit_nes_byte(GAME_PATH, 0x125D8, gemini_string_color)
    edit_nes_byte(GAME_PATH, 0x125D9, gemini_string_color + 0x10)

    # Hard Man
    for i in range(0x6A92, 0x6AA2):
        if int(read_nes_byte(GAME_PATH, i), 16) not in [0x0F, 0x20, 0x30]:
            if(int(read_nes_byte(GAME_PATH, i), 16) in LIGHT_COLORS):
                edit_nes_byte(GAME_PATH, i, random.choice(LIGHT_COLORS_NW))
            else:
                edit_nes_byte(GAME_PATH, i, random.choice(DARK_COLORS))

    # Top Man
    for i in range(0x8A92, 0x8AC6):
        if i not in [0x8AB6, 0x8AB7, 0x8AB8, 0x8AB9]: # These specific values are for tile animation and should not be messed with
            if int(read_nes_byte(GAME_PATH, i), 16) not in [0x0F, 0x20, 0x30]:
                if(int(read_nes_byte(GAME_PATH, i), 16) in LIGHT_COLORS):
                    edit_nes_byte(GAME_PATH, i, random.choice(LIGHT_COLORS_NW))
                else:
                    edit_nes_byte(GAME_PATH, i, random.choice(DARK_COLORS))
    # This ensures that the background of the panels and pipes is the same color as the stage background.
    edit_nes_byte(GAME_PATH, 0x8AB5, int(read_nes_byte(GAME_PATH, 0x8AA9), 16))
    # Animated tiles
    edit_nes_byte(GAME_PATH, 0x125F2, int(read_nes_byte(GAME_PATH, 0x8A9F), 16))
    edit_nes_byte(GAME_PATH, 0x125F3, random.choice(LIGHT_COLORS))
    edit_nes_byte(GAME_PATH, 0x125F4, int(read_nes_byte(GAME_PATH, 0x8AA9), 16))
    edit_nes_byte(GAME_PATH, 0x125F5, int(read_nes_byte(GAME_PATH, 0x8A9F), 16))
    edit_nes_byte(GAME_PATH, 0x125F6, random.choice(LIGHT_COLORS))
    edit_nes_byte(GAME_PATH, 0x125F7, int(read_nes_byte(GAME_PATH, 0x8AA9), 16))
    edit_nes_byte(GAME_PATH, 0x125F8, int(read_nes_byte(GAME_PATH, 0x8A9F), 16))
    edit_nes_byte(GAME_PATH, 0x125F9, random.choice(LIGHT_COLORS))
    edit_nes_byte(GAME_PATH, 0x125FA, int(read_nes_byte(GAME_PATH, 0x8AA9), 16))
    edit_nes_byte(GAME_PATH, 0x12601, int(read_nes_byte(GAME_PATH, 0x8A9F), 16))
    edit_nes_byte(GAME_PATH, 0x12602, random.choice(LIGHT_COLORS))
    edit_nes_byte(GAME_PATH, 0x12603, int(read_nes_byte(GAME_PATH, 0x8AA9), 16)) 

    # Snake Man
    for i in range(0xAA92, 0xAAA2):
        if int(read_nes_byte(GAME_PATH, i), 16) not in [0x0F, 0x20, 0x30]:
            if(int(read_nes_byte(GAME_PATH, i), 16) in LIGHT_COLORS):
                edit_nes_byte(GAME_PATH, i, random.choice(LIGHT_COLORS_NW))
            else:
                edit_nes_byte(GAME_PATH, i, random.choice(DARK_COLORS))
    # Animated tile values (sky and clouds)
    edit_nes_byte(GAME_PATH, 0x1259F, 0x20)
    edit_nes_byte(GAME_PATH, 0x125A0, random.choice(LIGHT_COLORS_NW))
    edit_nes_byte(GAME_PATH, 0xAAA0, int(read_nes_byte(GAME_PATH, 0x125A0), 16))
    edit_nes_byte(GAME_PATH, 0xAAA1, int(read_nes_byte(GAME_PATH, 0x125A0), 16))
    edit_nes_byte(GAME_PATH, 0x125A2, int(read_nes_byte(GAME_PATH, 0x125A0), 16))
    edit_nes_byte(GAME_PATH, 0x125A3, int(read_nes_byte(GAME_PATH, 0x125A0), 16))

    # Spark Man
    for i in range(0xCA92, 0xCAB6):
        if i not in [0xCAA2, 0xCAA3, 0xCAA4, 0xCAA5]: # These specific values are for tile animation and should not be messed with
            if int(read_nes_byte(GAME_PATH, i), 16) not in [0x0F, 0x20, 0x30]:
                if(int(read_nes_byte(GAME_PATH, i), 16) in LIGHT_COLORS):
                    edit_nes_byte(GAME_PATH, i, random.choice(LIGHT_COLORS_NW))
                else:
                    edit_nes_byte(GAME_PATH, i, random.choice(DARK_COLORS_NB))
    # The following few lines standardize the floor colors so that changing screens doesn't create weird jumbled color visuals
    edit_nes_byte(GAME_PATH, 0xCA98, int(read_nes_byte(GAME_PATH, 0xCA94), 16))
    edit_nes_byte(GAME_PATH, 0xCA99, int(read_nes_byte(GAME_PATH, 0xCA94), 16))
    edit_nes_byte(GAME_PATH, 0xCA9C, int(read_nes_byte(GAME_PATH, 0xCA94), 16))
    edit_nes_byte(GAME_PATH, 0xCA9F, int(read_nes_byte(GAME_PATH, 0xCA94), 16))
    # Animated tiles. Pull values from existing randomized stuff so your eyes don't get fried and to avoid weird color changes on transition
    edit_nes_byte(GAME_PATH, 0x125DD, int(read_nes_byte(GAME_PATH, 0xCA93), 16))
    edit_nes_byte(GAME_PATH, 0x125DE, int(read_nes_byte(GAME_PATH, 0xCA94), 16))
    edit_nes_byte(GAME_PATH, 0x125DF, random.choice(LIGHT_COLORS_NW)) # Flashing floor light color
    edit_nes_byte(GAME_PATH, 0x125E0, int(read_nes_byte(GAME_PATH, 0xCA93), 16))
    edit_nes_byte(GAME_PATH, 0x125E1, int(read_nes_byte(GAME_PATH, 0xCA94), 16)) 
    edit_nes_byte(GAME_PATH, 0x125E3, int(read_nes_byte(GAME_PATH, 0xCA9F), 16)) # Moving conveyors/gears/meters
    edit_nes_byte(GAME_PATH, 0x125E4, int(read_nes_byte(GAME_PATH, 0xCAA0), 16)) 
    edit_nes_byte(GAME_PATH, 0x125E6, int(read_nes_byte(GAME_PATH, 0xCA9F), 16)) 
    edit_nes_byte(GAME_PATH, 0x125E8, int(read_nes_byte(GAME_PATH, 0x125E4), 16))

    # Shadow Man
    for i in range(0xEA92, 0xEAA2):
        if int(read_nes_byte(GAME_PATH, i), 16) not in [0x0F, 0x20, 0x30]:
            if(int(read_nes_byte(GAME_PATH, i), 16) in LIGHT_COLORS):
                edit_nes_byte(GAME_PATH, i, random.choice(LIGHT_COLORS_NW))
            else:
                edit_nes_byte(GAME_PATH, i, random.choice(DARK_COLORS))
    # Animated tiles
    # Shadow Man's lava/sewer water works with a gradient across NES color palette rows (26, 16, 06). I think preserving this structure is best for graphical integrity.
    shadow_middle_color = random.randint(0x11, 0x1C)
    edit_nes_byte(GAME_PATH, 0x125E9, shadow_middle_color + 0x10)
    edit_nes_byte(GAME_PATH, 0x125EA, shadow_middle_color)
    edit_nes_byte(GAME_PATH, 0x125EB, shadow_middle_color - 0x10)
    edit_nes_byte(GAME_PATH, 0x125EC, shadow_middle_color)
    edit_nes_byte(GAME_PATH, 0x125ED, shadow_middle_color - 0x10)
    edit_nes_byte(GAME_PATH, 0x125EE, shadow_middle_color + 0x10)
    edit_nes_byte(GAME_PATH, 0x125EF, shadow_middle_color - 0x10)
    edit_nes_byte(GAME_PATH, 0x125F0, shadow_middle_color + 0x10)
    edit_nes_byte(GAME_PATH, 0x125F1, shadow_middle_color)
    # Put these values back into the unanimated tileset to prevent weird colors on screen transition
    edit_nes_byte(GAME_PATH, 0xEA97, int(read_nes_byte(GAME_PATH, 0x125E9), 16))
    edit_nes_byte(GAME_PATH, 0xEA98, int(read_nes_byte(GAME_PATH, 0x125EA), 16))
    edit_nes_byte(GAME_PATH, 0xEA99, int(read_nes_byte(GAME_PATH, 0x125EB), 16))

    # Break Man's fight?
    for i in range(0x31E2A, 0x31E57):
        if int(read_nes_byte(GAME_PATH, i), 16) not in [0x0F, 0x20, 0x30]:
            if(int(read_nes_byte(GAME_PATH, i), 16) in LIGHT_COLORS):
                edit_nes_byte(GAME_PATH, i, random.choice(LIGHT_COLORS_NW))
            else:
                edit_nes_byte(GAME_PATH, i, random.choice(DARK_COLORS_NB))


def scramble_title_screen_palette():
# This scrambles the palette of the title screen.
    edit_nes_byte(GAME_PATH, 0x31C15, random.choice(LIGHT_COLORS)) # Light blue letter highlights
    edit_nes_byte(GAME_PATH, 0x31C18, random.choice(LIGHT_COLORS)) # Light blue letter highlights
    edit_nes_byte(GAME_PATH, 0x31C1A, random.choice(DARK_COLORS_NB)) # Dark green letter shadows
    edit_nes_byte(GAME_PATH, 0x31C1C, random.choice(LIGHT_COLORS)) # Bright red lettering
    edit_nes_byte(GAME_PATH, 0x31C1E, random.choice(DARK_COLORS_NB)) # Dark red lettering
    edit_nes_byte(GAME_PATH, 0x31C28, random.choice(LIGHT_COLORS)) # Selection cursor


def scramble_stage_select_palettes():
# This scrambles the color schemes for the stage select and password screen. Black and white, as well as character faces, are not replaced to maintain some level of graphical integrity.
    # Stage select cursor dot palette
    #edit_nes_byte(GAME_PATH, 0x31C34, random.choice(VIABLE_COLORS))
    edit_nes_byte(GAME_PATH, 0x31C35, random.choice(LIGHT_COLORS)) # Cursor color 1
    edit_nes_byte(GAME_PATH, 0x31C36, random.choice(DARK_COLORS)) # Cursor color 2

    # Robot Master faces and eyes
    #edit_nes_byte(GAME_PATH, 0x31C38, random.choice(VIABLE_COLORS))
    #edit_nes_byte(GAME_PATH, 0x31C39, random.choice(VIABLE_COLORS))
    #edit_nes_byte(GAME_PATH, 0x31C3A, random.choice(VIABLE_COLORS))

    # Robot Master faces and eyes
    #edit_nes_byte(GAME_PATH, 0x31C3C, random.choice(VIABLE_COLORS))
    #edit_nes_byte(GAME_PATH, 0x31C3D, random.choice(VIABLE_COLORS))
    #edit_nes_byte(GAME_PATH, 0x31C3E, random.choice(VIABLE_COLORS))

    # Robot Master faces and eyes
    #edit_nes_byte(GAME_PATH, 0x31C40, random.choice(VIABLE_COLORS))
    #edit_nes_byte(GAME_PATH, 0x31C41, random.choice(VIABLE_COLORS))
    #edit_nes_byte(GAME_PATH, 0x31C42, random.choice(VIABLE_COLORS))

    # Stage select background, Mega Man, and blue Robot Masters (Needle, Shadow, Hard)
    #edit_nes_byte(GAME_PATH, 0x31C44, random.choice(VIABLE_COLORS))
    # Assign a color palette for the stage select to create consistency between selection screen and boss intro screen
    stage_select_primary = random.choice(LIGHT_COLORS)
    stage_select_secondary = random.choice(DARK_COLORS)
    edit_nes_byte(GAME_PATH, 0x31C45, stage_select_primary)
    edit_nes_byte(GAME_PATH, 0x31C46, stage_select_secondary)

    # Snake Man
    #edit_nes_byte(GAME_PATH, 0x31C48, random.choice(VIABLE_COLORS))
    #edit_nes_byte(GAME_PATH, 0x31C49, random.choice(VIABLE_COLORS)) # Snake Man's face
    edit_nes_byte(GAME_PATH, 0x31C4A, random.choice(VIABLE_COLORS_NBW)) # Snake Man

    # Red Robot Masters (Top, Spark, Magnet)
    #edit_nes_byte(GAME_PATH, 0x31C4C, random.choice(VIABLE_COLORS))
    edit_nes_byte(GAME_PATH, 0x31C4D, random.choice(LIGHT_COLORS_NW)) # Lighter color on red RMs
    edit_nes_byte(GAME_PATH, 0x31C4E, random.choice(DARK_COLORS_NB)) # Darker color on red RMs

    # Gemini Man
    #edit_nes_byte(GAME_PATH, 0x31C50, random.choice(VIABLE_COLORS))
    edit_nes_byte(GAME_PATH, 0x31C51, random.choice(VIABLE_COLORS_NBW)) # Gemini Man
    edit_nes_byte(GAME_PATH, 0x31C52, random.choice(LIGHT_COLORS_NW)) # Gemini Man's earpiece

    # Password screen
    edit_nes_byte(GAME_PATH, 0x31C55, stage_select_primary)
    edit_nes_byte(GAME_PATH, 0x31C56, stage_select_secondary)

    # Boss intro screen
    edit_nes_byte(GAME_PATH, 0x31C65, stage_select_primary)
    edit_nes_byte(GAME_PATH, 0x31C66, stage_select_secondary)
    edit_nes_byte(GAME_PATH, 0x31C6E, stage_select_primary)
    edit_nes_byte(GAME_PATH, 0x31C72, stage_select_primary)


def scramble_weapon_palettes():
# This scrambles the color palettes for all of the weapons except the Mega Buster.
    # Gemini Laser
    edit_nes_byte(GAME_PATH, 0x4656, random.choice(LIGHT_COLORS))
    edit_nes_byte(GAME_PATH, 0x4657, random.choice(DARK_COLORS))

    # Needle Cannon
    edit_nes_byte(GAME_PATH, 0x465A, random.choice(LIGHT_COLORS))
    edit_nes_byte(GAME_PATH, 0x465B, random.choice(DARK_COLORS))

    # Hard Knuckle
    edit_nes_byte(GAME_PATH, 0x465E, random.choice(LIGHT_COLORS))
    edit_nes_byte(GAME_PATH, 0x465F, random.choice(DARK_COLORS))

    # Magnet Missile
    edit_nes_byte(GAME_PATH, 0x4662, random.choice(LIGHT_COLORS))
    edit_nes_byte(GAME_PATH, 0x4663, random.choice(DARK_COLORS))

    # Top Spin
    edit_nes_byte(GAME_PATH, 0x4666, random.choice(LIGHT_COLORS))
    edit_nes_byte(GAME_PATH, 0x4667, random.choice(DARK_COLORS))

    # Search Snake
    edit_nes_byte(GAME_PATH, 0x466A, random.choice(LIGHT_COLORS))
    edit_nes_byte(GAME_PATH, 0x466B, random.choice(DARK_COLORS))

    # Spark Shock
    edit_nes_byte(GAME_PATH, 0x4672, random.choice(LIGHT_COLORS))
    edit_nes_byte(GAME_PATH, 0x4673, random.choice(DARK_COLORS))

    # Shadow Blade
    edit_nes_byte(GAME_PATH, 0x467A, random.choice(LIGHT_COLORS))
    edit_nes_byte(GAME_PATH, 0x467B, random.choice(DARK_COLORS))

    # Rush Coil, Rush Jet, Rush Marine (all set to the same palette for consistency)
    rush_primary = random.choice(LIGHT_COLORS)
    rush_secondary = random.choice(DARK_COLORS)
    edit_nes_byte(GAME_PATH, 0x466E, rush_primary)
    edit_nes_byte(GAME_PATH, 0x466F, rush_secondary)
    edit_nes_byte(GAME_PATH, 0x4676, rush_primary)
    edit_nes_byte(GAME_PATH, 0x4677, rush_secondary)
    edit_nes_byte(GAME_PATH, 0x467E, rush_primary)
    edit_nes_byte(GAME_PATH, 0x467F, rush_secondary)


def scramble_weapon_energy_costs():
# Scrambles the energy cost for each weapon.
    # This first set of values is how many bars are used per shot for the weapons that use more than one bar of energy per shot. Weapons that use less are set to 0x01 and handled in the next set of values.
    edit_nes_byte(GAME_PATH, 0x3DF2C, random.randint(0x01, 0x03)) # Gemini Laser (default 2)
    edit_nes_byte(GAME_PATH, 0x3DF2D, 0x01) # Needle Cannon (default 1)
    edit_nes_byte(GAME_PATH, 0x3DF2E, random.randint(0x01, 0x03)) # Hard Knuckle (default 2)
    edit_nes_byte(GAME_PATH, 0x3DF2F, random.randint(0x01, 0x03)) # Magnet Missile (default 2)
    edit_nes_byte(GAME_PATH, 0x3DF30, 0x00) # Top Spin (default 0, do not change)
    edit_nes_byte(GAME_PATH, 0x3DF31, 0x01) # Search Snake (default 1)
    edit_nes_byte(GAME_PATH, 0x3DF32, random.randint(0x02, 0x04)) # Rush Coil (default 3)
    edit_nes_byte(GAME_PATH, 0x3DF33, random.choice([0x01, 0x01, 0x02])) # Spark Shock (default 1)
    edit_nes_byte(GAME_PATH, 0x3DF34, 0x01) # Rush Marine (default 1)
    edit_nes_byte(GAME_PATH, 0x3DF35, 0x01) # Shadow Blade (default 1)
    edit_nes_byte(GAME_PATH, 0x3DF36, 0x01) # Rush Jet (default 1)

    # This second set of values represents the number of times a weapon needs to be fired before a bar is used. This is primarily for weapons that use less than one bar of energy per shot normally.
    edit_nes_byte(GAME_PATH, 0x3DF39, random.randint(0x02, 0x06)) # Needle Cannon (default 4)
    edit_nes_byte(GAME_PATH, 0x3DF3D, random.randint(0x01, 0x03)) # Search Snake (default 2)
    if(int(read_nes_byte(GAME_PATH, 0x3DF33), 16) < 2): # only see if Spark Shock is eligible to cost 1/2 bars if the value in the above table is not set to 0x02 or higher
        edit_nes_byte(GAME_PATH, 0x3DF3F, random.randint(0x01, 0x02)) # Spark Shock (default 1)
    edit_nes_byte(GAME_PATH, 0x3DF41, random.randint(0x01, 0x03)) # Shadow Blade (default 2)


def scramble_weapon_behaviors():
# This scrambles the behaviors of the game's weapons.
    # Weapon projectile limits (the max number of each weapon that can be on screen at once) Setting any of these higher than the default usually causes collision issues (except Shadow Blade...?) Creates ghost projectiles that don't work
    edit_nes_byte(GAME_PATH, 0x3D34D, 0x03) # Mega Buster (default 3) setting this higher than 3 causes collision issues?
    edit_nes_byte(GAME_PATH, 0x3D34E, 0x01) # Gemini Laser (default 1)
    edit_nes_byte(GAME_PATH, 0x3D34F, 0x03) # Needle Cannon (default 3) setting this higher than 3 seems to cause collision issues
    edit_nes_byte(GAME_PATH, 0x3D350, 0x01) # Hard Knuckle (default 1)
    edit_nes_byte(GAME_PATH, 0x3D351, random.choice([0x01, 0x02])) # Magnet Missile (default 2)
    edit_nes_byte(GAME_PATH, 0x3D352, random.choice([0x00])) # Top Spin (default 0, do not recommend changing)
    edit_nes_byte(GAME_PATH, 0x3D353, random.choice([0x01, 0x02, 0x03])) # Search Snake (default 3)
    edit_nes_byte(GAME_PATH, 0x3D354, random.choice([0x01, 0x02, 0x03])) # Rush Coil (default 3)
    edit_nes_byte(GAME_PATH, 0x3D355, random.choice([0x01, 0x02])) # Spark Shock (default 2)
    edit_nes_byte(GAME_PATH, 0x3D356, random.choice([0x01, 0x02, 0x03])) # Rush Marine (default 3)
    edit_nes_byte(GAME_PATH, 0x3D357, random.choice([0x01, 0x02, 0x03])) # Shadow Blade (default 1)
    edit_nes_byte(GAME_PATH, 0x3D358, random.choice([0x01, 0x02, 0x03])) # Rush Jet (default 3)

    # Default projectile speed (affects all straight shooting weapons: Mega Buster, Needle Cannon, Magnet Missile, Gemini Laser, Spark Shock, Shadow Blade). Also messes with Hard Knuckle for some reason.
    edit_nes_byte(GAME_PATH, 0x3D166, random.choice([0x02, 0x03, 0x04, 0x05, 0x06, 0x07]))

    # Some notes on projectiles
    # (GE) 0x388FB (49) This fucks up Gemini Laser's wall collision, mostly documenting in the search for Needle Cannon's subroutine
    # (GE) 0x388FF (04) Can make Gemini Laser get stuck on walls
    # (GE) 0x3890B (04) Can make Gemini Laser bounce directly backwards
    # (GE) 0x38914 (29) Also fucks up Gemini Laser's wall collision
    # (GE) 0x38920 (06) Makes Gemini Laser get stuck to floors depending on value
    # (GE) 0x38923 (A0) Messes with the upwards bouncing laser sprite
    # (GE) 0x38925 (05) Messes with the downwards bouncing laser sprite
    # (GE) 0x38938 (A1) Causes Gemini Laser to vanish sometimes
    # (GE) 0x38940 (03) Causes Gemini Laser to bounce in reverse on some surfaces
    # (GE) 0x38945 (A1) Really messes with laser sprites and bouncing
    # (GE) 0x38948 (05) Messes with laser sprites
    # (GE) 0x3894D (04) Breaks laser bounce logic and splitting
    # (GE) 0x38952 (04) Can cause laser to always bounce upwards
    # (GE) 0x38955 (B2) Can lock one of the laser segments in place, creating almost a trap-type weapon
    # (HA) 0x38959 Controls the Hard Knuckle spawn animation
    # (HA) 0x38981 Hard Knuckle acceleration? Doesn't actually seem to affect anything so unsure
    # (NE) 0x3CD7B (16) Forces Mega Man into the Needle Cannon firing animation depending on what value is added
    # (GE) 0x3D169 (04) Actually interesting, it seems like higher values of this cause the laser to move slower
    # (GE) 0x3D16B (31) This causes Gemini Laser to always fire forwards depending on what value is assigned.
    # (GE) 0x3D16E (04) Causes some some of weird multi-directional laser if changed to certain values.
    # (HA) 0x3D170 Controls sprite position for Hard Knuckle depending on facing left/right
    # (GE) 0x3D174 (03) Messes with Gemini Laser's x spawn coordinate.
    # (GE) 0x3D17B (03) Somehow screws with Gemini Laser spawning in.
    # 0x3D17E (03) Actually messes with any projectile spawning in.
    # 0x3D18A (03) Default height offset for all projectiles.
    # 0x3D190 (03) Causes weird flickering when projectiles are shot if changed.
    # 0x3D192 (00) Controls the sprites for projectiles. Change at your own peril.
    # 0x3D1A9 (00) More sprite control for projectiles.
    # (GE) 0x3D1AF (03) Messes with Gemini Laser's wall collision if changed.
    # (NE) 0x3D1B1 (3B) Changing this prevents Needle Cannon from alternating up and down.
    # (HA) 0x3D1B3 (00) Completely screws with Mega Man's state if changed.
    # (GE) 0x3D230 (BA) Has something to do with laser wall collision.
    # (GE) 0x3D250 (03) Screws with Gemini Laser's x spawn coordinate.
    # (GE) 0x3D255 (03) Seems to mess with longevity of laser projectiles
    # (HA) 0x3D25F (03) Controls Hard Knuckle spawning
    # (HA) 0x3D263 Controls Hard Knuckle spawning somehow

    # Gemini Laser variables
    edit_nes_byte(GAME_PATH, 0x388F1, random.choice([0x01, 0x02, 0x03, 0x04, 0x05, 0x06])) # Speed of Gemini Laser after bouncing on a wall (default 03)
    edit_nes_byte(GAME_PATH, 0x3D230, random.randint(0x74, 0xF4)) # Length of time before Gemini Laser expires, and maybe does some other weird ass stuff? (default B4) 

    # Needle Cannon variables
    edit_nes_byte(GAME_PATH, 0x3CD81, random.choice([0xC0, 0xE0, 0xF0])) # Timer for Needle Cannon; lowering this value and raising 0x3CD8A decreases cooldown, raising this and lowering 0x3CD8A increases cooldown
    edit_nes_byte(GAME_PATH, 0x3CD8A, 0x100 - int(read_nes_byte(GAME_PATH, 0x3CD81), 16)) # See above, this value should be a factor of 0x100 to work properly
    edit_nes_byte(GAME_PATH, 0x3D34B, random.randint(0xF0, 0xFF)) # Y value for first shot height
    edit_nes_byte(GAME_PATH, 0x3D34C, random.randint(0x00, 0x0F)) # Y value for second shot height 

    # Hard Knuckle variables
    edit_nes_byte(GAME_PATH, 0x3D28D, random.randint(0x3F, 0xFF)) # Input sensitivity (default 80)
    edit_nes_byte(GAME_PATH, 0x3D29A, random.randint(0x08, 0x18)) # Delay, aka how long Mega Man pauses before shooting (default 10)
    edit_nes_byte(GAME_PATH, 0x3D282, random.randint(0x00, 0x02)) # Hard Knuckle acceleration (default 00)

    # Search Snake variables
    edit_nes_byte(GAME_PATH, 0x3D2CF, random.randint(0x00, 0x06)) # Search Snake vertical launch speed (default 03)
    edit_nes_byte(GAME_PATH, 0x3D2D9, random.randint(0x00, 0x04)) # Search Snake horizontal launch speed (default 01)

    # Shadow Blade variables
    edit_nes_byte(GAME_PATH, 0x3D2EB, random.choice([0x04, 0x07, 0x08, 0x0B, 0x0F])) # Shadow Blade shooting directions: see documentation for more info, but determines Shadow Blade throwable angles. Randomized between 5 upwards, 5 downwards, all 8, up/left/right, down/left right (Default 0B)
    edit_nes_byte(GAME_PATH, 0x3D2F7, random.randint(0x01, 0x07)) # Shadow Blade vertical launch speed (default 04)
    shadow_blade_returns = random.randint(0, 3) # Little randomization to see if Shadow Blade will boomerang at all. Default is a 25% chance to act like Metal Blade
    if shadow_blade_returns:
        edit_nes_byte(GAME_PATH, 0x3D2FC, random.randint(0x0A, 0x28)) # Shadow Blade range, i.e. how long it travels before boomeranging. Setting it high enough causes it to act like Metal Blade (default 14)
    else:
        edit_nes_byte(GAME_PATH, 0x3D2FC, 0xFF) # 0xFF is more than enough range for the blade to never boomerang


def scramble_boss_weakness_tables():
# Scrambles the weaknesses of the bosses in the game. Damage tables are listed by weapon, which is how this list is structured. See the attached notes for more details on the enemy damage tables.
    # To give every weapon at least one boss that it's effective against, use a 2d array to randomize with some logic
    effectiveness = [
    [0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01],
    [0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01],
    [0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01],
    [0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01],
    [0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01],
    [0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01],
    [0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01],
    [0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01]]
    # Mega Man 3 bosses all have 2 weaknesses so let's preserve that in the randomization
    weaknesses_1 = [0, 1, 2, 3, 4, 5, 6, 7]
    random.shuffle(weaknesses_1)
    weaknesses_2 = weaknesses_1
    random.shuffle(weaknesses_2)
    # These loops set immunities, weaknesses and semi-weaknesses across the Robot Master damage tables
    for i in range(len(effectiveness)):
        for j in range(i):
            effectiveness[i][j] = random.choice([0x00, 0x00, 0x01, 0x01, 0x01, 0x02])
        effectiveness[i][weaknesses_1[i]] = 0x04
        effectiveness[i][weaknesses_2[i]] = 0x04
    print(effectiveness)
    
    # Needle Cannon
    needle_effectiveness = [0x00, 0x00, 0x01, 0x01, 0x01, 0x02, 0x04, 0x04]
    random.shuffle(needle_effectiveness)
    edit_nes_byte(GAME_PATH, 0x142D0, needle_effectiveness[0]) # VS Needle Man
    edit_nes_byte(GAME_PATH, 0x142D7, needle_effectiveness[0]) # Also VS Needle Man but specifically for the head hammer extended state
    edit_nes_byte(GAME_PATH, 0x142D1, needle_effectiveness[1]) # VS Magnet Man
    edit_nes_byte(GAME_PATH, 0x142D2, needle_effectiveness[2]) # VS Top Man
    edit_nes_byte(GAME_PATH, 0x142D3, needle_effectiveness[3]) # VS Shadow Man
    edit_nes_byte(GAME_PATH, 0x142E0, needle_effectiveness[4]) # VS Hard Man
    edit_nes_byte(GAME_PATH, 0x142E2, needle_effectiveness[5]) # VS Spark Man
    edit_nes_byte(GAME_PATH, 0x142E4, needle_effectiveness[6]) # VS Snake Man
    edit_nes_byte(GAME_PATH, 0x142E6, needle_effectiveness[7]) # VS Gemini Man
    edit_nes_byte(GAME_PATH, 0x142E7, needle_effectiveness[7]) # VS Gemini Man's clone (yes it has a separate damage table for some reason)

    # Magnet Missile
    magnet_effectiveness = [0x00, 0x00, 0x01, 0x01, 0x01, 0x02, 0x04, 0x04]
    random.shuffle(magnet_effectiveness)
    edit_nes_byte(GAME_PATH, 0x143D0, magnet_effectiveness[0]) # VS Needle Man
    edit_nes_byte(GAME_PATH, 0x143D7, magnet_effectiveness[0]) # Also VS Needle Man but specifically for the head hammer extended state
    edit_nes_byte(GAME_PATH, 0x143D1, magnet_effectiveness[1]) # VS Magnet Man
    edit_nes_byte(GAME_PATH, 0x143D2, magnet_effectiveness[2]) # VS Top Man
    edit_nes_byte(GAME_PATH, 0x143D3, magnet_effectiveness[3]) # VS Shadow Man
    edit_nes_byte(GAME_PATH, 0x143E0, magnet_effectiveness[4]) # VS Hard Man
    edit_nes_byte(GAME_PATH, 0x143E2, magnet_effectiveness[5]) # VS Spark Man
    edit_nes_byte(GAME_PATH, 0x143E4, magnet_effectiveness[6]) # VS Snake Man
    edit_nes_byte(GAME_PATH, 0x143E6, magnet_effectiveness[7]) # VS Gemini Man
    edit_nes_byte(GAME_PATH, 0x143E7, magnet_effectiveness[7]) # VS Gemini Man's clone (yes it has a separate damage table for some reason)

    # Gemini Laser
    gemini_effectiveness = [0x00, 0x00, 0x01, 0x01, 0x01, 0x02, 0x04, 0x04]
    random.shuffle(gemini_effectiveness)
    edit_nes_byte(GAME_PATH, 0x144D0, gemini_effectiveness[0]) # VS Needle Man
    edit_nes_byte(GAME_PATH, 0x144D7, gemini_effectiveness[0]) # Also VS Needle Man but specifically for the head hammer extended state
    edit_nes_byte(GAME_PATH, 0x144D1, gemini_effectiveness[1]) # VS Magnet Man
    edit_nes_byte(GAME_PATH, 0x144D2, gemini_effectiveness[2]) # VS Top Man
    edit_nes_byte(GAME_PATH, 0x144D3, gemini_effectiveness[3]) # VS Shadow Man
    edit_nes_byte(GAME_PATH, 0x144E0, gemini_effectiveness[4]) # VS Hard Man
    edit_nes_byte(GAME_PATH, 0x144E2, gemini_effectiveness[5]) # VS Spark Man
    edit_nes_byte(GAME_PATH, 0x144E4, gemini_effectiveness[6]) # VS Snake Man
    edit_nes_byte(GAME_PATH, 0x144E6, gemini_effectiveness[7]) # VS Gemini Man
    edit_nes_byte(GAME_PATH, 0x144E7, gemini_effectiveness[7]) # VS Gemini Man's clone (yes it has a separate damage table for some reason)


if __name__ == "__main__":
# Mix it all up!
    scramble_stage_order()
    scramble_title_screen_palette()
    scramble_weapon_palettes()
    scramble_stage_select_palettes()
    scramble_stage_palettes()
    scramble_sprite_palettes()
    scramble_weapon_energy_costs()
    scramble_weapon_behaviors()
    scramble_boss_weakness_tables()