import struct
import random
import math

GAME_PATH = "MegaMan3.nes"

# The NES palette has 64 different colors, but many of them are repeats. This list excludes the duplicate instances of black.
VIABLE_COLORS = [0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x10, 0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17, 0x18, 0x19, 0x1A, 0x1B, 0x1C, 0x1D, 0x20, 0x21, 0x22, 0x23, 0x24, 0x25, 0x26, 0x27, 0x28, 0x29, 0x2A, 0x2B, 0x2C, 0x2D, 0x30, 0x31, 0x32, 0x33, 0x34, 0x35, 0x36, 0x37, 0x38, 0x39, 0x3A, 0x3B, 0x3C, 0x3D]

# The following lists are subsets of the total available color palette. NBW/NB/NW exclude black/white; dark and light color lists are self-explanatory, containing the darker or lighter half of available NES colors.
VIABLE_COLORS_NBW = [0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x10, 0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17, 0x18, 0x19, 0x1A, 0x1B, 0x1C, 0x21, 0x22, 0x23, 0x24, 0x25, 0x26, 0x27, 0x28, 0x29, 0x2A, 0x2B, 0x2C, 0x2D, 0x31, 0x32, 0x33, 0x34, 0x35, 0x36, 0x37, 0x38, 0x39, 0x3A, 0x3B, 0x3C, 0x3D]
DARK_COLORS = [0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17, 0x18, 0x19, 0x1A, 0x1B, 0x1C, 0x1D]
DARK_COLORS_NB = [0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17, 0x18, 0x19, 0x1A, 0x1B, 0x1C]
LIGHT_COLORS = [0x21, 0x22, 0x23, 0x24, 0x25, 0x26, 0x27, 0x28, 0x29, 0x2A, 0x2B, 0x2C, 0x30, 0x31, 0x32, 0x33, 0x34, 0x35, 0x36, 0x37, 0x38, 0x39, 0x3A, 0x3B, 0x3C, 0x3D]
LIGHT_COLORS_NW = [0x21, 0x22, 0x23, 0x24, 0x25, 0x26, 0x27, 0x28, 0x29, 0x2A, 0x2B, 0x2C, 0x31, 0x32, 0x33, 0x34, 0x35, 0x36, 0x37, 0x38, 0x39, 0x3A, 0x3B, 0x3C, 0x3D]

# This is how the lettering system (A-Z) works for the stage select, and possibly other things.
LETTERS = [0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F, 0x10, 0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17, 0x18, 0x19, 0x1A, 0x1B, 0x1C, 0x1D, 0x1E, 0x1F, 0x20, 0x21, 0x22, 0x23]
# This is for the Robot Master name generation piece
THREE_LETTER_NOUNS = [
    "box", "cup", "pen", "jar", "lid", "can", "pan", "pot", "mug", "rug",
    "mat", "bed", "cot", "tab", "bin", "bag", "key", "cap", "hat", "tie",
    "wig", "zip", "rod", "net", "peg", "pin", "tap", "tub", "fan", "pad",
    "map", "bar", "toy", "bat", "cue", "die", "ink", "jet", "kit", "log",
    "ram", "rim", "urn", "toe", "wax", "web", "zip", "arc", "axe", "orb"
]
FOUR_LETTER_NOUNS = [
    "book", "desk", "lamp", "door", "wall", "roof", "sofa", "seat", "rack", "sack",
    "lock", "safe", "case", "tree", "cart", "tote", "bowl", "dish", "slap", "vase",
    "tank", "tube", "pipe", "wire", "cord", "plug", "chip", "disk", "gear", "tool",
    "drum", "bell", "horn", "lens", "mask", "coat", "shoe", "boot", "sock", "belt",
    "coin", "bill", "card", "note", "file", "page", "pack", "clip", "hook", "tray"
] 
FIVE_LETTER_NOUNS = [
    "table", "chair", "couch", "shelf", "clock", "watch", "phone", "cable", "mouse", "spice",
    "glass", "plate", "spoon", "knife", "noise", "light", "bread", "frame", "brush", "libra",
    "towel", "sheet", "grass", "shirt", "water", "brick", "cloth", "agate", "heart", "steel",
    "purse", "crate", "boxer", "panel", "light", "cream", "voice", "drain", "paper", "valve",
    "wheel", "motor", "fancy", "cable", "lever", "chain", "screw", "ingot", "hinge", "plate"
]
SIX_LETTER_NOUNS = [
    "energy", "planet", "forest", "desert", "island", "valley", "stream", "meadow", "animal", "insect",
    "flower", "branch", "jungle", "garden", "castle", "palace", "temple", "church", "school", "office",
    "market", "bakery", "bridge", "tunnel", "taurus", "engine", "rocket", "record", "system", "device",
    "gadget", "camera", "sensor", "screen", "bottle", "bucket", "basket", "drawer", "closet", "window",
    "mirror", "statue", "figure", "symbol", "pencil", "guitar", "ladder", "napkin", "quartz", "tablet"
] 

# Enumerate which graphics sets actually have usable assets (i.e. not bosses)
VIABLE_GFX_SETS = [0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17, 0x18, 0x19, 0x1A, 0x1B, 0x1C, 0x1D, 0x1F, 0x20, 0x21, 0x22, 0x2D, 0x2E, 0x2F, 0x30, 0x31, 0x32, 0x33, 0x38, 0x39]

# This globally accessible list determines which enemies belong to which graphics set for enemy randomization.
ENEMY_GRAPHICS = [
    [0x00, [0x01, 0x09, 0x15, 0x1B, 0x1F, 0x38]], # Dada (available in set 0x01, 0x09, 0x15, 0x1B, 0x1F, 0x38)
    [0x01, [0x01, 0x09, 0x15, 0x1B, 0x1F, 0x38]], # Potton
    [0x02, [0x06, 0x1B]], # New Shotman
    [0x03, [0x17]], # Hammer Joe
    [0x04, [0x01, 0x0A, 0x0C]], # Bubukan
    [0x05, [0x06, 0x17, 0x1C, 0x20]], # Jamacy (climbing variant)
    [0x06, [0x06, 0x1B]], # Bomb Flier
    # [0x07] Mega Man's teleport animation (do not use)
    [0x08, [0x00, 0x0A, 0x0C, 0x19, 0x30, 0x31, 0x32, 0x33]], # Yambow
    [0x09, [0x00, 0x18, 0x21, 0x22]], # Metall DX (grounded)
    [0x0A, [0x00, 0x18, 0x21, 0x22]], # Cannon
    # [0x0B] Snake Man cloud platform (probably shouldn't use)
    [0x0C, [0x06, 0x17, 0x1C, 0x20]], # Jamacy (crawling variant)
    [0x0D, [0x06, 0x17, 0x1C, 0x20]], # Jamacy (crawling and climbing variant?)
    [0x0E, [0x03, 0x33, 0x38]], # Gyoraibo (Doc Gemini variant?)
    [0x0F, [0x09, 0x19]], # Magfly
    # [0x10] No clue what this is (do not use)
    [0x11, [0x32, 0x37]], # Junk Golem
    [0x12, [0x02, 0x2D, 0x30]], # Pickelman Bull
    [0x13, [0x0B]], # Bikky
    # [0x14] Mega Man?? (do not use)
    [0x15, [0x06, 0x17, 0x1C, 0x20]], # Jamacy (Alternate climbing variant? State for climbing variant?)
    [0x16, [0x09, 0x19]], # Magnet force (left)
    # [0x17] No clue what this is (do not use)
    [0x18, [0x04, 0x14, 0x1A, 0x1C, 0x1D, 0x20, 0x2F, 0x39]], # Nitron
    # [0x19] No clue what this is (do not use)
    [0x1A, [0x03, 0x33, 0x38]], # Gyoraibo (Normal Gemini variant?)
    [0x1B, [0x12, 0x2E]], # Hari Hari
    # [0x1C] # Penpen Maker (handle) (probably shouldn't use)
    [0x1D, [0x05, 0x1F]], # Returning Monking
    # [0x1E], # Weird invincible moving Returning Monking? Apparently unused (probably shouldn't use)
    [0x1F, [0x2F]], # Have "Su" Bee
    [0x20, [0x02, 0x03, 0x13, 0x1A, 0x22, 0x2D]], # Bolton & Nutton
    [0x21, [0x04, 0x14, 0x1A, 0x1C, 0x1D, 0x20, 0x2F, 0x39]], # Wanaan
    [0x22, [0x01, 0x0A, 0x0C]], # Needle Man needle obstacle (upwards variant)
    [0x23, [0x01, 0x0A, 0x0C]], # Needle Man needle obstacle (downwards variant)
    [0x24, [0x04, 0x14, 0x1A, 0x1C, 0x1D, 0x20, 0x2F, 0x39]], # Elec'n
    # [0x25] Magnet force animation (left) (probably shouldn't use)
    [0x26, [0x02, 0x2D, 0x30]], # Mechakkero
    # [0x27] Top Man top platform (probably shouldn't use)
    # [0x28 - 0x2B] No clue what this is (do not use)
    [0x2C, [0x03, 0x33, 0x38]], # Penpen
    # [0x2D] Spark Man rising platforms (probably shouldn't use)
    # [0x2E - 0x30] No clue what this is; 0x2F resembles Hari Hari but moves slowly forward and is not interactable (do not use)
    # [0x31] Magnet force animation (right) (probably shouldn't use)
    # [0x32, [0x03, 0x33, 0x38]], # Pole (these don't seem to work correctly when spawned randomly)
    # [0x33] # Holograph Mega Mans (don't use this in normal enemy randomization)
    # [0x34 - 0x35] No clue what this is (do not use)
    [0x36, [0x08, 0x09]], # Peterchy
    [0x37, [0x08]], # Walking Bomb
    [0x38, [0x00, 0x0A, 0x0C, 0x19, 0x30, 0x31, 0x32]], # Parasyu
    [0x39, [0x08]], # Hologran (static)
    [0x3A, [0x08]], # Hologran (moving)
    [0x3B, [0x04, 0x18, 0x1D]], # Bomber Pepe
    [0x3C, [0x00, 0x18, 0x21, 0x22]], # Metall DX (heli)
    [0x3D, [0x09, 0x19]], # Magnet force (right)
    # [0x3E] # Proto Man fight (don't use this in normal enemy randomization)
    # [0x3F - 0x46] No clue what this is (do not use)
    # [0x47 - 0x4E] The eight Robot Masters (NE, MA, GE, HA, TO, SN, SP, SH) (don't use in normal enemy randomization)
    # [0x4F] Mega Man's sprite? (do not use)
    # The following items had to be removed from the entity pool due to constantly spawning all the time
    # [0x50, [0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17, 0x18, 0x19, 0x1A, 0x1B, 0x1C, 0x1D, 0x1E, 0x1F, 0x20, 0x21, 0x22, 0x2D, 0x2E, 0x2F, 0x30, 0x31, 0x32, 0x33, 0x37, 0x38, 0x39]], # Large health capsule
    # [0x51, [0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17, 0x18, 0x19, 0x1A, 0x1B, 0x1C, 0x1D, 0x1E, 0x1F, 0x20, 0x21, 0x22, 0x2D, 0x2E, 0x2F, 0x30, 0x31, 0x32, 0x33, 0x37, 0x38, 0x39]], # Small health capsule
    # [0x52, [0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17, 0x18, 0x19, 0x1A, 0x1B, 0x1C, 0x1D, 0x1E, 0x1F, 0x20, 0x21, 0x22, 0x2D, 0x2E, 0x2F, 0x30, 0x31, 0x32, 0x33, 0x37, 0x38, 0x39]], # Large weapon energy capsule
    # [0x53, [0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17, 0x18, 0x19, 0x1A, 0x1B, 0x1C, 0x1D, 0x1E, 0x1F, 0x20, 0x21, 0x22, 0x2D, 0x2E, 0x2F, 0x30, 0x31, 0x32, 0x33, 0x37, 0x38, 0x39]], # Small weapon energy capsule
    # [0x54, [0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17, 0x18, 0x19, 0x1A, 0x1B, 0x1C, 0x1D, 0x1E, 0x1F, 0x20, 0x21, 0x22, 0x2D, 0x2E, 0x2F, 0x30, 0x31, 0x32, 0x33, 0x37, 0x38, 0x39]], # E Tank
    # [0x55, [0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17, 0x18, 0x19, 0x1A, 0x1B, 0x1C, 0x1D, 0x1E, 0x1F, 0x20, 0x21, 0x22, 0x2D, 0x2E, 0x2F, 0x30, 0x31, 0x32, 0x33, 0x37, 0x38, 0x39]], # 1-UP / extra life
    [0x56, [0x02, 0x03, 0x06, 0x09, 0x0B, 0x17, 0x19, 0x1B, 0x2D, 0x30, 0x33, 0x38]], # Surprise Box / ? Can
    # [0x57] # Giant Metall (don't use this in normal enemy randomization)
    # [0x58] # Doc Spark conveyor wheel (left) (probably shouldn't use)
    # [0x59] # Doc Spark conveyor wheel (right) (probably shouldn't use)
    # [0x5A] # Shadow Man collapsing platform (probably shouldn't use)
    # [0x5B] # No clue what this is (do not use)
    [0x5C, [0x13]], # Giant Springer
    [0x5D, [0x06, 0x09, 0x19, 0x1B]], # Hard Knuckle destructible wall
    # [0x5E] # Kamegoro Maker (don't use this in normal enemy randomization)
    # [0x5F] # Kamegoro Maker currents (do not use)
    [0x60, [0x12, 0x15, 0x2E]], # Petit Snakey
    [0x61, [0x12, 0x15, 0x2E]], # Petit Snakey (upside down variant)
    [0x62, [0x16, 0x31]], # Komasaburo 
    [0x63, [0x32, 0x37]], # Spark Man junk block
    [0x64, [0x02, 0x03, 0x13, 0x1A, 0x22, 0x2D]], # Electric Gabyoall
    [0x65, [0x02, 0x03, 0x13, 0x1A, 0x22, 0x2D]], # Electric Gabyoall (wider variant)
    # [0x66 - 0x67] Big Snakey body and init sprites (do not use)
    # [0x68 - 0x6F] The eight Doc Robots (FL, BU, QU, WO, CR, AI, ME, HE) (don't use in normal enemy randomization)
    # [0x70 - 0x71] Big Snakey eye and mouth sprites (do not use)
    # [0x72 - 0x73] Tama eye and body sprites (do not use)
    # [0x74] Seal that Proto Man destroys in Gemini Man's stage (do not use)
    # [0x75 - 0x77] Tama tail, body, and init sprites (do not use)
    # [0x78] Proto Man (variant that opens the seal in Gemini Man's stage) (do not use)
    # [0x79 - 0x80] Gamma sprites (don't use in normal enemy randomization)
    # [0x81] Yellow Devil MK-II (don't use in normal enemy randomization)
    # [0x82 - 0x89] Wily Machine 3 sprites (don't use in normal enemy randomization)
    # [0x8A] Teleporter (do not use)
]
CHANCE_ITEMS_SPAWN = 3 # Percentage chance for stage entities to be replaced with items. 3% by default
ITEM_LIST = [0x50, 0x51, 0x52, 0x53, 0x54, 0x55] # List of items (enumerated above)

# This globally accessible list is used for randomizing what bosses appear in what stage. The list items are the boss entity ID and graphics set. It seems that the bank 0 and 1 values are actually automatically handled with the graphics set value.
RANDOMIZED_BOSSES = [
    [0x47, 0x25], # Needle Man  
    [0x48, 0x23], # Magnet Man
    [0x49, 0x27], # Gemini Man
    [0x4A, 0x24], # Hard Man
    [0x4B, 0x2A], # Top Man
    [0x4C, 0x26], # Snake Man
    [0x4D, 0x28], # Spark Man
    [0x4E, 0x29] # Shadow Man
    ]
random.shuffle(RANDOMIZED_BOSSES)

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


def convert_string_to_mm3_text(text):
    build_string = []
    for char in text:
        build_string.append(ord(char.lower()) - 97 + 0x0A)
    return build_string


def replace_entities(graphics_set, enemy_lower_bound, enemy_upper_bound, *args):
    replace_enemies = random.choice(VIABLE_GFX_SETS) # choose random graphics set
    # If additional arguments are given to restrict the graphics set chosen, use that list instead
    if args:
        replace_enemies = args[0]
    replace_enemy_set = []
    for i in ENEMY_GRAPHICS:
        if replace_enemies in i[1]: # add only enemies that exist in this graphics set to the possible enemy pool
            replace_enemy_set.append(i[0])
    edit_nes_byte(GAME_PATH, graphics_set, replace_enemies) # Graphics set
    for i in range(enemy_lower_bound, enemy_upper_bound):
        if random.randint(0, 99) < CHANCE_ITEMS_SPAWN: # add a chance to replace an enemy with an item (3% by default)
            edit_nes_byte(GAME_PATH, i, random.choice(ITEM_LIST))
        else:
            edit_nes_byte(GAME_PATH, i, random.choice(replace_enemy_set))


def activate_burst_chaser():
# Speeds up the game a bit by increasing Mega Man's speed, bullet speed, and a few other variables.
    edit_nes_byte(GAME_PATH, 0x3CD57, 0x03) # Mega Man's movement speed (default 01)
    edit_nes_byte(GAME_PATH, 0x3D166, 0x07) # Bullet speed (default 04)
    edit_nes_byte(GAME_PATH, 0x3D77D, 0x4C) # Invicibility time after taking damage (default 3C)
    edit_nes_byte(GAME_PATH, 0x3D3D5, 0x03) # Mega Man's sliding speed (default 02)
    edit_nes_byte(GAME_PATH, 0x3D4CC, 0x02) # Ladder climbing speed (default 01)


def fix_scanline():
# Fixes the annoying scanline issue on the stage select. Yep, it's one byte.
    edit_nes_byte(GAME_PATH, 0x3C4E0, 0xCF)


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


def randomize_needle_man_entities():
# Randomizes the entities for Needle Man's stage. Replacing entities is surprisingly convoluted because of all the changes required for the graphics sets etc.
    # Hari Haris on the first screen
    replace_entities(0xA70, 0xE10, 0xE14)
    
    # Yambows, Metalls, and Cannons on second screen
    replace_entities(0xA72, 0xE14, 0xE21)

    # Needles on third screen
    replace_entities(0xA74, 0xE21, 0xE29)

    # Hari Hari on fourth screen
    replace_entities(0xA76, 0xE29, 0xE2A)

    # Hammer Joes on fifth screen
    replace_entities(0xA78, 0xE2B, 0xE2D)

    # Bikky on the sixth screen
    replace_entities(0xA7A, 0xE2D, 0xE2E)

    # Randomizes the boss himself
    edit_nes_byte(GAME_PATH, 0xE2E, RANDOMIZED_BOSSES[0][0])
    edit_nes_byte(GAME_PATH, 0xA7E, RANDOMIZED_BOSSES[0][1])


def randomize_magnet_man_entities():
# Randomizes the entities for Magnet Man's stage.
    # Magflys on first screen
    replace_entities(0x2A70, 0x2E10, 0x2E17)
    
    # Proto Man encounter on screen 2 (don't replace this lmao)
    # replace_entities(0x2A72, 0x2E17, 0x2E18)

    # Giant Springers on third screen
    replace_entities(0x2A74, 0x2E18, 0x2E1A)

    # Peterchys on fourth screen
    replace_entities(0x2A76, 0x2E1A, 0x2E1C)

    # Peterchys and magnet force objects on fifth screen
    replace_entities(0x2A78, 0x2E1C, 0x2E23)

    # Health pickups on sixth screen
    replace_entities(0x2A7A, 0x2E23, 0x2E27)

    # Seventh screen with yoku blocks, can only randomize to 0x09 and 0x19 to not mess up yoku block sprites
    replace_entities(0x2A7C, 0x2E27, 0x2E2D, random.choice([0x09, 0x19]))

    # Eighth screen with just pickups
    replace_entities(0x2A7E, 0x2E2D, 0x2E31)

    # Ninth screen with New Shotman
    replace_entities(0x2A80, 0x2E31, 0x2E32)

    # Tenth screen with Giant Springer
    replace_entities(0x2A82, 0x2E32, 0x2E33)

    # Randomizes the boss himself
    edit_nes_byte(GAME_PATH, 0x2E33, RANDOMIZED_BOSSES[1][0])
    edit_nes_byte(GAME_PATH, 0x2A86, RANDOMIZED_BOSSES[1][1])


def randomize_gemini_man_entities():
# Randomizes the entities for Gemini Man's stage.
    # First screen Bomber Pepes and Nitrons; choose a graphics set that is compatible with the star background
    replace_entities(0x4A70, 0x4E10, 0x4E25, random.choice([0x04, 0x14, 0x1A, 0x1C, 0x1D, 0x20, 0x2F, 0x39]))

    # Second screen with Proto Man (don't replace this)
    # replace_entities(0x4A72, 0x4E25, 0x4E27)

    # Third screen with pickups; replace with a graphics set that is compatible with Poles
    replace_entities(0x4A74, 0x4E27, 0x4E2A, random.choice([0x03, 0x33, 0x38]))

    # Fourth screen with Poles but no other entities?
    # replace_entities(0x4A76, 0x4E2A, 0x4E2A)

    # Fifth screen with Yambows, Penpen Makers; put the Penpen Makers back
    replace_entities(0x4A78, 0x4E2A, 0x4E32, random.choice([0x03, 0x33, 0x38]))
    edit_nes_byte(GAME_PATH, 0x4E2D, 0x1C)
    edit_nes_byte(GAME_PATH, 0x4E30, 0x1C)

    # Sixth screen with just a health pickup... I'll let the player have this one
    # replace_entities(0x4A7A, 0x4E32, 0x4E32)

    # Seventh screen with Yambows and Gyoraibos; restrict the available enemies to only those graphics sets that have the correct water splash animation
    replace_entities(0x4A7C, 0x4E33, 0x4E48, random.choice([0x03, 0x33, 0x38]))
    edit_nes_byte(GAME_PATH, 0x4E37, 0x54) # I'll leave the E-Tanks be
    edit_nes_byte(GAME_PATH, 0x4E46, 0x51) # This entity often causes softlocks since it's positioned right over the ladder; replace it with a small health pickup so that it falls out of the way

    # Eighth screen with Mechakkeros
    replace_entities(0x4A7E, 0x4E49, 0x4E4B)

    # Ninth screen with Bikky
    replace_entities(0x4A80, 0x4E4B, 0x4E4C)

    # Randomize the boss himself
    edit_nes_byte(GAME_PATH, 0x4E4C, RANDOMIZED_BOSSES[2][0])
    edit_nes_byte(GAME_PATH, 0x4A84, RANDOMIZED_BOSSES[2][1])


def randomize_hard_man_entities():
# Randomizes the entities for Hard Man's stage.
    # First screen with Have "Su" Bees, Wanaans, health pickup
    replace_entities(0x6A70, 0x6E10, 0x6E1A)

    # Second screen with Hammer Joe
    replace_entities(0x6A72, 0x6E1A, 0x6E1B)

    # Third screen with Returning Monkings
    replace_entities(0x6A74, 0x6E1B, 0x6E1D)

    # Fourth screen with health and Hammer Joe
    replace_entities(0x6A76, 0x6E1E, 0x6E1F)

    # Fifth screen with Returning Monking
    replace_entities(0x6A78, 0x6E1F, 0x6E20)

    # Sixth screen with Pickelman Bulls, leave the E-Tank
    replace_entities(0x6A7A, 0x6E20, 0x6E23)

    # Seventh screen with Metalls and health
    replace_entities(0x6A7C, 0x6E24, 0x6E29)

    # Eighth screen with Have "Su" Bee and Wanaans
    replace_entities(0x6A7E, 0x6E29, 0x6E34)

    # Ninth screen with Proto Man, do not replace
    # replace_entities(0x6A80, 0x6E34, 0x6E35)

    # Tenth screen with health pickup, I'll let the player have this one
    # replace_entities(0x6A82, 0x6E35, 0x6E36)

    # Eleventh screen with Bikky
    replace_entities(0x6A84, 0x6E36, 0x6E37)

    # Randomize the boss himself
    edit_nes_byte(GAME_PATH, 0x6E37, RANDOMIZED_BOSSES[3][0])
    edit_nes_byte(GAME_PATH, 0x6A88, RANDOMIZED_BOSSES[3][1])
 

def scramble_stage_entities():
# This scrambles all the stage entities.
    randomize_needle_man_entities()
    randomize_magnet_man_entities()
    randomize_gemini_man_entities()
    randomize_hard_man_entities()


def scramble_music():
# This scrambles all the music in the game.
    robot_master_music_list = [0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08]
    random.shuffle(robot_master_music_list)
    wily_stage_music_list = [0x09, 0x09, 0x0A, 0x0A, 0x0B, 0x0B]
    random.shuffle(wily_stage_music_list)
    # Equally distribute the eight initial stage themes to random stages
    for i in range(0x3CD1C, 0x3CD24):
        edit_nes_byte(GAME_PATH, i, robot_master_music_list[i - 0x3CD1C]) 
    # For Doc Robot stages, just pull stage themes from the previously built array
    for i in range(0x3CD24, 0x3CD28):
        edit_nes_byte(GAME_PATH, i, robot_master_music_list[(i - 0x3CD24) * 2])
    # Pull equally distributed Wily stage themes for the fortress stages
    for i in range(0x3CD28, 0x3CD2E):
        edit_nes_byte(GAME_PATH, i, wily_stage_music_list[i - 0x3CD28])


def scramble_sprite_palettes():
# This scrambles the color schemes for the enemies and bosses in the game. Black and white are not replaced to maintain some level of graphical integrity. Light colors are replaced with other light colors and dark colors are replaced with other dark colors.
    for i in range(0x2040, 0x220F):
        if int(read_nes_byte(GAME_PATH, i), 16) not in [0x0F, 0x20, 0x30]:
            if(int(read_nes_byte(GAME_PATH, i), 16) in LIGHT_COLORS):
                edit_nes_byte(GAME_PATH, i, random.choice(LIGHT_COLORS_NW))
            else:
                edit_nes_byte(GAME_PATH, i, random.choice(DARK_COLORS_NB))
    # Specific check for Hard Man's sprite since he's composed of two dark colors and looks awful with totally random colors lmao
    edit_nes_byte(GAME_PATH, 0x2166, 0x10)
    # Another check for Proto Man since he suffers from the same issue
    edit_nes_byte(GAME_PATH, 0x20F2, 0x10) # Proto Man grey
    edit_nes_byte(GAME_PATH, 0x20F3, random.randint(0x11, 0x1C)) # Proto Man red


def scramble_sprite_health():
# Scrambles the health values for the enemies of the game. Bosses are not affected.
    for i in range(0x410, 0x49F):
        if int(read_nes_byte(GAME_PATH, i), 16) not in [0x1C, 0xFF, 0x00]: # Do not scramble bosses or any entity with null/zero HP
            edit_nes_byte(GAME_PATH, i, random.randint(0x01, math.floor(int(read_nes_byte(GAME_PATH, i), 16) * 1.5)))


def scramble_sprite_speed():
# Scrambles the speed values for the enemies of the game.
    for i in range(0x510, 0x58F):
        if int(read_nes_byte(GAME_PATH, i), 16) not in [0x1C, 0xFF, 0x00]: # Do not scramble bosses or any entity with no movement value to avoid causing weird issues
            edit_nes_byte(GAME_PATH, i, random.randint(0x01, 0x0A))


def randomize_needle_man_graphics():
# Randomizes the graphics for Needle Man's stage.
    for i in range(0xA92, 0xAB6):
        if i not in [0xAA2, 0xAA3, 0xAA4, 0xAA5]:
            if int(read_nes_byte(GAME_PATH, i), 16) not in [0x0F, 0x20, 0x30]:
                if(int(read_nes_byte(GAME_PATH, i), 16) in LIGHT_COLORS):
                    edit_nes_byte(GAME_PATH, i, random.choice(LIGHT_COLORS_NW))
                else:
                    edit_nes_byte(GAME_PATH, i, random.choice(DARK_COLORS_NB))

    # Some fixes for bizarre color shenanigans with ladders and backgrounds
    edit_nes_byte(GAME_PATH, 0xA9D, random.randint(0x00, 0x0C))
    edit_nes_byte(GAME_PATH, 0xAA1, int(read_nes_byte(GAME_PATH, 0xA99), 16))
    edit_nes_byte(GAME_PATH, 0xAA8, int(read_nes_byte(GAME_PATH, 0xA94), 16))
    edit_nes_byte(GAME_PATH, 0xAA9, int(read_nes_byte(GAME_PATH, 0xA95), 16))
    edit_nes_byte(GAME_PATH, 0xAAF, int(read_nes_byte(GAME_PATH, 0xA9B), 16))
    edit_nes_byte(GAME_PATH, 0xAB0, int(read_nes_byte(GAME_PATH, 0xA9C), 16))
    edit_nes_byte(GAME_PATH, 0xAB1, int(read_nes_byte(GAME_PATH, 0xA9D), 16))


def randomize_magnet_man_graphics():
# Randomizes the graphics for Magnet Man's stage.
    for i in range(0x2A92, 0x2AB5):
        if int(read_nes_byte(GAME_PATH, i), 16) not in [0x0F, 0x20, 0x30]:
            if(int(read_nes_byte(GAME_PATH, i), 16) in LIGHT_COLORS):
                edit_nes_byte(GAME_PATH, i, random.choice(LIGHT_COLORS_NW))
            else:
                edit_nes_byte(GAME_PATH, i, random.choice(DARK_COLORS_NB))

    # This check is made for the sky colors at the beginning so they don't look incoherent.
    edit_nes_byte(GAME_PATH, 0x2AA0, int(read_nes_byte(GAME_PATH, 0x2A9B), 16))
    edit_nes_byte(GAME_PATH, 0x2AA1, int(read_nes_byte(GAME_PATH, 0x2A9C), 16))

    # Magnet Man's background is very harsh on the eyes with randomized colors; this should alleviate some of the visual pain
    magnet_background = random.randint(0x00, 0x0C)
    edit_nes_byte(GAME_PATH, 0x2A97, magnet_background + 0x10)
    edit_nes_byte(GAME_PATH, 0x2A98, magnet_background)
    edit_nes_byte(GAME_PATH, 0x2AB4, int(read_nes_byte(GAME_PATH, 0x2A98), 16))

    # Prevent the screen from weirdly changing palette after first screen
    for i in range(0x2AA6, 0x2AAE):
        edit_nes_byte(GAME_PATH, i, int(read_nes_byte(GAME_PATH, i - 0x14), 16))

    # Fix background colors after that palette shift
    edit_nes_byte(GAME_PATH, 0x2AAF, int(read_nes_byte(GAME_PATH, 0x2AAB), 16))


def randomize_gemini_man_graphics():
# Randomizes the graphics for Gemini Man's stage.
    for i in range(0x4A92, 0x4AA2):
        if i not in [0x4AA2, 0x4AA3, 0x4AA4, 0x4AA5, 0x4AB6, 0x4AB7, 0x4AB8, 0x4AB9, 0x4ACA, 0x4ACB, 0x4ACC, 0x4ACD]: # Animated tile values, do not change
            if int(read_nes_byte(GAME_PATH, i), 16) not in [0x0F, 0x20, 0x30]:
                if(int(read_nes_byte(GAME_PATH, i), 16) in LIGHT_COLORS):
                    edit_nes_byte(GAME_PATH, i, random.choice(LIGHT_COLORS_NW))
                else:
                    edit_nes_byte(GAME_PATH, i, random.choice(DARK_COLORS_NB))

    # Animated tiles; Gemini Man's animations are more complicated than the rest of the stages and are stored in a different, more annoying to parse way as well
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

    # Fix block colors; block animations begin at 0x125BF
    color_1 = int(read_nes_byte(GAME_PATH, 0x125BF), 16) # Light blue highlight
    color_2 = int(read_nes_byte(GAME_PATH, 0x125C0), 16) # Blue 
    color_3 = int(read_nes_byte(GAME_PATH, 0x125C3), 16) # Red
    color_4 = int(read_nes_byte(GAME_PATH, 0x125C6), 16) # Yellow
    new_color_1 = random.randint(0x31, 0x3C)
    new_color_2 = random.randint(0x11, 0x1C)
    new_color_3 = random.randint(0x11, 0x1C)
    new_color_4 = random.randint(0x11, 0x1C)

    for i in range(0x4AA6, 0x4ADE):
        if int(read_nes_byte(GAME_PATH, i), 16) == color_1:
           edit_nes_byte(GAME_PATH, i, new_color_1)
        elif int(read_nes_byte(GAME_PATH, i), 16) == color_2:
           edit_nes_byte(GAME_PATH, i, new_color_2)
        elif int(read_nes_byte(GAME_PATH, i), 16) == color_3:
           edit_nes_byte(GAME_PATH, i, new_color_3)
        elif int(read_nes_byte(GAME_PATH, i), 16) == color_4:
           edit_nes_byte(GAME_PATH, i, new_color_4)

    for i in range(0x125BF, 0x125D1):
        if int(read_nes_byte(GAME_PATH, i), 16) == color_1:
           edit_nes_byte(GAME_PATH, i, new_color_1)
        elif int(read_nes_byte(GAME_PATH, i), 16) == color_2:
           edit_nes_byte(GAME_PATH, i, new_color_2)
        elif int(read_nes_byte(GAME_PATH, i), 16) == color_3:
           edit_nes_byte(GAME_PATH, i, new_color_3)
        elif int(read_nes_byte(GAME_PATH, i), 16) == color_4:
           edit_nes_byte(GAME_PATH, i, new_color_4)

    # Fix for the ground changing color after Proto Man cutscene
    edit_nes_byte(GAME_PATH, 0x4ADB, int(read_nes_byte(GAME_PATH, 0x4A9F), 16))
    edit_nes_byte(GAME_PATH, 0x4ADC, int(read_nes_byte(GAME_PATH, 0x4AA0), 16))
    edit_nes_byte(GAME_PATH, 0x4ADD, int(read_nes_byte(GAME_PATH, 0x4AA1), 16))


def randomize_hard_man_graphics():
# Randomizes the graphics for Hard Man's stage.
    for i in range(0x6A92, 0x6AA2):
        if int(read_nes_byte(GAME_PATH, i), 16) not in [0x0F, 0x20, 0x30]:
            if(int(read_nes_byte(GAME_PATH, i), 16) in LIGHT_COLORS):
                edit_nes_byte(GAME_PATH, i, random.choice(LIGHT_COLORS_NW))
            else:
                edit_nes_byte(GAME_PATH, i, random.choice(DARK_COLORS_NB))
    
    # The rocks look really terrible with totally random color schemes, so apply a gradient
    rock_base_color = random.randint(0x01, 0x0C)
    edit_nes_byte(GAME_PATH, 0x6A95, rock_base_color)
    edit_nes_byte(GAME_PATH, 0x6A94, rock_base_color + 0x20)
    edit_nes_byte(GAME_PATH, 0x6A93, rock_base_color + 0x30)

def scramble_stage_palettes():
# This scrambles the color schemes for the stages in the game. Black and white are not replaced to maintain some level of graphical integrity, and black and white are excluded from the possible color options to prevent extreme eyesore.
    randomize_needle_man_graphics()
    randomize_magnet_man_graphics()
    randomize_gemini_man_graphics()
    randomize_hard_man_graphics()

    # Top Man
    for i in range(0x8A92, 0x8AC6):
        if i not in [0x8AB6, 0x8AB7, 0x8AB8, 0x8AB9]: # These specific values are for tile animation and should not be messed with
            if int(read_nes_byte(GAME_PATH, i), 16) not in [0x0F, 0x20, 0x30]:
                if(int(read_nes_byte(GAME_PATH, i), 16) in LIGHT_COLORS):
                    edit_nes_byte(GAME_PATH, i, random.choice(LIGHT_COLORS_NW))
                else:
                    edit_nes_byte(GAME_PATH, i, random.choice(DARK_COLORS_NB))
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
                edit_nes_byte(GAME_PATH, i, random.choice(DARK_COLORS_NB))
    # Animated tile values (sky and clouds)
    edit_nes_byte(GAME_PATH, 0x125A0, random.choice(LIGHT_COLORS_NW))
    edit_nes_byte(GAME_PATH, 0xAAA0, int(read_nes_byte(GAME_PATH, 0x125A0), 16))
    edit_nes_byte(GAME_PATH, 0xAAA1, int(read_nes_byte(GAME_PATH, 0x125A0), 16))
    edit_nes_byte(GAME_PATH, 0x125A2, int(read_nes_byte(GAME_PATH, 0x125A0), 16))
    edit_nes_byte(GAME_PATH, 0x125A3, int(read_nes_byte(GAME_PATH, 0x125A0), 16))
    # This controls the color for the cloud animation, turn it to white if this would cause a color overflow when adding 0x10
    if int(read_nes_byte(GAME_PATH, 0xAAA0), 16) > 0x2F:
        edit_nes_byte(GAME_PATH, 0x1259F, 0x20)
    else:
        edit_nes_byte(GAME_PATH, 0x1259F, int(read_nes_byte(GAME_PATH, 0xAAA0), 16) + 0x10)
    
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
                edit_nes_byte(GAME_PATH, i, random.choice(DARK_COLORS_NB))
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
    stage_select_primary = random.choice(LIGHT_COLORS_NW)
    stage_select_secondary = random.choice(DARK_COLORS_NB)
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


def scramble_robot_master_names():
# Purely cosmetic, but changes the Robot Master names.
    list_new_names = [] # This just ensures that no name is generated twice
    needle_new_name = random.choice(SIX_LETTER_NOUNS)
    list_new_names.append(needle_new_name)
    magnet_new_name = random.choice(SIX_LETTER_NOUNS)
    while magnet_new_name in list_new_names: # If the chosen name is already in the list of names, reroll
        magnet_new_name = random.choice(SIX_LETTER_NOUNS)
    list_new_names.append(magnet_new_name)
    gemini_new_name = random.choice(SIX_LETTER_NOUNS)
    while gemini_new_name in list_new_names: # If the chosen name is already in the list of names, reroll
        gemini_new_name = random.choice(SIX_LETTER_NOUNS)
    list_new_names.append(gemini_new_name)
    hard_new_name = random.choice(FOUR_LETTER_NOUNS)
    list_new_names.append(hard_new_name)
    top_new_name = random.choice(THREE_LETTER_NOUNS)
    list_new_names.append(top_new_name)
    snake_new_name = random.choice(FIVE_LETTER_NOUNS)
    while snake_new_name in list_new_names: # If the chosen name is already in the list of names, reroll
        snake_new_name = random.choice(FIVE_LETTER_NOUNS)
    list_new_names.append(snake_new_name)
    spark_new_name = random.choice(FIVE_LETTER_NOUNS)
    while spark_new_name in list_new_names: # If the chosen name is already in the list of names, reroll
        spark_new_name = random.choice(FIVE_LETTER_NOUNS)
    list_new_names.append(spark_new_name)
    shadow_new_name = random.choice(SIX_LETTER_NOUNS)
    while shadow_new_name in list_new_names: # If the chosen name is already in the list of names, reroll
        shadow_new_name = random.choice(SIX_LETTER_NOUNS)
    list_new_names.append(shadow_new_name)

    # This section is used somewhere but unsure where
    for i in range(0x61F1, 0x61F7): # "Needle Man"
        edit_nes_byte(GAME_PATH, i, convert_string_to_mm3_text(needle_new_name)[i - 0x61F1])
    for i in range(0x61FB, 0x6201): # "Magnet Man"
        edit_nes_byte(GAME_PATH, i, convert_string_to_mm3_text(magnet_new_name)[i - 0x61FB])
    for i in range(0x6205, 0x620B): # "Gemini Man"
        edit_nes_byte(GAME_PATH, i, convert_string_to_mm3_text(gemini_new_name)[i - 0x6205])
    for i in range(0x620F, 0x6213): # "Hard Man"
        edit_nes_byte(GAME_PATH, i, convert_string_to_mm3_text(hard_new_name)[i - 0x620F])
    for i in range(0x6219, 0x621C): # "Top Man"
        edit_nes_byte(GAME_PATH, i, convert_string_to_mm3_text(top_new_name)[i - 0x6219])
    for i in range(0x6223, 0x6228): # "Snake Man"
        edit_nes_byte(GAME_PATH, i, convert_string_to_mm3_text(snake_new_name)[i - 0x6223])
    for i in range(0x622D, 0x6232): # "Spark Man"
        edit_nes_byte(GAME_PATH, i, convert_string_to_mm3_text(spark_new_name)[i - 0x622D])
    for i in range(0x6237, 0x623D): # "Shadow Man"   
        edit_nes_byte(GAME_PATH, i, convert_string_to_mm3_text(shadow_new_name)[i - 0x6237])

    # Actual stage select stuff?
    for i in range(0x639E, 0x63A4): # "Needle Man"
        edit_nes_byte(GAME_PATH, i, convert_string_to_mm3_text(needle_new_name)[i - 0x639E])
    for i in range(0x63F0, 0x63F6): # "Magnet Man"
        edit_nes_byte(GAME_PATH, i, convert_string_to_mm3_text(magnet_new_name)[i - 0x63F0])
    for i in range(0x63E7, 0x63ED): # "Gemini Man"
        edit_nes_byte(GAME_PATH, i, convert_string_to_mm3_text(gemini_new_name)[i - 0x63E7])
    for i in range(0x63C3, 0x63C7): # "Hard Man"
        edit_nes_byte(GAME_PATH, i, convert_string_to_mm3_text(hard_new_name)[i - 0x63C3])
    for i in range(0x63CC, 0x63CF): # "Top Man"
        edit_nes_byte(GAME_PATH, i, convert_string_to_mm3_text(top_new_name)[i - 0x63CC])
    for i in range(0x6395, 0x639A): # "Snake Man"
        edit_nes_byte(GAME_PATH, i, convert_string_to_mm3_text(snake_new_name)[i - 0x6395])
    for i in range(0x638C, 0x6391): # "Spark Man"
        edit_nes_byte(GAME_PATH, i, convert_string_to_mm3_text(spark_new_name)[i - 0x638C])
    for i in range(0x63F9, 0x63FF): # "Shadow Man"   
        edit_nes_byte(GAME_PATH, i, convert_string_to_mm3_text(shadow_new_name)[i - 0x63F9])


def scramble_weapon_palettes():
# This scrambles the color palettes for all of the weapons except the Mega Buster.
    # Gemini Laser
    gemini_primary = random.randint(0x20, 0x2C)
    gemini_secondary = random.randint(0x10, 0x1C)
    edit_nes_byte(GAME_PATH, 0x4656, gemini_primary)
    edit_nes_byte(GAME_PATH, 0x4657, gemini_secondary)

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

    # Weapon get screen palettes
    # Gemini Laser
    edit_nes_byte(GAME_PATH, 0x31BD8, 0x30)
    edit_nes_byte(GAME_PATH, 0x31BD9, gemini_primary + 0x10)
    edit_nes_byte(GAME_PATH, 0x31BDA, gemini_secondary)
    edit_nes_byte(GAME_PATH, 0x31BDC, gemini_secondary - 0x10)
    edit_nes_byte(GAME_PATH, 0x31BDD, gemini_primary)
    edit_nes_byte(GAME_PATH, 0x31BDE, gemini_secondary)

    # Needle Cannon


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
    edit_nes_byte(GAME_PATH, 0x3D351, random.choice([0x01, 0x02, 0x03])) # Magnet Missile (default 2)
    edit_nes_byte(GAME_PATH, 0x3D352, random.choice([0x00])) # Top Spin (default 0, do not recommend changing)
    edit_nes_byte(GAME_PATH, 0x3D353, random.choice([0x02, 0x03])) # Search Snake (default 3)
    edit_nes_byte(GAME_PATH, 0x3D354, random.choice([0x02, 0x03])) # Rush Coil (default 3)
    edit_nes_byte(GAME_PATH, 0x3D355, random.choice([0x01, 0x02])) # Spark Shock (default 2)
    edit_nes_byte(GAME_PATH, 0x3D356, random.choice([0x02, 0x03])) # Rush Marine (default 3)
    edit_nes_byte(GAME_PATH, 0x3D357, random.choice([0x01, 0x02, 0x03])) # Shadow Blade (default 1)
    edit_nes_byte(GAME_PATH, 0x3D358, random.choice([0x02, 0x03])) # Rush Jet (default 3)

    # Default projectile speed (affects all straight shooting weapons: Mega Buster, Needle Cannon, Magnet Missile, Gemini Laser, Spark Shock, Shadow Blade). Also appears to mess with Hard Knuckle for some reason.
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
    edit_nes_byte(GAME_PATH, 0x3D2F7, random.randint(0x02, 0x07)) # Shadow Blade vertical launch speed (default 04)
    shadow_blade_returns = random.randint(0, 3) # Little randomization to see if Shadow Blade will boomerang at all. Default is a 25% chance to act like Metal Blade
    if shadow_blade_returns:
        edit_nes_byte(GAME_PATH, 0x3D2FC, random.randint(0x0A, 0x28)) # Shadow Blade range, i.e. how long it travels before boomeranging. Setting it high enough causes it to act like Metal Blade (default 14)
    else:
        edit_nes_byte(GAME_PATH, 0x3D2FC, 0xFF) # 0xFF is more than enough range for the blade to never boomerang


def scramble_enemy_weakness_tables():
# Scrambles the amount of damage that each special weapon does to the enemies in the game. The buster's table is not altered in this.
    for i in range(0x14210, 0x14A10):
        if i > 0x14610 and i < 0x14710: # This is specifically for Top Spin; in the base game it either kills a normal enemy in one hit or is completely ineffective, so we will preserve the idea here
            edit_nes_byte(GAME_PATH, i, random.choice([0x00, 0x0A]))
        else:
            edit_nes_byte(GAME_PATH, i, random.choice([0x00, 0x00, 0x01, 0x01, 0x02, 0x02, 0x06, 0x0A]))


def scramble_boss_behaviors():
# Scrambles the AI for the bosses in the game.
    # Needle Man
    edit_nes_byte(GAME_PATH, 0x88A6, random.randint(0x02, 0x06)) # Speed of Needle Man's needles (default 04)
    edit_nes_byte(GAME_PATH, 0xC0C9, random.randint(0x01, 0x02)) # Related to number of needles are shot per round? (default 01)
    edit_nes_byte(GAME_PATH, 0xC0F9, random.randint(0x0A, 0x16)) # This value governs how Needle Man moves in the air. The lower the value, the longer he stays in the air and shoots needles (default 10)
    edit_nes_byte(GAME_PATH, 0xC19F, random.randint(0x01, 0x02)) # Related to jump height (default 01)
    edit_nes_byte(GAME_PATH, 0xC1B0, random.randint(0x04, 0x07)) # Related to jump height (default 06)
    edit_nes_byte(GAME_PATH, 0xC1B1, random.randint(0x07, 0x0A)) # Related to jump height (default 09)
    edit_nes_byte(GAME_PATH, 0xC1B8, random.randint(0x05, 0x07)) # Related to jump height (default 06)
    edit_nes_byte(GAME_PATH, 0xC1E2, random.randint(0x01, 0x03)) # Related to Needle Man's horizontal jump speed (default 02)
    edit_nes_byte(GAME_PATH, 0xC1E6, random.randint(0x01, 0x05)) # Related to Needle Man's horizontal jump speed (default 03)
    edit_nes_byte(GAME_PATH, 0xC1E7, random.randint(0x01, 0x03)) # Related to Needle Man's horizontal jump speed (default 02)

    # Magnet Man
    edit_nes_byte(GAME_PATH, 0xC2D1, random.randint(0x03, 0x05)) # Delay time between each jump (default 04)
    edit_nes_byte(GAME_PATH, 0xC30F, random.randint(0xA0, 0xF0)) # Timer for Magnet Man's pulling phase (default F0)
    edit_nes_byte(GAME_PATH, 0xC34C, random.randint(0x02, 0x0A)) # Delay time between Magnet Missiles being fired (default 06)
    edit_nes_byte(GAME_PATH, 0xC366, random.randint(0x01, 0x06)) # Number of Magnet Missiles used before falling back to the ground (default 03)
    edit_nes_byte(GAME_PATH, 0xC381, random.randint(0x04, 0x08)) # Gravity after firing Magnet Missile (default 06)
    edit_nes_byte(GAME_PATH, 0xC42C, random.randint(0x02, 0x06)) # First jump height (default 04)
    edit_nes_byte(GAME_PATH, 0xC42D, random.randint(0x04, 0x08)) # Second jump height (default 06)
    edit_nes_byte(GAME_PATH, 0xC42F, random.randint(0xA3, 0xC8)) # Horizontal distance Magnet Man travels with each jump? (default B3)
    edit_nes_byte(GAME_PATH, 0xC432, random.randint(0x00, 0x02)) # Also related to horizontal jumping distance? (default 01)
    edit_nes_byte(GAME_PATH, 0xC433, random.randint(0x01, 0x04)) # Also related to horizontal jumping distance? (default 02)
    edit_nes_byte(GAME_PATH, 0xC469, random.randint(0x02, 0x06)) # Speed of Magnet Missile (default 04)

    # Gemini Man
    edit_nes_byte(GAME_PATH, 0xA827, random.randint(0x01, 0x05)) # Speed of Gemini Laser after bouncing off the wall (default 03)
    edit_nes_byte(GAME_PATH, 0xE70F, random.randint(0x07, 0x15)) # Battle phase changes at one below this value (default 0F)
    # edit_nes_byte(GAME_PATH, 0xE7B8, 0xA7) # X position that Gemini Man and his clone stop to jump at; don't mess with this one (default A7)
    edit_nes_byte(GAME_PATH, 0xE8F5, random.randint(0x02, 0x06)) # Phase 1 bullet speed (default 04)
    edit_nes_byte(GAME_PATH, 0xE9A0, random.randint(0x21, 0x38)) # Related to clone movement speed (default 2D)
    edit_nes_byte(GAME_PATH, 0xE9A5, random.randint(0x01, 0x05)) # Related to clone movement speed (default 03)
    edit_nes_byte(GAME_PATH, 0xE785, random.randint(0x49, 0x4F)) # Related to phase 2 Gemini Man speed (default 4C)
    edit_nes_byte(GAME_PATH, 0xE78A, random.randint(0x01, 0x02)) # Related to phase 2 Gemini Man speed (default 01)
    edit_nes_byte(GAME_PATH, 0xE85B, random.randint(0x03, 0x07)) # Jumping height (default 05)
    edit_nes_byte(GAME_PATH, 0xE951, random.randint(0x01, 0x05)) # Speed of Gemini Laser when shot initially (default 03)

    # Hard Man
    edit_nes_byte(GAME_PATH, 0xE0B5, random.randint(0x06, 0x0A)) # Jumping height (default 08)
    edit_nes_byte(GAME_PATH, 0xE0BD, random.randint(0x10, 0x2D)) # Time until jumping after shooting Hard Knuckle (default 1E)
    edit_nes_byte(GAME_PATH, 0xE133, random.randint(0x03, 0x07)) # Hard Man's gravity after jumping (default 05)
    # edit_nes_byte(GAME_PATH, 0xE138, 0xBD) # Speed related variable; don't mess with this one (default BD)
    edit_nes_byte(GAME_PATH, 0xE195, random.randint(0x01, 0x07)) # Jumping height after tackle attack (default 04)
    # edit_nes_byte(GAME_PATH, 0xE19D, 0x01) # Shaking intensity during tackle attack (do not set higher than 02) (default 01)
    edit_nes_byte(GAME_PATH, 0xE1C5, random.randint(0x08, 0x18)) # Time until shooting Hard Knuckle after recovering from tackle (default 10)
    # edit_nes_byte(GAME_PATH, 0xE1F5, 0x3D) # Length of time the ground shakes for during Hard Man's tackle; this setting can sometimes cause the ground to be disjointed if changed (still trying to figure this out) (default 3D)
    edit_nes_byte(GAME_PATH, 0xE237, random.randint(0x02, 0x04)) # Hard Man horizontal speed during jump? (default 03)
    edit_nes_byte(GAME_PATH, 0xE238, random.randint(0x02, 0x04)) # Hard Man horizontal speed during jump? (default 03)
    edit_nes_byte(GAME_PATH, 0xE2AA, random.randint(0x07, 0x09)) # Influences the height of Hard Knuckle after it reverses direction (default 08)
    edit_nes_byte(GAME_PATH, 0xE31D, random.randint(0x02, 0x05)) # Speed of the Hard Knuckle, perhaps the first one? (default 03)
    edit_nes_byte(GAME_PATH, 0xE31F, random.randint(0x02, 0x05)) # Another speed variable, perhaps the second Hard Knuckle? (default 03)

    # Top Man
    edit_nes_byte(GAME_PATH, 0xC57D, random.randint(0x28, 0x88)) # Time until Top Man starts spinning after shooting (default 78)
    edit_nes_byte(GAME_PATH, 0xC593, random.randint(0xC0, 0xF0)) # How far Top Man goes to the right before stopping (default D0)
    edit_nes_byte(GAME_PATH, 0xC5A0, random.randint(0x10, 0x40)) # How far Top Man goes to the left before stopping (default 30)
    edit_nes_byte(GAME_PATH, 0xC5EF, random.randint(0x0A, 0x12)) # Where tops originate from (default 0E)
    edit_nes_byte(GAME_PATH, 0xC602, random.randint(0x02, 0x07)) # Speed of thrown tops (default 04)


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
    # Mega Man 3 bosses all have 2 weaknesses so let's preserve the chance for that in the randomization
    weaknesses_1 = [0, 1, 2, 3, 4, 5, 6, 7]
    random.shuffle(weaknesses_1)
    weaknesses_2 = [0, 1, 2, 3, 4, 5, 6, 7]
    random.shuffle(weaknesses_2)

    # These loops set immunities, weaknesses and semi-weaknesses across the Robot Master damage tables
    for i in range(len(effectiveness)):
        for j in range(i):
            effectiveness[i][j] = random.choice([0x00, 0x00, 0x01, 0x01, 0x01, 0x02])
        effectiveness[i][weaknesses_1[i]] = 0x04
        effectiveness[i][weaknesses_2[i]] = random.choice([0x04, 0x04, 0x04, 0x05, 0x07, 0x07, 0x07, 0x07])
    
    # Repeat this same process for the Doc Robots
    doc_effectiveness = [
    [0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01],
    [0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01],
    [0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01],
    [0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01],
    [0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01],
    [0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01],
    [0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01],
    [0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01]]
    # Mega Man 3 bosses all have 2 weaknesses so let's preserve the chance for that in the randomization
    doc_weaknesses_1 = [0, 1, 2, 3, 4, 5, 6, 7]
    random.shuffle(doc_weaknesses_1)
    doc_weaknesses_2 = [0, 1, 2, 3, 4, 5, 6, 7]
    random.shuffle(doc_weaknesses_2)
    
    # These loops set immunities, weaknesses and semi-weaknesses across the Robot Master damage tables
    for i in range(len(doc_effectiveness)):
        for j in range(i):
            doc_effectiveness[i][j] = random.choice([0x00, 0x00, 0x01, 0x01, 0x01, 0x02])
        doc_effectiveness[i][doc_weaknesses_1[i]] = 0x04
        doc_effectiveness[i][doc_weaknesses_2[i]] = random.choice([0x04, 0x04, 0x04, 0x04, 0x04, 0x04, 0x07, 0x07]) # Doc Robot weaknesses have a slightly different distribution that I've replicated here
    
    # Loop through and assign all weaknesses to Robot Masters and Doc Robots
    counter = 0
    for i in range(0x14100, 0x14A00, 0x100):
        if i == 0x14100: # This first segment is for the Mega Buster, which we want to make do only 1 or 2 damage to bosses. No boss should be immune to the Mega Buster
            # Doc Robots (yes these are first in memory interestingly)
            edit_nes_byte(GAME_PATH, i + 0xB0, random.choice([0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x02, 0x02])) # VS Doc Flash Man
            edit_nes_byte(GAME_PATH, i + 0xB1, random.choice([0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x02, 0x02])) # VS Doc Wood Man
            edit_nes_byte(GAME_PATH, i + 0xB2, random.choice([0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x02, 0x02])) # VS Doc Crash Man
            edit_nes_byte(GAME_PATH, i + 0xB3, random.choice([0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x02, 0x02])) # VS Doc Metal Man
            edit_nes_byte(GAME_PATH, i + 0xC0, random.choice([0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x02, 0x02])) # VS Doc Bubble Man
            edit_nes_byte(GAME_PATH, i + 0xC1, random.choice([0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x02, 0x02])) # VS Doc Heat Man
            edit_nes_byte(GAME_PATH, i + 0xC2, random.choice([0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x02, 0x02])) # VS Doc Quick Man
            edit_nes_byte(GAME_PATH, i + 0xC3, random.choice([0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x02, 0x02])) # VS Doc Air Man

            # Robot Masters
            edit_nes_byte(GAME_PATH, i + 0xD0, random.choice([0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x02, 0x02])) # VS Needle Man
            edit_nes_byte(GAME_PATH, i + 0xD7, random.choice([0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x02, 0x02])) # Also VS Needle Man but specifically for the head hammer extended state
            edit_nes_byte(GAME_PATH, i + 0xD1, random.choice([0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x02, 0x02])) # VS Magnet Man
            edit_nes_byte(GAME_PATH, i + 0xD2, random.choice([0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x02, 0x02])) # VS Top Man
            edit_nes_byte(GAME_PATH, i + 0xD3, random.choice([0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x02, 0x02])) # VS Shadow Man
            edit_nes_byte(GAME_PATH, i + 0xE0, random.choice([0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x02, 0x02])) # VS Hard Man
            edit_nes_byte(GAME_PATH, i + 0xE2, random.choice([0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x02, 0x02])) # VS Spark Man
            edit_nes_byte(GAME_PATH, i + 0xE4, random.choice([0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x02, 0x02])) # VS Snake Man
            edit_nes_byte(GAME_PATH, i + 0xE6, random.choice([0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x02, 0x02])) # VS Gemini Man
            edit_nes_byte(GAME_PATH, i + 0xE7, random.choice([0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x02, 0x02])) # VS Gemini Man's clone (yes it has a separate damage table for some reason)
        else:
            # Doc Robots (yes these are first in memory interestingly)
            edit_nes_byte(GAME_PATH, i + 0xB0, doc_effectiveness[counter][0]) # VS Doc Flash Man
            edit_nes_byte(GAME_PATH, i + 0xB1, doc_effectiveness[counter][1]) # VS Doc Wood Man
            edit_nes_byte(GAME_PATH, i + 0xB2, doc_effectiveness[counter][2]) # VS Doc Crash Man
            edit_nes_byte(GAME_PATH, i + 0xB3, doc_effectiveness[counter][3]) # VS Doc Metal Man
            edit_nes_byte(GAME_PATH, i + 0xC0, doc_effectiveness[counter][4]) # VS Doc Bubble Man
            edit_nes_byte(GAME_PATH, i + 0xC1, doc_effectiveness[counter][5]) # VS Doc Heat Man
            edit_nes_byte(GAME_PATH, i + 0xC2, doc_effectiveness[counter][6]) # VS Doc Quick Man
            edit_nes_byte(GAME_PATH, i + 0xC3, doc_effectiveness[counter][7]) # VS Doc Air Man

            # Robot Masters
            edit_nes_byte(GAME_PATH, i + 0xD0, effectiveness[counter][0]) # VS Needle Man
            edit_nes_byte(GAME_PATH, i + 0xD7, effectiveness[counter][0]) # Also VS Needle Man but specifically for the head hammer extended state
            edit_nes_byte(GAME_PATH, i + 0xD1, effectiveness[counter][1]) # VS Magnet Man
            edit_nes_byte(GAME_PATH, i + 0xD2, effectiveness[counter][2]) # VS Top Man
            edit_nes_byte(GAME_PATH, i + 0xD3, effectiveness[counter][3]) # VS Shadow Man
            edit_nes_byte(GAME_PATH, i + 0xE0, effectiveness[counter][4]) # VS Hard Man
            edit_nes_byte(GAME_PATH, i + 0xE2, effectiveness[counter][5]) # VS Spark Man
            edit_nes_byte(GAME_PATH, i + 0xE4, effectiveness[counter][6]) # VS Snake Man
            edit_nes_byte(GAME_PATH, i + 0xE6, effectiveness[counter][7]) # VS Gemini Man
            edit_nes_byte(GAME_PATH, i + 0xE7, effectiveness[counter][7]) # VS Gemini Man's clone (yes it has a separate damage table for some reason)
            counter += 1 


if __name__ == "__main__":
# Mix it all up!
    # Core randomizer features
    scramble_stage_order()
    scramble_title_screen_palette()
    scramble_weapon_palettes()
    scramble_robot_master_names()
    scramble_stage_select_palettes()
    scramble_stage_palettes()
    scramble_music()
    scramble_stage_entities()
    scramble_sprite_palettes()
    scramble_sprite_health()
    scramble_sprite_speed()
    scramble_weapon_energy_costs()
    scramble_weapon_behaviors()
    scramble_enemy_weakness_tables()
    scramble_boss_behaviors()
    scramble_boss_weakness_tables() # Make sure to scramble boss tables after enemy tables, otherwise the enemy scrambling will overwrite those memory values

    # Bonus stuff
    fix_scanline() # Disable if you want to preserve the annoying scanline issue on the stage select...?
    activate_burst_chaser() # Disable if not playing Burst Chaser mode