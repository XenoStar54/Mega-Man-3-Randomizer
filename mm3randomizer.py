import struct
import random
import math

# Change this seed for a specific generated ROM.
#random.seed(54)

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
    "tank", "tube", "pipe", "wire", "cord", "xeno", "chip", "disk", "gear", "tool",
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

# This name list is used to generate a new, globally accessible name for each robot master
list_new_names = [] # This just ensures that no name is generated twice
NEEDLE_NEW_NAME = random.choice(SIX_LETTER_NOUNS)
list_new_names.append(NEEDLE_NEW_NAME)
MAGNET_NEW_NAME = random.choice(SIX_LETTER_NOUNS)
while MAGNET_NEW_NAME in list_new_names: # If the chosen name is already in the list of names, reroll
    MAGNET_NEW_NAME = random.choice(SIX_LETTER_NOUNS)
list_new_names.append(MAGNET_NEW_NAME)
GEMINI_NEW_NAME = random.choice(SIX_LETTER_NOUNS)
while GEMINI_NEW_NAME in list_new_names: # If the chosen name is already in the list of names, reroll
    GEMINI_NEW_NAME = random.choice(SIX_LETTER_NOUNS)
list_new_names.append(GEMINI_NEW_NAME)
HARD_NEW_NAME = random.choice(FOUR_LETTER_NOUNS)
list_new_names.append(HARD_NEW_NAME)
TOP_NEW_NAME = random.choice(THREE_LETTER_NOUNS)
list_new_names.append(TOP_NEW_NAME)
SNAKE_NEW_NAME = random.choice(FIVE_LETTER_NOUNS)
while SNAKE_NEW_NAME in list_new_names: # If the chosen name is already in the list of names, reroll
    SNAKE_NEW_NAME = random.choice(FIVE_LETTER_NOUNS)
list_new_names.append(SNAKE_NEW_NAME)
SPARK_NEW_NAME = random.choice(FIVE_LETTER_NOUNS)
while SPARK_NEW_NAME in list_new_names: # If the chosen name is already in the list of names, reroll
    SPARK_NEW_NAME = random.choice(FIVE_LETTER_NOUNS)
list_new_names.append(SPARK_NEW_NAME)
SHADOW_NEW_NAME = random.choice(SIX_LETTER_NOUNS)
while SHADOW_NEW_NAME in list_new_names: # If the chosen name is already in the list of names, reroll
    SHADOW_NEW_NAME = random.choice(SIX_LETTER_NOUNS)
list_new_names.append(SHADOW_NEW_NAME)

# These lists provide new words for randomizing the weapon names.
FOUR_LETTER_WEAPONS = [
    "spin", "slap", "ball", "beam", "bomb", "shot", "ring", "kick", "hold", "bolt", "mine", "hole", "dash", "club", "clap"
]
FIVE_LETTER_WEAPONS = [
    "blade", "laser", "shock", "blast", "slash", "smack", "storm", "spear", "flash", "crush", "flush", "blast", "sword", "punch"
]
SIX_LETTER_WEAPONS = [
    "cannon", "attack", "cutter", "shield", "strike", "string", "burner", "digger", "mortar", "rocket", "bullet", "katana"
]
SEVEN_LETTER_WEAPONS = [
    "missile", "knuckle", "stopper", "slasher", "shooter", "barrier", "crusher", "blaster", "striker", "grenade", "bazooka"
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
    # [0x14] Jamacy Generator (do not use)
    [0x15, [0x06, 0x17, 0x1C, 0x20]], # Jamacy (Alternate climbing variant? State for climbing variant?)
    [0x16, [0x09, 0x19]], # Magnet force (left)
    # [0x17] No clue what this is (do not use)
    [0x18, [0x04, 0x14, 0x1A, 0x1C, 0x1D, 0x20, 0x2F, 0x39]], # Nitron
    # [0x19] No clue what this is (do not use)
    [0x1A, [0x03, 0x33, 0x38]], # Gyoraibo (Normal Gemini variant?)
    [0x1B, [0x2E]], # Hari Hari
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
RANDOMIZED_ROBOT_MASTERS = [
    [0x47, 0x25], # Needle Man  
    [0x48, 0x23], # Magnet Man
    [0x49, 0x27], # Gemini Man
    [0x4A, 0x24], # Hard Man
    [0x4B, 0x2A], # Top Man
    [0x4C, 0x26], # Snake Man
    [0x4D, 0x28], # Spark Man
    [0x4E, 0x29]  # Shadow Man
    ]
random.shuffle(RANDOMIZED_ROBOT_MASTERS)

# This globally accessible list randomizes the locations of the Doc Robots. The list items are the boss entity ID and graphics set.
RANDOMIZED_DOC_ROBOTS = [
    [0x68, 0x0F], # Doc Flash
    [0x69, 0x10], # Doc Bubble
    [0x6A, 0x0F], # Doc Quick
    [0x6B, 0x10], # Doc Wood
    [0x6C, 0x0F], # Doc Crash
    [0x6D, 0x10], # Doc Air
    [0x6E, 0x0F], # Doc Metal
    [0x6F, 0x10]  # Doc Heat
]
random.shuffle(RANDOMIZED_DOC_ROBOTS)

# Special weapons are assigned during the weapon bar cutscene after a boss is defeated. The first two values are programmed in pairs of position and the menu page (00 or 06) the weapon is located on. The second two values are the primary and secondary colors for the respective weapon.
WEAPON_POSITIONS = [
    [0x02, 0x00, random.randint(0x20, 0x2C), random.randint(0x10, 0x1D), NEEDLE_NEW_NAME], # Needle Cannon
    [0x04, 0x00, random.randint(0x20, 0x2C), random.randint(0x10, 0x1D), MAGNET_NEW_NAME], # Magnet Missile
    [0x01, 0x00, random.randint(0x20, 0x2C), random.randint(0x10, 0x1D), GEMINI_NEW_NAME], # Gemini Laser
    [0x03, 0x00, random.randint(0x20, 0x2C), random.randint(0x10, 0x1D), HARD_NEW_NAME],   # Hard Knuckle
    [0x05, 0x00, random.randint(0x20, 0x2C), random.randint(0x10, 0x1D), TOP_NEW_NAME],    # Top Spin
    [0x00, 0x06, random.randint(0x20, 0x2C), random.randint(0x10, 0x1D), SNAKE_NEW_NAME],  # Search Snake
    [0x02, 0x06, random.randint(0x20, 0x2C), random.randint(0x10, 0x1D), SPARK_NEW_NAME],  # Spark Shock
    [0x04, 0x06, random.randint(0x20, 0x2C), random.randint(0x10, 0x1D), SHADOW_NEW_NAME]  # Shadow Blade
]
# This list contains the weapon colors in the order they're actually placed on the weapon get menu. This is used for Mega Man's color during actual gameplay, as opposed to the previous list which is primarily for randomizing weapon locations and the weapon get screen.
ORDERED_WEAPONS = [
    [WEAPON_POSITIONS[2][2], WEAPON_POSITIONS[2][3]], # Gemini Laser
    [WEAPON_POSITIONS[0][2], WEAPON_POSITIONS[0][3]], # Needle Cannon
    [WEAPON_POSITIONS[3][2], WEAPON_POSITIONS[3][3]], # Hard Knuckle
    [WEAPON_POSITIONS[1][2], WEAPON_POSITIONS[1][3]], # Magnet Missile
    [WEAPON_POSITIONS[4][2], WEAPON_POSITIONS[4][3]], # Top Spin
    [WEAPON_POSITIONS[5][2], WEAPON_POSITIONS[5][3]], # Search Snake
    [WEAPON_POSITIONS[6][2], WEAPON_POSITIONS[6][3]], # Spark Shock
    [WEAPON_POSITIONS[7][2], WEAPON_POSITIONS[7][3]], # Shadow Blade
]
random.shuffle(WEAPON_POSITIONS)


def edit_nes_byte(file_path, offset, new_value):
# A helper function that edits the value of the byte at the specified address in the ROM.

    with open(file_path, "rb+") as f:
        f.seek(offset)
        # Write one byte
        f.write(struct.pack('B', new_value))


def read_nes_byte(file_path, offset):
# A helper function that returns the value of the byte at the specified address in the ROM.

    with open(file_path, "rb+") as f:
        f.seek(offset)
        value = f.read(1)
        return value.hex()


def scramble_title_screen_palette():
# This scrambles the palette of the title screen.

    edit_nes_byte(GAME_PATH, 0x31C15, random.choice(LIGHT_COLORS)) # Light blue letter highlights
    edit_nes_byte(GAME_PATH, 0x31C18, random.choice(LIGHT_COLORS)) # Light blue letter highlights
    edit_nes_byte(GAME_PATH, 0x31C1A, random.choice(DARK_COLORS_NB)) # Dark green letter shadows
    edit_nes_byte(GAME_PATH, 0x31C1C, random.choice(LIGHT_COLORS)) # Bright red lettering
    edit_nes_byte(GAME_PATH, 0x31C1E, random.choice(DARK_COLORS_NB)) # Dark red lettering
    edit_nes_byte(GAME_PATH, 0x31C28, random.choice(LIGHT_COLORS)) # Selection cursor


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
    # Palette changes after Doc Robot stages appear for some reason
    edit_nes_byte(GAME_PATH, 0x31D48, stage_select_primary)
    edit_nes_byte(GAME_PATH, 0x31D49, stage_select_secondary)

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


def convert_string_to_mm3_text(text):
# A helper function that converts characters to the character set used for typed text in Mega Man 3.

    build_string = []
    for char in text:
        build_string.append(ord(char.lower()) - 97 + 0x0A)
    return build_string


def scramble_robot_master_names():
# Purely cosmetic, but changes the Robot Master names.

    # This section is used somewhere but unsure where
    for i in range(0x61F1, 0x61F7): # "Needle Man"
        edit_nes_byte(GAME_PATH, i, convert_string_to_mm3_text(NEEDLE_NEW_NAME)[i - 0x61F1])
    for i in range(0x61FB, 0x6201): # "Magnet Man"
        edit_nes_byte(GAME_PATH, i, convert_string_to_mm3_text(MAGNET_NEW_NAME)[i - 0x61FB])
    for i in range(0x6205, 0x620B): # "Gemini Man"
        edit_nes_byte(GAME_PATH, i, convert_string_to_mm3_text(GEMINI_NEW_NAME)[i - 0x6205])
    for i in range(0x620F, 0x6213): # "Hard Man"
        edit_nes_byte(GAME_PATH, i, convert_string_to_mm3_text(HARD_NEW_NAME)[i - 0x620F])
    for i in range(0x6219, 0x621C): # "Top Man"
        edit_nes_byte(GAME_PATH, i, convert_string_to_mm3_text(TOP_NEW_NAME)[i - 0x6219])
    for i in range(0x6223, 0x6228): # "Snake Man"
        edit_nes_byte(GAME_PATH, i, convert_string_to_mm3_text(SNAKE_NEW_NAME)[i - 0x6223])
    for i in range(0x622D, 0x6232): # "Spark Man"
        edit_nes_byte(GAME_PATH, i, convert_string_to_mm3_text(SPARK_NEW_NAME)[i - 0x622D])
    for i in range(0x6237, 0x623D): # "Shadow Man"   
        edit_nes_byte(GAME_PATH, i, convert_string_to_mm3_text(SHADOW_NEW_NAME)[i - 0x6237])

    # Actual stage select stuff
    for i in range(0x639E, 0x63A4): # "Needle Man"
        edit_nes_byte(GAME_PATH, i, convert_string_to_mm3_text(NEEDLE_NEW_NAME)[i - 0x639E])
    for i in range(0x63F0, 0x63F6): # "Magnet Man"
        edit_nes_byte(GAME_PATH, i, convert_string_to_mm3_text(MAGNET_NEW_NAME)[i - 0x63F0])
    for i in range(0x63E7, 0x63ED): # "Gemini Man"
        edit_nes_byte(GAME_PATH, i, convert_string_to_mm3_text(GEMINI_NEW_NAME)[i - 0x63E7])
    for i in range(0x63C3, 0x63C7): # "Hard Man"
        edit_nes_byte(GAME_PATH, i, convert_string_to_mm3_text(HARD_NEW_NAME)[i - 0x63C3])
    for i in range(0x63CC, 0x63CF): # "Top Man"
        edit_nes_byte(GAME_PATH, i, convert_string_to_mm3_text(TOP_NEW_NAME)[i - 0x63CC])
    for i in range(0x6395, 0x639A): # "Snake Man"
        edit_nes_byte(GAME_PATH, i, convert_string_to_mm3_text(SNAKE_NEW_NAME)[i - 0x6395])
    for i in range(0x638C, 0x6391): # "Spark Man"
        edit_nes_byte(GAME_PATH, i, convert_string_to_mm3_text(SPARK_NEW_NAME)[i - 0x638C])
    for i in range(0x63F9, 0x63FF): # "Shadow Man"   
        edit_nes_byte(GAME_PATH, i, convert_string_to_mm3_text(SHADOW_NEW_NAME)[i - 0x63F9])

    # Generate new names for weapons
    needle_weapon_name = random.choice(SIX_LETTER_WEAPONS)
    magnet_weapon_name = random.choice(SEVEN_LETTER_WEAPONS)
    gemini_weapon_name = random.choice(FIVE_LETTER_WEAPONS)
    hard_weapon_name = random.choice(SEVEN_LETTER_WEAPONS)
    top_weapon_name = random.choice(FOUR_LETTER_WEAPONS)
    snake_weapon_name = random.choice(SIX_LETTER_WEAPONS)
    spark_weapon_name = random.choice(FIVE_LETTER_WEAPONS)
    shadow_weapon_name = random.choice(FIVE_LETTER_WEAPONS)

    # Replace names on weapon get screen
    for i in range(0x6429, 0x642F): # "Needle"
        edit_nes_byte(GAME_PATH, i, convert_string_to_mm3_text(NEEDLE_NEW_NAME)[i - 0x6429])
    for i in range(0x6430, 0x6436): # "Cannon"
        edit_nes_byte(GAME_PATH, i, convert_string_to_mm3_text(needle_weapon_name)[i - 0x6430])
    for i in range(0x644C, 0x6452): # "Magnet"
        edit_nes_byte(GAME_PATH, i, convert_string_to_mm3_text(MAGNET_NEW_NAME)[i - 0x644C])
    for i in range(0x6453, 0x645A): # "Missile"
        edit_nes_byte(GAME_PATH, i, convert_string_to_mm3_text(magnet_weapon_name)[i - 0x6453])
    for i in range(0x645E, 0x6464): # "Gemini"
        edit_nes_byte(GAME_PATH, i, convert_string_to_mm3_text(GEMINI_NEW_NAME)[i - 0x645E])
    for i in range(0x6465, 0x646A): # "Laser"
        edit_nes_byte(GAME_PATH, i, convert_string_to_mm3_text(gemini_weapon_name)[i - 0x6465])
    for i in range(0x646E, 0x6472): # "Hard"
        edit_nes_byte(GAME_PATH, i, convert_string_to_mm3_text(HARD_NEW_NAME)[i - 0x646E])
    for i in range(0x6473, 0x647A): # "Knuckle"
        edit_nes_byte(GAME_PATH, i, convert_string_to_mm3_text(hard_weapon_name)[i - 0x6473])
    for i in range(0x647E, 0x6481): # "Top"
        edit_nes_byte(GAME_PATH, i, convert_string_to_mm3_text(TOP_NEW_NAME)[i - 0x647E])
    for i in range(0x6482, 0x6486): # "Spin"
        edit_nes_byte(GAME_PATH, i, convert_string_to_mm3_text(top_weapon_name)[i - 0x6482])
    for i in range(0x648A, 0x6490): # "Search"
        edit_nes_byte(GAME_PATH, i, convert_string_to_mm3_text(snake_weapon_name)[i - 0x648A])
    for i in range(0x6491, 0x6496): # "Snake"
        edit_nes_byte(GAME_PATH, i, convert_string_to_mm3_text(SNAKE_NEW_NAME)[i - 0x6491])
    for i in range(0x649A, 0x649F): # "Spark"
        edit_nes_byte(GAME_PATH, i, convert_string_to_mm3_text(SPARK_NEW_NAME)[i - 0x649A])
    for i in range(0x64A0, 0x64A5): # "Shock"
        edit_nes_byte(GAME_PATH, i, convert_string_to_mm3_text(spark_weapon_name)[i - 0x64A0])
    for i in range(0x64A9, 0x64AF): # "Shadow"   
        edit_nes_byte(GAME_PATH, i, convert_string_to_mm3_text(SHADOW_NEW_NAME)[i - 0x64A9])
    for i in range(0x64B0, 0x64B5): # "Blade"
        edit_nes_byte(GAME_PATH, i, convert_string_to_mm3_text(shadow_weapon_name)[i - 0x64B0])

    # Weapon menu weapon initials
    # edit_nes_byte(GAME_PATH, 0x45E8) "P"
    # edit_nes_byte(GAME_PATH, 0x45F4) " "
    edit_nes_byte(GAME_PATH, 0x45E9, convert_string_to_mm3_text(GEMINI_NEW_NAME)[0]) # "G"
    edit_nes_byte(GAME_PATH, 0x45F5, convert_string_to_mm3_text(GEMINI_NEW_NAME)[1]) # "E"
    edit_nes_byte(GAME_PATH, 0x45EA, convert_string_to_mm3_text(NEEDLE_NEW_NAME)[0]) # "N"
    edit_nes_byte(GAME_PATH, 0x45F6, convert_string_to_mm3_text(NEEDLE_NEW_NAME)[1]) # "E"
    edit_nes_byte(GAME_PATH, 0x45EB, convert_string_to_mm3_text(MAGNET_NEW_NAME)[0]) # "M"
    edit_nes_byte(GAME_PATH, 0x45F7, convert_string_to_mm3_text(MAGNET_NEW_NAME)[1]) # "A"
    edit_nes_byte(GAME_PATH, 0x45EC, convert_string_to_mm3_text(HARD_NEW_NAME)[0]) # "H"
    edit_nes_byte(GAME_PATH, 0x45F8, convert_string_to_mm3_text(HARD_NEW_NAME)[1]) # "A"
    edit_nes_byte(GAME_PATH, 0x45ED, convert_string_to_mm3_text(TOP_NEW_NAME)[0]) # "T"
    edit_nes_byte(GAME_PATH, 0x45F9, convert_string_to_mm3_text(TOP_NEW_NAME)[1]) # "O"
    edit_nes_byte(GAME_PATH, 0x45EE, convert_string_to_mm3_text(SNAKE_NEW_NAME)[0]) # "S"
    edit_nes_byte(GAME_PATH, 0x45FA, convert_string_to_mm3_text(SNAKE_NEW_NAME)[1]) # "N"
    # edit_nes_byte(GAME_PATH, 0x45EF,) "R"
    # edit_nes_byte(GAME_PATH, 0x45FB,) "C"
    edit_nes_byte(GAME_PATH, 0x45F0, convert_string_to_mm3_text(SPARK_NEW_NAME)[0]) # "S"
    edit_nes_byte(GAME_PATH, 0x45FC, convert_string_to_mm3_text(SPARK_NEW_NAME)[1]) # "P"
    # edit_nes_byte(GAME_PATH, 0x45F1,) "R"
    # edit_nes_byte(GAME_PATH, 0x45FD,) "M"
    edit_nes_byte(GAME_PATH, 0x45F2, convert_string_to_mm3_text(SHADOW_NEW_NAME)[0]) # "S"
    edit_nes_byte(GAME_PATH, 0x45FE, convert_string_to_mm3_text(SHADOW_NEW_NAME)[1]) # "H"
    # edit_nes_byte(GAME_PATH, 0x45F3,) "R"
    # edit_nes_byte(GAME_PATH, 0x45FF,) "J"


def randomize_needle_man_graphics():
# Randomizes the graphics for Needle Man's stage.

    for i in range(0xA92, 0xAB6):
        if i not in [0xAA2, 0xAA3, 0xAA4, 0xAA5]:
            if int(read_nes_byte(GAME_PATH, i), 16) not in [0x0F, 0x20, 0x30]:
                if(int(read_nes_byte(GAME_PATH, i), 16) in LIGHT_COLORS):
                    edit_nes_byte(GAME_PATH, i, random.choice(LIGHT_COLORS_NW))
                else:
                    edit_nes_byte(GAME_PATH, i, random.choice(DARK_COLORS_NB))

    # Shading fix for the background walls
    needle_background = random.randint(0x10, 0x1C)
    edit_nes_byte(GAME_PATH, 0xA9C, needle_background)
    edit_nes_byte(GAME_PATH, 0xA9D, needle_background - 0x10)

    # Some fixes for bizarre color shenanigans with ladders and backgrounds
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

    # Fix block colors; block animations begin at 0x125BF
    color_1 = int(read_nes_byte(GAME_PATH, 0x125BF), 16) # Light blue highlight
    color_2 = int(read_nes_byte(GAME_PATH, 0x125C0), 16) # Blue 
    color_3 = int(read_nes_byte(GAME_PATH, 0x125C3), 16) # Red
    color_4 = int(read_nes_byte(GAME_PATH, 0x125C6), 16) # Yellow

    # Randomize some new block colors, ensure no colors are repeated for maximum graphical variety
    new_color_1 = random.randint(0x31, 0x3C)
    new_color_2 = random.randint(0x11, 0x1C)
    new_color_3 = random.randint(0x11, 0x1C)
    while new_color_3 == new_color_2:
        new_color_3 = random.randint(0x11, 0x1C)
    new_color_4 = random.randint(0x11, 0x1C)
    while new_color_4 == new_color_2 or new_color_4 == new_color_3:
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

    # Flashing stringy things in the background of the cave segments; do this after the block colors to prevent overwrites
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

    # Fix for the ground changing color after Proto Man cutscene
    edit_nes_byte(GAME_PATH, 0x4ADB, int(read_nes_byte(GAME_PATH, 0x4A9F), 16))
    edit_nes_byte(GAME_PATH, 0x4ADC, int(read_nes_byte(GAME_PATH, 0x4AA0), 16))
    edit_nes_byte(GAME_PATH, 0x4ADD, int(read_nes_byte(GAME_PATH, 0x4AA1), 16))

    # Restrict background of the boss fight to avoid ugly backgrounds
    edit_nes_byte(GAME_PATH, 0x4AC8, random.randint(0x00, 0x0C))
    edit_nes_byte(GAME_PATH, 0x4AC9, random.randint(0x00, 0x0C))
    edit_nes_byte(GAME_PATH, 0x4AC7, random.randint(0x20, 0x2C))


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

    # Darken cave background colors
    edit_nes_byte(GAME_PATH, 0x6A97, random.randint(0x01, 0x0C))
    edit_nes_byte(GAME_PATH, 0x6A98, random.randint(0x01, 0x0C))
    edit_nes_byte(GAME_PATH, 0x6A99, random.randint(0x01, 0x0C))


def randomize_top_man_graphics():
# Randomizes the graphics for Top Man's stage.

    for i in range(0x8A92, 0x8AC6):
        if i not in [0x8AA2, 0x8AA3, 0x8AA4, 0x8AA5, 0x8AB6, 0x8AB7, 0x8AB8, 0x8AB9]: # These specific values are for tile animation and should not be messed with
            if int(read_nes_byte(GAME_PATH, i), 16) not in [0x0F, 0x20, 0x30]:
                if(int(read_nes_byte(GAME_PATH, i), 16) in LIGHT_COLORS):
                    edit_nes_byte(GAME_PATH, i, random.choice(LIGHT_COLORS_NW))
                else:
                    edit_nes_byte(GAME_PATH, i, random.choice(DARK_COLORS_NB))

    # This ensures that the background of the panels and pipes is the same color as the stage background.
    edit_nes_byte(GAME_PATH, 0x8AB5, int(read_nes_byte(GAME_PATH, 0x8AA9), 16))

    # Apply a gradient to make the leaves look coherent
    top_leaves = random.choice(DARK_COLORS_NB)
    edit_nes_byte(GAME_PATH, 0x8AAC, top_leaves)
    edit_nes_byte(GAME_PATH, 0x8AAD, top_leaves + 0x10)

    # Ensure that the leaves under the glass match the leaves outside of the glass
    edit_nes_byte(GAME_PATH, 0x8AA8, int(read_nes_byte(GAME_PATH, 0x8AAC), 16))

    # Animated tiles
    edit_nes_byte(GAME_PATH, 0x125F2, int(read_nes_byte(GAME_PATH, 0x8AB3), 16))
    edit_nes_byte(GAME_PATH, 0x125F3, random.choice(LIGHT_COLORS_NW))
    edit_nes_byte(GAME_PATH, 0x125F4, int(read_nes_byte(GAME_PATH, 0x8AA9), 16))
    edit_nes_byte(GAME_PATH, 0x125F5, int(read_nes_byte(GAME_PATH, 0x8AB3), 16))
    edit_nes_byte(GAME_PATH, 0x125F6, random.choice(LIGHT_COLORS_NW))
    edit_nes_byte(GAME_PATH, 0x125F7, int(read_nes_byte(GAME_PATH, 0x8AA9), 16))
    edit_nes_byte(GAME_PATH, 0x125F8, int(read_nes_byte(GAME_PATH, 0x8AB3), 16))
    edit_nes_byte(GAME_PATH, 0x125F9, random.choice(LIGHT_COLORS_NW))
    edit_nes_byte(GAME_PATH, 0x125FA, int(read_nes_byte(GAME_PATH, 0x8AA9), 16))
    edit_nes_byte(GAME_PATH, 0x12601, int(read_nes_byte(GAME_PATH, 0x8AB3), 16))
    edit_nes_byte(GAME_PATH, 0x12602, random.choice(LIGHT_COLORS_NW))
    edit_nes_byte(GAME_PATH, 0x12603, int(read_nes_byte(GAME_PATH, 0x8AA9), 16))

    # Top Man's stage changes palette very frequently. Here are some fixes for the constantly shifting colors
    edit_nes_byte(GAME_PATH, 0x8A95, int(read_nes_byte(GAME_PATH, 0x8AA9), 16))
    edit_nes_byte(GAME_PATH, 0x8A94, top_leaves)
    edit_nes_byte(GAME_PATH, 0x8A98, top_leaves)
    edit_nes_byte(GAME_PATH, 0x8A99, top_leaves + 0x10)
    edit_nes_byte(GAME_PATH, 0x8AA1, int(read_nes_byte(GAME_PATH, 0x8A9C), 16))
    edit_nes_byte(GAME_PATH, 0x8AB0, int(read_nes_byte(GAME_PATH, 0x8A9C), 16))
    edit_nes_byte(GAME_PATH, 0x8AB1, int(read_nes_byte(GAME_PATH, 0x8A9D), 16))
    edit_nes_byte(GAME_PATH, 0x8ABC, top_leaves)
    edit_nes_byte(GAME_PATH, 0x8ABD, int(read_nes_byte(GAME_PATH, 0x8AA9), 16))
    edit_nes_byte(GAME_PATH, 0x8AC0, top_leaves)
    edit_nes_byte(GAME_PATH, 0x8AC1, top_leaves + 0x10)
    edit_nes_byte(GAME_PATH, 0x8AC4, int(read_nes_byte(GAME_PATH, 0x8A9C), 16))
    edit_nes_byte(GAME_PATH, 0x8AC5, int(read_nes_byte(GAME_PATH, 0x8A9D), 16))


def randomize_snake_man_graphics():
# Randomizes the graphics for Snake Man's stage.

    for i in range(0xAA92, 0xAAA2):
        if int(read_nes_byte(GAME_PATH, i), 16) not in [0x0F, 0x20, 0x30]:
            if(int(read_nes_byte(GAME_PATH, i), 16) in LIGHT_COLORS):
                edit_nes_byte(GAME_PATH, i, random.choice(LIGHT_COLORS_NW))
            else:
                edit_nes_byte(GAME_PATH, i, random.choice(DARK_COLORS_NB))

    # Snake Man's stage benefits a lot from a gradient color scheme much like some other graphical assets
    snake_middle_color = random.randint(0x11, 0x1C)
    edit_nes_byte(GAME_PATH, 0xAA93, snake_middle_color + 0x10)
    edit_nes_byte(GAME_PATH, 0xAA94, snake_middle_color )
    edit_nes_byte(GAME_PATH, 0xAA95, snake_middle_color - 0x10)

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


def randomize_spark_man_graphics():
# Randomizes the graphics for Spark Man's stage.

    for i in range(0xCA92, 0xCAB6):
        if i not in [0xCAA2, 0xCAA3, 0xCAA4, 0xCAA5]: # These specific values are for tile animation and should not be messed with
            if int(read_nes_byte(GAME_PATH, i), 16) not in [0x0F, 0x20, 0x30]:
                if(int(read_nes_byte(GAME_PATH, i), 16) in LIGHT_COLORS):
                    edit_nes_byte(GAME_PATH, i, random.choice(LIGHT_COLORS_NW))
                else:
                    edit_nes_byte(GAME_PATH, i, random.choice(DARK_COLORS_NB))

    # Standardize the floor colors so that changing screens doesn't create weird jumbled color visuals
    edit_nes_byte(GAME_PATH, 0xCA9C, int(read_nes_byte(GAME_PATH, 0xCA98), 16))

    # This fixes the visuals on the junk block screen
    edit_nes_byte(GAME_PATH, 0xCAA8, int(read_nes_byte(GAME_PATH, 0xCA94), 16))
    edit_nes_byte(GAME_PATH, 0xCAA9, int(read_nes_byte(GAME_PATH, 0xCA95), 16))
    edit_nes_byte(GAME_PATH, 0xCAAC, int(read_nes_byte(GAME_PATH, 0xCA98), 16))
    edit_nes_byte(GAME_PATH, 0xCAB0, int(read_nes_byte(GAME_PATH, 0xCA98), 16))

    # Animated tiles. Pull values from existing randomized stuff so your eyes don't get fried and to avoid weird color changes on transition
    edit_nes_byte(GAME_PATH, 0x125DE, int(read_nes_byte(GAME_PATH, 0xCA98), 16))
    edit_nes_byte(GAME_PATH, 0x125DF, random.choice(LIGHT_COLORS_NW)) # Flashing floor light color
    edit_nes_byte(GAME_PATH, 0xCA99, int(read_nes_byte(GAME_PATH, 0x125DF), 16))
    edit_nes_byte(GAME_PATH, 0xCAAD, int(read_nes_byte(GAME_PATH, 0xCA99), 16))
    edit_nes_byte(GAME_PATH, 0x125E1, int(read_nes_byte(GAME_PATH, 0x125DE), 16)) 
    edit_nes_byte(GAME_PATH, 0x125E3, int(read_nes_byte(GAME_PATH, 0xCA9F), 16)) # Moving conveyors/gears/meters
    edit_nes_byte(GAME_PATH, 0x125E4, int(read_nes_byte(GAME_PATH, 0xCAA0), 16)) 
    edit_nes_byte(GAME_PATH, 0x125E6, int(read_nes_byte(GAME_PATH, 0xCA9F), 16)) 
    edit_nes_byte(GAME_PATH, 0x125E8, int(read_nes_byte(GAME_PATH, 0x125E4), 16))


def randomize_shadow_man_graphics():
# Randomizes the graphics for Shadow Man's stage.

    for i in range(0xEA92, 0xEAA2):
        if int(read_nes_byte(GAME_PATH, i), 16) not in [0x0F, 0x20, 0x30]:
            if(int(read_nes_byte(GAME_PATH, i), 16) in LIGHT_COLORS):
                edit_nes_byte(GAME_PATH, i, random.choice(LIGHT_COLORS_NW))
            else:
                edit_nes_byte(GAME_PATH, i, random.choice(DARK_COLORS_NB))

    # Darken the background to be less of an eyesore
    edit_nes_byte(GAME_PATH, 0xEA9A, random.randint(0x00, 0x0C))
    edit_nes_byte(GAME_PATH, 0xEA9B, random.randint(0x00, 0x0C))
    edit_nes_byte(GAME_PATH, 0xEA9C, random.randint(0x00, 0x0C))

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


def randomize_doc_needle_graphics():
# Randomizes the graphics for the Doc Needle Man stage.

    for i in range(0x10A92, 0x10AB6):
        if int(read_nes_byte(GAME_PATH, i), 16) not in [0x0F, 0x20, 0x30]:
            if(int(read_nes_byte(GAME_PATH, i), 16) in LIGHT_COLORS):
                edit_nes_byte(GAME_PATH, i, random.choice(LIGHT_COLORS_NW))
            else:
                edit_nes_byte(GAME_PATH, i, random.choice(DARK_COLORS_NB))

    # Gradient for stage graphics to make them look better
    doc_needle_bg = random.randint(0x10, 0x1C)
    doc_needle_bg_2 = random.randint(0x10, 0x1C)
    edit_nes_byte(GAME_PATH, 0x10A9B, doc_needle_bg + 0x10)
    edit_nes_byte(GAME_PATH, 0x10A9C, doc_needle_bg)
    edit_nes_byte(GAME_PATH, 0x10A9D, doc_needle_bg - 0x10)
    edit_nes_byte(GAME_PATH, 0x10A9F, doc_needle_bg_2 + 0x10)
    edit_nes_byte(GAME_PATH, 0x10AA0, doc_needle_bg_2)
    edit_nes_byte(GAME_PATH, 0x10AA1, doc_needle_bg_2 - 0x10)

    # Fixes for palette shift on Giant Metall screens
    edit_nes_byte(GAME_PATH, 0x10AA7, int(read_nes_byte(GAME_PATH, 0x10A93), 16))
    edit_nes_byte(GAME_PATH, 0x10AA8, int(read_nes_byte(GAME_PATH, 0x10A94), 16))
    edit_nes_byte(GAME_PATH, 0x10AA9, int(read_nes_byte(GAME_PATH, 0x10A95), 16))
    edit_nes_byte(GAME_PATH, 0x10AAF, int(read_nes_byte(GAME_PATH, 0x10A9B), 16))
    edit_nes_byte(GAME_PATH, 0x10AB0, int(read_nes_byte(GAME_PATH, 0x10A9C), 16))
    edit_nes_byte(GAME_PATH, 0x10AB1, int(read_nes_byte(GAME_PATH, 0x10A9D), 16))


def randomize_doc_gemini_graphics():
# Randomizes the graphics for the Doc Gemini Man stage.

    for i in range(0x12A92, 0x12AA2):
        if int(read_nes_byte(GAME_PATH, i), 16) not in [0x0F, 0x20, 0x30]:
            if(int(read_nes_byte(GAME_PATH, i), 16) in LIGHT_COLORS):
                edit_nes_byte(GAME_PATH, i, random.choice(LIGHT_COLORS_NW))
            else:
                edit_nes_byte(GAME_PATH, i, random.choice(DARK_COLORS_NB))

    # Fix for the ground changing color on the screen with transition underground
    edit_nes_byte(GAME_PATH, 0x12AEF, int(read_nes_byte(GAME_PATH, 0x12A9F), 16))
    edit_nes_byte(GAME_PATH, 0x12AF0, int(read_nes_byte(GAME_PATH, 0x12AA0), 16))
    edit_nes_byte(GAME_PATH, 0x12AF1, int(read_nes_byte(GAME_PATH, 0x12AA1), 16))

    # The blocks use the same palette as the original stage for the animation, so transfer over values to the static tileset
    edit_nes_byte(GAME_PATH, 0x12AA7, int(read_nes_byte(GAME_PATH, 0x125BF), 16))
    edit_nes_byte(GAME_PATH, 0x12AA8, int(read_nes_byte(GAME_PATH, 0x125C0), 16))
    edit_nes_byte(GAME_PATH, 0x12AA9, int(read_nes_byte(GAME_PATH, 0x125C1), 16))
    edit_nes_byte(GAME_PATH, 0x12AAB, int(read_nes_byte(GAME_PATH, 0x125C8), 16))
    edit_nes_byte(GAME_PATH, 0x12AAC, int(read_nes_byte(GAME_PATH, 0x125C9), 16))
    edit_nes_byte(GAME_PATH, 0x12AAD, int(read_nes_byte(GAME_PATH, 0x125CA), 16))
    edit_nes_byte(GAME_PATH, 0x12AAF, int(read_nes_byte(GAME_PATH, 0x125D1), 16))
    edit_nes_byte(GAME_PATH, 0x12AB0, int(read_nes_byte(GAME_PATH, 0x125D2), 16))
    edit_nes_byte(GAME_PATH, 0x12AB1, int(read_nes_byte(GAME_PATH, 0x125D3), 16))
    edit_nes_byte(GAME_PATH, 0x12ABB, int(read_nes_byte(GAME_PATH, 0x125BF), 16))
    edit_nes_byte(GAME_PATH, 0x12ABC, int(read_nes_byte(GAME_PATH, 0x125C0), 16))
    edit_nes_byte(GAME_PATH, 0x12ABD, int(read_nes_byte(GAME_PATH, 0x125C1), 16))
    edit_nes_byte(GAME_PATH, 0x12ABF, int(read_nes_byte(GAME_PATH, 0x125C8), 16))
    edit_nes_byte(GAME_PATH, 0x12AC0, int(read_nes_byte(GAME_PATH, 0x125C9), 16))
    edit_nes_byte(GAME_PATH, 0x12AC1, int(read_nes_byte(GAME_PATH, 0x125CA), 16))
    edit_nes_byte(GAME_PATH, 0x12AC3, int(read_nes_byte(GAME_PATH, 0x125D1), 16))
    edit_nes_byte(GAME_PATH, 0x12AC4, int(read_nes_byte(GAME_PATH, 0x125D2), 16))
    edit_nes_byte(GAME_PATH, 0x12AC5, int(read_nes_byte(GAME_PATH, 0x125D3), 16))
    edit_nes_byte(GAME_PATH, 0x12ACF, int(read_nes_byte(GAME_PATH, 0x125BF), 16))
    edit_nes_byte(GAME_PATH, 0x12AD0, int(read_nes_byte(GAME_PATH, 0x125C0), 16))
    edit_nes_byte(GAME_PATH, 0x12AD1, int(read_nes_byte(GAME_PATH, 0x125C1), 16))
    edit_nes_byte(GAME_PATH, 0x12AD3, int(read_nes_byte(GAME_PATH, 0x125C8), 16))
    edit_nes_byte(GAME_PATH, 0x12AD4, int(read_nes_byte(GAME_PATH, 0x125C9), 16))
    edit_nes_byte(GAME_PATH, 0x12AD5, int(read_nes_byte(GAME_PATH, 0x125CA), 16))
    edit_nes_byte(GAME_PATH, 0x12AD7, int(read_nes_byte(GAME_PATH, 0x125D1), 16))
    edit_nes_byte(GAME_PATH, 0x12AD8, int(read_nes_byte(GAME_PATH, 0x125D2), 16))
    edit_nes_byte(GAME_PATH, 0x12AD9, int(read_nes_byte(GAME_PATH, 0x125D3), 16))
    edit_nes_byte(GAME_PATH, 0x12AE3, int(read_nes_byte(GAME_PATH, 0x125BF), 16))
    edit_nes_byte(GAME_PATH, 0x12AE4, int(read_nes_byte(GAME_PATH, 0x125C0), 16))
    edit_nes_byte(GAME_PATH, 0x12AE5, int(read_nes_byte(GAME_PATH, 0x125C1), 16))
    edit_nes_byte(GAME_PATH, 0x12AE7, int(read_nes_byte(GAME_PATH, 0x125C8), 16))
    edit_nes_byte(GAME_PATH, 0x12AE8, int(read_nes_byte(GAME_PATH, 0x125C9), 16))
    edit_nes_byte(GAME_PATH, 0x12AE9, int(read_nes_byte(GAME_PATH, 0x125CA), 16))
    edit_nes_byte(GAME_PATH, 0x12AEB, int(read_nes_byte(GAME_PATH, 0x125D1), 16))
    edit_nes_byte(GAME_PATH, 0x12AEC, int(read_nes_byte(GAME_PATH, 0x125D2), 16))
    edit_nes_byte(GAME_PATH, 0x12AED, int(read_nes_byte(GAME_PATH, 0x125D3), 16))

    # Restrict background of the middle boss fight to avoid ugly backgrounds
    edit_nes_byte(GAME_PATH, 0x12AC8, random.randint(0x00, 0x0C))
    edit_nes_byte(GAME_PATH, 0x12AC9, random.randint(0x00, 0x0C))
    edit_nes_byte(GAME_PATH, 0x12AC7, random.randint(0x20, 0x2C))


def randomize_doc_spark_graphics():
# Randomizes the graphics for the Doc Spark Man stage.

    for i in range(0x14A92, 0x14AB6):
        if i not in [0x14AA2, 0x14AA3, 0x14AA4, 0x14AA5]: # These specific values are for tile animation and should not be messed with
            if int(read_nes_byte(GAME_PATH, i), 16) not in [0x0F, 0x20, 0x30]:
                if(int(read_nes_byte(GAME_PATH, i), 16) in LIGHT_COLORS):
                    edit_nes_byte(GAME_PATH, i, random.choice(LIGHT_COLORS_NW))
                else:
                    edit_nes_byte(GAME_PATH, i, random.choice(DARK_COLORS_NB))

    # The following few lines standardize the floor colors so that changing screens doesn't create weird jumbled color visuals
    edit_nes_byte(GAME_PATH, 0x14A98, int(read_nes_byte(GAME_PATH, 0x125DE), 16))
    edit_nes_byte(GAME_PATH, 0x14A99, int(read_nes_byte(GAME_PATH, 0x125DF), 16))
    edit_nes_byte(GAME_PATH, 0x14A9C, int(read_nes_byte(GAME_PATH, 0x125DE), 16))
    edit_nes_byte(GAME_PATH, 0x14A9F, int(read_nes_byte(GAME_PATH, 0x125E6), 16))
    edit_nes_byte(GAME_PATH, 0x14AA0, int(read_nes_byte(GAME_PATH, 0x125E4), 16))
    edit_nes_byte(GAME_PATH, 0x14AA8, int(read_nes_byte(GAME_PATH, 0x14A94), 16))
    edit_nes_byte(GAME_PATH, 0x14AA9, int(read_nes_byte(GAME_PATH, 0x14A95), 16))
    edit_nes_byte(GAME_PATH, 0x14AAC, int(read_nes_byte(GAME_PATH, 0x125DE), 16))
    edit_nes_byte(GAME_PATH, 0x14AAD, int(read_nes_byte(GAME_PATH, 0x125DF), 16))
    edit_nes_byte(GAME_PATH, 0x14AB0, int(read_nes_byte(GAME_PATH, 0x125DE), 16))
    

def randomize_doc_shadow_graphics():
# Randomizes the graphics for the Doc Shadow Man stage.

    for i in range(0x16A92, 0x16AA2):
        if int(read_nes_byte(GAME_PATH, i), 16) not in [0x0F, 0x20, 0x30]:
            if(int(read_nes_byte(GAME_PATH, i), 16) in LIGHT_COLORS):
                edit_nes_byte(GAME_PATH, i, random.choice(LIGHT_COLORS_NW))
            else:
                edit_nes_byte(GAME_PATH, i, random.choice(DARK_COLORS_NB))

    # Darken the background to be less of an eyesore
    edit_nes_byte(GAME_PATH, 0x16A9A, random.randint(0x00, 0x0C))
    edit_nes_byte(GAME_PATH, 0x16A9B, random.randint(0x00, 0x0C))
    edit_nes_byte(GAME_PATH, 0x16A9C, random.randint(0x00, 0x0C))

    # Put animated water values into base tileset to prevent weird color changes on transition
    edit_nes_byte(GAME_PATH, 0x16A97, int(read_nes_byte(GAME_PATH, 0x125E9), 16))
    edit_nes_byte(GAME_PATH, 0x16A98, int(read_nes_byte(GAME_PATH, 0x125EA), 16))
    edit_nes_byte(GAME_PATH, 0x16A99, int(read_nes_byte(GAME_PATH, 0x125EB), 16))

    # Fix spike background
    edit_nes_byte(GAME_PATH, 0x16A95, int(read_nes_byte(GAME_PATH, 0x16A9D), 16))


def randomize_break_man_graphics():
# Randomizes the graphics for Break Man's fight.

    # Incredibly weird but it seems that Mega Man's palette and Proto Man's palette are actually stored here along with the stage graphics? Editing the palettes around these values screws up their color schemes
    for i in range(0x31E3E, 0x31E4A):
        if int(read_nes_byte(GAME_PATH, i), 16) not in [0x0F, 0x20, 0x30]:
            if(int(read_nes_byte(GAME_PATH, i), 16) in LIGHT_COLORS):
                edit_nes_byte(GAME_PATH, i, random.choice(LIGHT_COLORS_NW))
            else:
                edit_nes_byte(GAME_PATH, i, random.choice(DARK_COLORS_NB))

    # The rocks look really terrible with totally random color schemes, so apply a gradient
    rock_base_color = random.randint(0x01, 0x0C)
    edit_nes_byte(GAME_PATH, 0x31E3D, rock_base_color)
    edit_nes_byte(GAME_PATH, 0x31E3C, rock_base_color + 0x20)
    edit_nes_byte(GAME_PATH, 0x31E3B, rock_base_color + 0x30)


def randomize_wily_1_graphics():
# Randomizes the graphics for the first Wily fortress stage.

    for i in range(0x18A92, 0x18AA2):
        if int(read_nes_byte(GAME_PATH, i), 16) not in [0x0F, 0x20, 0x30]:
            if(int(read_nes_byte(GAME_PATH, i), 16) in LIGHT_COLORS):
                edit_nes_byte(GAME_PATH, i, random.choice(LIGHT_COLORS_NW))
            else:
                edit_nes_byte(GAME_PATH, i, random.choice(DARK_COLORS_NB))

    # Give the rocks at the beginning a gradient so they don't look awful
    rock_base_color = random.randint(0x01, 0x0C)
    edit_nes_byte(GAME_PATH, 0x18A9D, rock_base_color)
    edit_nes_byte(GAME_PATH, 0x18A9C, rock_base_color + 0x20)
    edit_nes_byte(GAME_PATH, 0x18A9B, rock_base_color + 0x30)


def randomize_wily_2_graphics():
# Randomizes the graphics for the second Wily fortress stage.

    for i in range(0x1AA92, 0x1AAA2):
        if int(read_nes_byte(GAME_PATH, i), 16) not in [0x0F, 0x20, 0x30]:
            if(int(read_nes_byte(GAME_PATH, i), 16) in LIGHT_COLORS):
                edit_nes_byte(GAME_PATH, i, random.choice(LIGHT_COLORS_NW))
            else:
                edit_nes_byte(GAME_PATH, i, random.choice(DARK_COLORS_NB))


def randomize_wily_3_graphics():
# Randomizes the graphics for the third Wily fortress stage.

    for i in range(0x1CA92, 0x1CAA2):
        if int(read_nes_byte(GAME_PATH, i), 16) not in [0x0F, 0x20, 0x30]:
            if(int(read_nes_byte(GAME_PATH, i), 16) in LIGHT_COLORS):
                edit_nes_byte(GAME_PATH, i, random.choice(LIGHT_COLORS_NW))
            else:
                edit_nes_byte(GAME_PATH, i, random.choice(DARK_COLORS_NB))


def scramble_stage_palettes():
# This scrambles the color schemes for the stages in the game. Black and white are not replaced to maintain some level of graphical integrity, and black and white are excluded from the possible color options to prevent extreme eyesore.

    # Robot Masters
    randomize_needle_man_graphics()
    randomize_magnet_man_graphics()
    randomize_gemini_man_graphics()
    randomize_hard_man_graphics()
    randomize_top_man_graphics()
    randomize_snake_man_graphics()
    randomize_spark_man_graphics()
    randomize_shadow_man_graphics()

    # Doc Robots
    randomize_doc_needle_graphics()
    randomize_doc_gemini_graphics()
    randomize_doc_spark_graphics()
    randomize_doc_shadow_graphics()

    # Break Man
    randomize_break_man_graphics()

    # Wily Fortress
    randomize_wily_1_graphics()
    randomize_wily_2_graphics()
    randomize_wily_3_graphics()


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


def scramble_weapon_locations():
# This scrambles the stages where special weapons are found.

    for i in range(0x3DD14, 0x3DD1C):
        edit_nes_byte(GAME_PATH, i, WEAPON_POSITIONS[i - 0x3DD14][0])
        edit_nes_byte(GAME_PATH, i + 0x08, WEAPON_POSITIONS[i - 0x3DD14][1])

    # Weapon get screen palettes, set here to match the color of the randomized weapon locations
    # Weapon located in Needle Man's stage
    edit_nes_byte(GAME_PATH, 0x31BC8, 0x30)
    edit_nes_byte(GAME_PATH, 0x31BC9, WEAPON_POSITIONS[0][2] + 0x10)
    edit_nes_byte(GAME_PATH, 0x31BCA, WEAPON_POSITIONS[0][3])
    edit_nes_byte(GAME_PATH, 0x31BCC, WEAPON_POSITIONS[0][3] - 0x10)
    edit_nes_byte(GAME_PATH, 0x31BCD, WEAPON_POSITIONS[0][2])
    edit_nes_byte(GAME_PATH, 0x31BCE, WEAPON_POSITIONS[0][3])

    # Weapon located in Magnet Man's stage
    edit_nes_byte(GAME_PATH, 0x31BD0, 0x30)
    edit_nes_byte(GAME_PATH, 0x31BD1, WEAPON_POSITIONS[1][2] + 0x10)
    edit_nes_byte(GAME_PATH, 0x31BD2, WEAPON_POSITIONS[1][3])
    edit_nes_byte(GAME_PATH, 0x31BD4, WEAPON_POSITIONS[1][3] - 0x10)
    edit_nes_byte(GAME_PATH, 0x31BD5, WEAPON_POSITIONS[1][2])
    edit_nes_byte(GAME_PATH, 0x31BD6, WEAPON_POSITIONS[1][3])

    # Weapon located in Gemini Man's stage
    edit_nes_byte(GAME_PATH, 0x31BD8, 0x30)
    edit_nes_byte(GAME_PATH, 0x31BD9, WEAPON_POSITIONS[2][2] + 0x10)
    edit_nes_byte(GAME_PATH, 0x31BDA, WEAPON_POSITIONS[2][3])
    edit_nes_byte(GAME_PATH, 0x31BDC, WEAPON_POSITIONS[2][3] - 0x10)
    edit_nes_byte(GAME_PATH, 0x31BDD, WEAPON_POSITIONS[2][2])
    edit_nes_byte(GAME_PATH, 0x31BDE, WEAPON_POSITIONS[2][3])

    # Weapon located in Hard Man's stage
    edit_nes_byte(GAME_PATH, 0x31BE0, 0x30)
    edit_nes_byte(GAME_PATH, 0x31BE1, WEAPON_POSITIONS[3][2] + 0x10)
    edit_nes_byte(GAME_PATH, 0x31BE2, WEAPON_POSITIONS[3][3])
    edit_nes_byte(GAME_PATH, 0x31BE4, WEAPON_POSITIONS[3][3] - 0x10)
    edit_nes_byte(GAME_PATH, 0x31BE5, WEAPON_POSITIONS[3][2])
    edit_nes_byte(GAME_PATH, 0x31BE6, WEAPON_POSITIONS[3][3])

    # Weapon located in Top Man's stage
    edit_nes_byte(GAME_PATH, 0x31BE8, 0x30)
    edit_nes_byte(GAME_PATH, 0x31BE9, WEAPON_POSITIONS[4][2] + 0x10)
    edit_nes_byte(GAME_PATH, 0x31BEA, WEAPON_POSITIONS[4][3])
    edit_nes_byte(GAME_PATH, 0x31BEC, WEAPON_POSITIONS[4][3] - 0x10)
    edit_nes_byte(GAME_PATH, 0x31BED, WEAPON_POSITIONS[4][2])
    edit_nes_byte(GAME_PATH, 0x31BEE, WEAPON_POSITIONS[4][3])

    # Weapon located in Snake Man's stage
    edit_nes_byte(GAME_PATH, 0x31BF0, 0x30)
    edit_nes_byte(GAME_PATH, 0x31BF1, WEAPON_POSITIONS[5][2] + 0x10)
    edit_nes_byte(GAME_PATH, 0x31BF2, WEAPON_POSITIONS[5][3])
    edit_nes_byte(GAME_PATH, 0x31BF4, WEAPON_POSITIONS[5][3] - 0x10)
    edit_nes_byte(GAME_PATH, 0x31BF5, WEAPON_POSITIONS[5][2])
    edit_nes_byte(GAME_PATH, 0x31BF6, WEAPON_POSITIONS[5][3])

    # Weapon located in Spark Man's stage
    edit_nes_byte(GAME_PATH, 0x31BF8, 0x30)
    edit_nes_byte(GAME_PATH, 0x31BF9, WEAPON_POSITIONS[6][2] + 0x10)
    edit_nes_byte(GAME_PATH, 0x31BFA, WEAPON_POSITIONS[6][3])
    edit_nes_byte(GAME_PATH, 0x31BFC, WEAPON_POSITIONS[6][3] - 0x10)
    edit_nes_byte(GAME_PATH, 0x31BFD, WEAPON_POSITIONS[6][2])
    edit_nes_byte(GAME_PATH, 0x31BFE, WEAPON_POSITIONS[6][3])

    # Weapon located in Shadow Man's stage
    edit_nes_byte(GAME_PATH, 0x31C00, 0x30)
    edit_nes_byte(GAME_PATH, 0x31C01, WEAPON_POSITIONS[7][2] + 0x10)
    edit_nes_byte(GAME_PATH, 0x31C02, WEAPON_POSITIONS[7][3])
    edit_nes_byte(GAME_PATH, 0x31C04, WEAPON_POSITIONS[7][3] - 0x10)
    edit_nes_byte(GAME_PATH, 0x31C05, WEAPON_POSITIONS[7][2])
    edit_nes_byte(GAME_PATH, 0x31C06, WEAPON_POSITIONS[7][3])


def scramble_weapon_palettes():
# This scrambles the color palettes for all of the weapons except the Mega Buster.

    # Gemini Laser
    edit_nes_byte(GAME_PATH, 0x4656, ORDERED_WEAPONS[0][0])
    edit_nes_byte(GAME_PATH, 0x4657, ORDERED_WEAPONS[0][1])

    # Needle Cannon
    edit_nes_byte(GAME_PATH, 0x465A, ORDERED_WEAPONS[1][0])
    edit_nes_byte(GAME_PATH, 0x465B, ORDERED_WEAPONS[1][1])

    # Hard Knuckle
    edit_nes_byte(GAME_PATH, 0x465E, ORDERED_WEAPONS[2][0])
    edit_nes_byte(GAME_PATH, 0x465F, ORDERED_WEAPONS[2][1])

    # Magnet Missile
    edit_nes_byte(GAME_PATH, 0x4662, ORDERED_WEAPONS[3][0])
    edit_nes_byte(GAME_PATH, 0x4663, ORDERED_WEAPONS[3][1])

    # Top Spin
    edit_nes_byte(GAME_PATH, 0x4666, ORDERED_WEAPONS[4][0])
    edit_nes_byte(GAME_PATH, 0x4667, ORDERED_WEAPONS[4][1])

    # Search Snake
    edit_nes_byte(GAME_PATH, 0x466A, ORDERED_WEAPONS[5][0])
    edit_nes_byte(GAME_PATH, 0x466B, ORDERED_WEAPONS[5][1])

    # Spark Shock
    edit_nes_byte(GAME_PATH, 0x4672, ORDERED_WEAPONS[6][0])
    edit_nes_byte(GAME_PATH, 0x4673, ORDERED_WEAPONS[6][1])

    # Shadow Blade
    edit_nes_byte(GAME_PATH, 0x467A, ORDERED_WEAPONS[7][0])
    edit_nes_byte(GAME_PATH, 0x467B, ORDERED_WEAPONS[7][1])

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

    # Top Spin variables (currently nonfunctional; anti-knockback variables cause immediate drainage of energy)
    #top_spin_knockback = random.choice([[0x85, 0xF5], [0xEA, 0xEA]]) 
    #edit_nes_byte(GAME_PATH, 0x38281, 0x85) # Controls knockback from Top Spin; if EA, no knockback occurs
    #edit_nes_byte(GAME_PATH, 0x38282, 0xF5) # Controls knockback from Top Spin; if EA, no knockback occurs

    # Search Snake variables
    edit_nes_byte(GAME_PATH, 0x3D2CF, random.randint(0x00, 0x06)) # Search Snake vertical launch speed (default 03)
    edit_nes_byte(GAME_PATH, 0x3D2D9, random.randint(0x00, 0x04)) # Search Snake horizontal launch speed (default 01)
    edit_nes_byte(GAME_PATH, 0x3D2DE, random.randint(0x0A, 0x23)) # Timer before Search Snake halts (default 13)
    edit_nes_byte(GAME_PATH, 0x389F4, random.randint(0x02, 0x05)) # Crawling speed of Search Snake (default 03)

    # Shadow Blade variables
    edit_nes_byte(GAME_PATH, 0x3D2EB, random.choice([0x07, 0x0B, 0x0F])) # Shadow Blade shooting directions: see documentation for more info, but determines Shadow Blade throwable angles. Randomized between 5 upwards, 5 downwards, all 8 (Default 0B)
    edit_nes_byte(GAME_PATH, 0x3D2F7, random.randint(0x02, 0x07)) # Shadow Blade vertical launch speed (default 04)
    shadow_blade_returns = random.randint(0, 2) # Little randomization to see if Shadow Blade will boomerang at all. Default is a 33.33% chance to act like Metal Blade
    if shadow_blade_returns:
        edit_nes_byte(GAME_PATH, 0x3D2FC, random.randint(0x0A, 0x28)) # Shadow Blade range, i.e. how long it travels before boomeranging. Setting it high enough causes it to act like Metal Blade (default 14)
    else:
        edit_nes_byte(GAME_PATH, 0x3D2FC, 0xFF) # 0xFF is more than enough range for the blade to never boomerang
    edit_nes_byte(GAME_PATH, 0x38AEB, random.randint(0x04, 0x24)) # Length of time before Shadow Blade is deleted after it boomerangs back (default 14)

    # Rush Jet variables
    # edit_nes_byte(GAME_PATH, 0x3CFB8, 0x02) # Rush Jet vertical speed; only enabled in burst chaser mode (default 01) 


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
    proto_color = random.randint(0x11, 0x1C)
    # Version that appears to blow up barrier in Gemini Man's stage
    edit_nes_byte(GAME_PATH, 0x20F2, 0x10) # Proto Man grey
    edit_nes_byte(GAME_PATH, 0x20F3, proto_color) # Proto Man red
    # Fight version
    edit_nes_byte(GAME_PATH, 0x20B2, 0x10) # Proto Man grey
    edit_nes_byte(GAME_PATH, 0x20B3, proto_color) # Proto Man red


def scramble_sprite_health():
# Scrambles the health values for the enemies of the game. Bosses are not affected.

    for i in range(0x410, 0x49F):
        if int(read_nes_byte(GAME_PATH, i), 16) not in [0x1C, 0xFF, 0x00]: # Do not scramble bosses or any entity with null/zero HP
            edit_nes_byte(GAME_PATH, i, random.randint(math.ceil(int(read_nes_byte(GAME_PATH, i), 16) * 0.5), math.ceil(int(read_nes_byte(GAME_PATH, i), 16) * 1.5))) # Move HP values between half and one and a half times normal HP


def scramble_sprite_speed():
# Scrambles the speed values for the sprites of the game.

    for i in range(0x510, 0x58F):
        if int(read_nes_byte(GAME_PATH, i), 16) not in [0x1C, 0xFF, 0x00]: # Do not scramble bosses or any entity with no movement value to avoid causing weird issues
            edit_nes_byte(GAME_PATH, i, random.randint(0x01, 0x0A))


def scramble_miniboss_behaviors():
# Scrambles the behaviors of the game's minibosses.

    # Proto Man
    edit_nes_byte(GAME_PATH, 0x3A138, random.randint(0x03, 0x07)) # Jumping height (default 05)
    edit_nes_byte(GAME_PATH, 0x3A2D9, random.randint(0x02, 0x06)) # Bullet speed (default 04)

    # Tama
    edit_nes_byte(GAME_PATH, 0x3BB93, 0x20) # Tama color palette white (default 20)
    tama_color = random.choice([0x11, 0x13, 0x15, 0x17, 0x19, 0x1B]) # Extremely weird; Tama does not display correctly unless its color values are set to odd numbers
    edit_nes_byte(GAME_PATH, 0x219A, tama_color + 0x20) # Tama sprite light color
    edit_nes_byte(GAME_PATH, 0x219B, tama_color) # Tama sprite dark color
    edit_nes_byte(GAME_PATH, 0x3BB9B, tama_color + 0x20) # Tama bg color palette light color (default 37)
    edit_nes_byte(GAME_PATH, 0x3BBA3, tama_color) # Tama bg color palette dark color (default 17)
    edit_nes_byte(GAME_PATH, 0x3BD82, random.randint(0x01, 0x05)) # Jumping height of yarn balls (default 03)
    edit_nes_byte(GAME_PATH, 0x3BC3D, random.randint(0x01, 0x03)) # Number of yarn balls spit out (default 02)
    edit_nes_byte(GAME_PATH, 0x3BC4F, random.randint(0x1C, 0x5C)) # Delay time for yarn balls after first (default 3C)
    edit_nes_byte(GAME_PATH, 0x3BC9F, random.randint(0x01, 0x02)) # Speed of balls (default 01)
    # edit_nes_byte(GAME_PATH, 0x3BD3B, 0x00) # Height of fleas thrown into the air (default 00)
    edit_nes_byte(GAME_PATH, 0x3BD72, random.randint(0x00, 0x02)) # Horizontal speed of flea 1 (default 01)
    edit_nes_byte(GAME_PATH, 0x3BD73, random.randint(0x00, 0x02)) # Horizontal speed of flea 2 (default 01)
    edit_nes_byte(GAME_PATH, 0x3BD74, random.randint(0x00, 0x02)) # Horizontal speed of flea 3 (default 01)
    edit_nes_byte(GAME_PATH, 0x3BDD4, random.randint(0x1C, 0x4C)) # Flea jumping delay time (default 3C)
    edit_nes_byte(GAME_PATH, 0x3BDDE, random.randint(0x03, 0x07)) # Flea jumping height (default 05)
    edit_nes_byte(GAME_PATH, 0x3BDE8, random.randint(0x00, 0x01)) # Flea jumping horizontal speed (default 00)

    # Big Snakey
    edit_nes_byte(GAME_PATH, 0x21A5, int(read_nes_byte(GAME_PATH, 0xAA92), 16)) # Big Snakey mouth color 1
    edit_nes_byte(GAME_PATH, 0x21A6, int(read_nes_byte(GAME_PATH, 0xAA93), 16)) # Big Snakey body color
    edit_nes_byte(GAME_PATH, 0x21A7, int(read_nes_byte(GAME_PATH, 0xAA94), 16)) # Big Snakey mouth color 2
    edit_nes_byte(GAME_PATH, 0x3BA96, random.randint(0x58, 0x88)) # Time until next attack phase (default 78)
    edit_nes_byte(GAME_PATH, 0x3BADA, random.randint(0x02, 0x06)) # Speed of shots (default 04)
    edit_nes_byte(GAME_PATH, 0x3BB61, random.randint(0x01, 0x05)) # Setting for number of energy balls shot (randomly selects between these four values) (default 03)
    edit_nes_byte(GAME_PATH, 0x3BB62, random.randint(0x01, 0x05)) # Setting for number of energy balls shot (randomly selects between these four values) (default 03)
    edit_nes_byte(GAME_PATH, 0x3BB63, random.randint(0x01, 0x05)) # Setting for number of energy balls shot (randomly selects between these four values) (default 04)
    edit_nes_byte(GAME_PATH, 0x3BB64, random.randint(0x01, 0x05)) # Setting for number of energy balls shot (randomly selects between these four values) (default 02)

    # Giant Metall
    edit_nes_byte(GAME_PATH, 0x25510, random.randint(0x0E, 0x2E)) # Time until third Metall is released after the first two (default 1E)
    edit_nes_byte(GAME_PATH, 0x25589, random.randint(0x0E, 0x2E)) # Time until second Metall is released after the first (default 1E)
    edit_nes_byte(GAME_PATH, 0x2559E, random.randint(0x02, 0x05)) # Number of Metalls that are released (default 03)
    edit_nes_byte(GAME_PATH, 0x25644, random.randint(0x01, 0x04)) # Speed of Metalls (default 02)
    edit_nes_byte(GAME_PATH, 0x25655, random.randint(0x01, 0x02)) # Speed of balls (default 00)
    edit_nes_byte(GAME_PATH, 0x25656, random.randint(0x01, 0x02)) # Speed of balls (default 01)
    edit_nes_byte(GAME_PATH, 0x25657, random.randint(0x01, 0x02)) # Speed of balls (default 00)
    edit_nes_byte(GAME_PATH, 0x25665, int(read_nes_byte(GAME_PATH, 0x10A93), 16)) # Palette loaded when Giant Metall is defeated (default 20)
    edit_nes_byte(GAME_PATH, 0x25666, int(read_nes_byte(GAME_PATH, 0x10A94), 16)) # Palette loaded when Giant Metall is defeated (default 27)
    edit_nes_byte(GAME_PATH, 0x25667, int(read_nes_byte(GAME_PATH, 0x10A95), 16)) # Palette loaded when Giant Metall is defeated (default 17)
    edit_nes_byte(GAME_PATH, 0x25669, int(read_nes_byte(GAME_PATH, 0x10A97), 16)) # Palette loaded when Giant Metall is defeated (default 03)
    edit_nes_byte(GAME_PATH, 0x2566A, int(read_nes_byte(GAME_PATH, 0x10A98), 16)) # Palette loaded when Giant Metall is defeated (default 12)
    edit_nes_byte(GAME_PATH, 0x2566D, int(read_nes_byte(GAME_PATH, 0x10A9B), 16)) # Palette loaded when Giant Metall is defeated (default 2B)
    edit_nes_byte(GAME_PATH, 0x2566E, int(read_nes_byte(GAME_PATH, 0x10A9C), 16)) # Palette loaded when Giant Metall is defeated (default 1B)
    edit_nes_byte(GAME_PATH, 0x2566F, int(read_nes_byte(GAME_PATH, 0x10A9D), 16)) # Palette loaded when Giant Metall is defeated (default 0B)
    edit_nes_byte(GAME_PATH, 0x25671, int(read_nes_byte(GAME_PATH, 0x10A9F), 16)) # Palette loaded when Giant Metall is defeated (default 22)
    edit_nes_byte(GAME_PATH, 0x25672, int(read_nes_byte(GAME_PATH, 0x10AA0), 16)) # Palette loaded when Giant Metall is defeated (default 12)
    edit_nes_byte(GAME_PATH, 0x25673, int(read_nes_byte(GAME_PATH, 0x10AA1), 16)) # Palette loaded when Giant Metall is defeated (default 02)


def replace_entities(graphics_set, enemy_lower_bound, enemy_upper_bound, *args):
# A helper function that replaces stage entities, handling graphics sets and easily allowing for the replacement of multiple entities at once.

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

    # Randomize the boss himself
    edit_nes_byte(GAME_PATH, 0xE2E, RANDOMIZED_ROBOT_MASTERS[0][0])
    edit_nes_byte(GAME_PATH, 0xA7E, RANDOMIZED_ROBOT_MASTERS[0][1])


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

    # Seventh screen with Yoku blocks, can only randomize to 0x09 and 0x19 to not mess up Yoku block sprites
    replace_entities(0x2A7C, 0x2E27, 0x2E2D, random.choice([0x09, 0x19]))

    # Eighth screen with just pickups
    replace_entities(0x2A7E, 0x2E2D, 0x2E31)

    # Ninth screen with New Shotman
    replace_entities(0x2A80, 0x2E31, 0x2E32)

    # Tenth screen with Giant Springer
    replace_entities(0x2A82, 0x2E32, 0x2E33)

    # Randomize the boss himself
    edit_nes_byte(GAME_PATH, 0x2E33, RANDOMIZED_ROBOT_MASTERS[1][0])
    edit_nes_byte(GAME_PATH, 0x2A86, RANDOMIZED_ROBOT_MASTERS[1][1])


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
    edit_nes_byte(GAME_PATH, 0x4E4C, RANDOMIZED_ROBOT_MASTERS[2][0])
    edit_nes_byte(GAME_PATH, 0x4A84, RANDOMIZED_ROBOT_MASTERS[2][1])


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
    edit_nes_byte(GAME_PATH, 0x6E37, RANDOMIZED_ROBOT_MASTERS[3][0])
    edit_nes_byte(GAME_PATH, 0x6A88, RANDOMIZED_ROBOT_MASTERS[3][1])


def randomize_top_man_entities():
# Randomizes the entities for Top Man's stage.

    # First screen with Bolton & Nuttons and Mechakkeros
    replace_entities(0x8A70, 0x8E10, 0x8E1C)

    # Second screen with Komasaburo
    replace_entities(0x8A72, 0x8E1C, 0x8E1D)

    # Third screen with pickups... we don't need this many pickups hehe
    replace_entities(0x8A74, 0x8E1D, 0x8E21)

    # Fourth screen with just a Bolton & Nutton
    replace_entities(0x8A76, 0x8E21, 0x8E22)

    # Fifth screen with Pickelman Bulls... I suppose I'll leave the pickups alone
    replace_entities(0x8A78, 0x8E22, 0x8E27)
    edit_nes_byte(GAME_PATH, 0x8E24, 0x55)
    edit_nes_byte(GAME_PATH, 0x8E25, 0x50)

    # Sixth screen with Metalls
    replace_entities(0x8A7A, 0x8E27, 0x8E29)

    # Seventh screen with Tama, we won't replace it
    # replace_entities(0x8A7C, 0x8E29, 0x8E2E)

    # Eighth screen with Komasaburo
    replace_entities(0x8A7E, 0x8E2E, 0x8E2F)

    # Ninth screen with Tama, we won't replace this either
    # replace_entities(0x8A80, 0x8E2F, 0x8E34)

    # Tenth screen with Metall and health pickup
    replace_entities(0x8A82, 0x8E34, 0x8E35)

    # Eleventh screen with Komasaburo and top platforms (do not replace the platforms)
    replace_entities(0x8A84, 0x8E36, 0x8E37, random.choice([0x16, 0x31]))

    # Randomize the boss himself
    edit_nes_byte(GAME_PATH, 0x8E3D, RANDOMIZED_ROBOT_MASTERS[4][0])
    edit_nes_byte(GAME_PATH, 0x8A88, RANDOMIZED_ROBOT_MASTERS[4][1])


def randomize_snake_man_entities():
# Randomizes the entities for Snake Man's stage.

    # First screen with Dadas and Petit Snakeys
    replace_entities(0xAA70, 0xAE10, 0xAE17)
    
    # Second screen with more Petit Snakeys
    replace_entities(0xAA72, 0xAE17, 0xAE1A)

    # Third screen with Big Snakey, do not replace
    # replace_entities(0xAA74, 0xAE1A, 0xAE25)

    # Fourth screen with Pottons and Petit Snakeys... leave one health pickup
    replace_entities(0xAA76, 0xAE25, 0xAE2D)
    edit_nes_byte(GAME_PATH, 0xAE2A, 0x50)

    # Fifth screen with Pottons and Bubukans
    replace_entities(0xAA78, 0xAE2D, 0xAE33)

    # Sixth screen with Hammer Joe
    replace_entities(0xAA7A, 0xAE33, 0xAE34)

    # Seventh screen with Hammer Joe
    replace_entities(0xAA7C, 0xAE34, 0xAE35)

    # Eighth screen with the surprise boxes... I'll leave these be
    # replace_entities(0xAA7E, 0xAE35, 0xAE37)

    # Ninth screen with Big Snakey, do not replace
    # replace_entities(0xAA80, 0xAE37, 0xAE42)

    # Tenth screen with Bubukans
    replace_entities(0xAA82, 0xAE42, 0xAE47)

    # Eleventh screen with Jamacy
    replace_entities(0xAA84, 0xAE47, 0xAE48)

    # Twelfth screen with Bomb Fliers and cloud platforms, do not replace the platforms
    replace_entities(0xAA86, 0xAE4C, 0xAE5A, random.choice([0x06, 0x1B]))
    edit_nes_byte(GAME_PATH, 0xAE4D, 0x0B)
    edit_nes_byte(GAME_PATH, 0xAE50, 0x0B)
    edit_nes_byte(GAME_PATH, 0xAE54, 0x0B)

    # Randomize the boss himself
    edit_nes_byte(GAME_PATH, 0xAE5A, RANDOMIZED_ROBOT_MASTERS[5][0])
    edit_nes_byte(GAME_PATH, 0xAA8A, RANDOMIZED_ROBOT_MASTERS[5][1])


def randomize_spark_man_entities():
# Randomizes the entities for Spark Man's stage.

    # First screen with Peterchy
    replace_entities(0xCA70, 0xCE10, 0xCE11)

    # Second screen with Electric Gabyoalls and Elec'ns
    replace_entities(0xCA72, 0xCE11, 0xCE18)

    # Third screen with Hammer Joe
    replace_entities(0xCA74, 0xCE18, 0xCE19)

    # Fourth screen with rising platforms and Electric Gabyoalls, do not replace the platforms
    replace_entities(0xCA76, 0xCE1D, 0xCE1F, random.choice([0x02, 0x03, 0x13, 0x1A, 0x22, 0x2D]))

    # Fifth screen with Pickelman Bull
    replace_entities(0xCA78, 0xCE1F, 0xCE20)

    # Sixth screen with Peterchys
    replace_entities(0xCA7A, 0xCE22, 0xCE26)

    # Seventh, eighth, and ninth screens are all empty

    # Tenth screen with junk blocks
    replace_entities(0xCA82, 0xCE26, 0xCE29)

    # Eleventh screen with rising platforms and Bolton & Nuttons, put the platforms back
    replace_entities(0xCA84, 0xCE2E, 0xCE38, random.choice([0x02, 0x03, 0x13, 0x1A, 0x22, 0x2D]))
    edit_nes_byte(GAME_PATH, 0xCE2F, 0x2D)
    edit_nes_byte(GAME_PATH, 0xCE32, 0x2D)
    edit_nes_byte(GAME_PATH, 0xCE35, 0x2D)

    # Randomize the boss himself
    edit_nes_byte(GAME_PATH, 0xCE38, RANDOMIZED_ROBOT_MASTERS[6][0])
    edit_nes_byte(GAME_PATH, 0xCA88, RANDOMIZED_ROBOT_MASTERS[6][1])


def randomize_shadow_man_entities():
# Randomizes the entities for Shadow Man's stage.

    # First screen with nothing on it
    # replace_entities(0xEA70, 0xEE10, 0xEE11)

    # Second screen with New Shotman
    replace_entities(0xEA72, 0xEE10, 0xEE11)

    # Third screen with nothing on it
    # replace_entities(0xEA74, 0xEE11, 0xEE12)

    # Fourth screen with Mechakkeros and Pickelman Bull
    replace_entities(0xEA76, 0xEE11, 0xEE14)

    # Fifth screen with Proto Man (do not replace)
    # replace_entities(0xEA78, 0xEE14, 0xEE15)

    # Sixth screen with Peterchys, Holograns, Walking Bombs
    replace_entities(0xEA7A, 0xEE15, 0xEE2A)

    # Seventh screen with Mechakkeros, Parasyus, Yambows
    replace_entities(0xEA7C, 0xEE2E, 0xEE3D)

    # Randomize the boss himself
    edit_nes_byte(GAME_PATH, 0xEE3D, RANDOMIZED_ROBOT_MASTERS[7][0])
    edit_nes_byte(GAME_PATH, 0xEA80, RANDOMIZED_ROBOT_MASTERS[7][1])


def randomize_doc_needle_entities():
# Randomizes the entities for the Doc Needle Man stage.

    # First screen with Hari Haris
    replace_entities(0x10A70, 0x10E10, 0x10E13)

    # Second screen with needle obstacles
    replace_entities(0x10A72, 0x10E13, 0x10E20)

    # Third screen with Giant Springer and life
    replace_entities(0x10A74, 0x10E20, 0x10E21)

    # Fourth screen with E-Tank, leave it alone
    # replace_entities(0x10A76, 0x10E22, 0x10E23)

    # Fifth screen with Hari Hari
    replace_entities(0x10A78, 0x10E23, 0x10E24)

    # Sixth screen is a door transition

    # Seventh screen with first Doc Robot boss
    edit_nes_byte(GAME_PATH, 0x10E24, RANDOMIZED_DOC_ROBOTS[0][0])
    edit_nes_byte(GAME_PATH, 0x10A7C, RANDOMIZED_DOC_ROBOTS[0][1])

    # Eighth screen with Yambows and Parasyus; keep the weapon energy pickups
    replace_entities(0x10A7E, 0x10E26, 0x10E40)
    edit_nes_byte(GAME_PATH, 0x10E2D, 0x52)
    edit_nes_byte(GAME_PATH, 0x10E32, 0x52)
    edit_nes_byte(GAME_PATH, 0x10E34, 0x52)
    edit_nes_byte(GAME_PATH, 0x10E3B, 0x52)

    # Ninth screen with nothing on it

    # Tenth screen with Bubukan
    replace_entities(0x10A82, 0x10E42, 0x10E43)

    # Eleventh screen with Giant Metall (do not replace)
    # replace_entities(0x10A84, 0x10E43, 0x10E44)

    # Twelfth screen with Metalls (heli variant) and Cannons
    replace_entities(0x10A86, 0x10E44, 0x10E4B)

    # Thirteenth screen with Giant Metall (do not replace)
    # replace_entities(0x10A88, 0x10E4B, 0x10E4C)

    # Fourteenth screen with Hari Hari and health pickup; leave the health pickup
    replace_entities(0x10A8A, 0x10E4C, 0x10E4D)

    # Fifteenth screen is a door transition

    # Randomize the second Doc Robot boss
    edit_nes_byte(GAME_PATH, 0x10E4E, RANDOMIZED_DOC_ROBOTS[1][0])
    edit_nes_byte(GAME_PATH, 0x10A8E, RANDOMIZED_DOC_ROBOTS[1][1])


def randomize_doc_gemini_entities():
# Randomizes the entities for the Doc Gemini Man stage.

    # First screen with Jamacys and Nitrons; choose a graphics set that is compatible with star background
    replace_entities(0x12A70, 0x12E10, 0x12E2A, random.choice([0x04, 0x14, 0x1A, 0x1C, 0x1D, 0x20, 0x2F, 0x39]))

    # Second screen is the empty crater where the barrier once was

    # Third screen with Pottons; choose a graphics set that has Poles
    replace_entities(0x12A74, 0x12E2B, 0x12E2E, random.choice([0x03, 0x33, 0x38]))

    # Fourth screen with Pottons; choose a graphics set that has Poles
    replace_entities(0x12A76, 0x12E2F, 0x12E33, random.choice([0x03, 0x33, 0x38]))

    # Fifth screen is a door transition

    # Sixth screen with first Doc Robot boss
    edit_nes_byte(GAME_PATH, 0x12E33, RANDOMIZED_DOC_ROBOTS[2][0])
    edit_nes_byte(GAME_PATH, 0x12A7A, RANDOMIZED_DOC_ROBOTS[2][1])

    # Seventh screen with Jamacy generator; I've replaced this with a conveyor wheel to prevent softlocks

    # Eighth screen with Gyoraibos and Pottons; keep the weapon energy pickups and pick a graphics set with the correct water splash animation
    replace_entities(0x12A7E, 0x12E36, 0x12E42, random.choice([0x03, 0x33, 0x38]))
    edit_nes_byte(GAME_PATH, 0x12E3C, 0x52)

    # Ninth screen with Pottons; pick a graphics set with the correct water splash animation
    replace_entities(0x12A80, 0x12E42, 0x12E45, random.choice([0x03, 0x33, 0x38]))

    # Tenth screen with Jamacys
    replace_entities(0x12A82, 0x12E45, 0x12E4B)

    # Eleventh screen with Jamacys
    replace_entities(0x12A84, 0x12E4B, 0x12E4D)

    # Twelfth screen is empty, but there is a mistake with the water graphics set here
    edit_nes_byte(GAME_PATH, 0x12A86, random.choice([0x03, 0x33, 0x38]))

    # Thirteenth screen is a door transition

    # Randomize the second Doc Robot boss
    edit_nes_byte(GAME_PATH, 0x12E4D, RANDOMIZED_DOC_ROBOTS[3][0])
    edit_nes_byte(GAME_PATH, 0x12A8A, RANDOMIZED_DOC_ROBOTS[3][1])


def randomize_doc_spark_entities():
# Randomizes the entities for the Doc Spark Man stage.
    
    # First screen with Peterchy; I've replaced this with a conveyor wheel to prevent softlocks
    # replace_entities(0x14A70, 0x14E10, 0x14E11)

    # Second screen with Jamacy; this needs to be converted into something non-threatening (i.e. health pickup) because in the vast majority of cases it will become impassable
    # replace_entities(0x14A72, 0x14E11, 0x14E12)
    edit_nes_byte(GAME_PATH, 0x14E11, 0x51)

    # Third screen with wheels and Elec'ns; this is a very restrictive screen since only one graphics set has the wheel graphics alongside any other enemies
    replace_entities(0x14A74, 0x14E12, 0x14E1B, 0x39)
    edit_nes_byte(GAME_PATH, 0x14E13, 0x59)
    edit_nes_byte(GAME_PATH, 0x14E15, 0x59)
    edit_nes_byte(GAME_PATH, 0x14E17, 0x58)
    edit_nes_byte(GAME_PATH, 0x14E19, 0x59)

    # Fourth screen is exclusively wheels, do not replace
    # replace_entities(0x14A76, 0x14E1C, 0x14E20)

    # Fifth screen with Giant Springers
    replace_entities(0x14A78, 0x14E21, 0x14E23)

    # Sixth screen is a door transition

    # Seventh screen with first Doc Robot boss
    edit_nes_byte(GAME_PATH, 0x14E23, RANDOMIZED_DOC_ROBOTS[4][0])
    edit_nes_byte(GAME_PATH, 0x14A7C, RANDOMIZED_DOC_ROBOTS[4][1])

    # Eighth screen is spike drop start

    # Ninth screen is spike drop
    
    # Tenth screen is spike drop

    # Eleventh screen is spike drop

    # Twelfth screen is long hallway with Bolton & Nuttons and Electric Gabyoalls
    replace_entities(0x14A86, 0x14E25, 0x14E31)

    # Thirteenth screen with junk blocks
    replace_entities(0x14A88, 0x14E31, 0x14E34)

    # Fourteenth screen is a door transition

    # Randomize the second Doc Robot boss
    edit_nes_byte(GAME_PATH, 0x14E34, RANDOMIZED_DOC_ROBOTS[5][0])
    edit_nes_byte(GAME_PATH, 0x14A8C, RANDOMIZED_DOC_ROBOTS[5][1])


def randomize_doc_shadow_entities():
# Randomizes the entities for the Doc Shadow stage.

    # First screen that's empty
    # replace_entities(0x16A70, 0x16E10, 0x16E11)

    # Second screen that's empty
    # replace_entities(0x16A72, 0x16E10, 0x16E11)

    # Third screen that's empty
    # replace_entities(0x16A74, 0x16E10, 0x16E11)

    # Fourth screen with Peterchys
    replace_entities(0x16A76, 0x16E10, 0x16E13)

    # Fifth screen with Bikky
    replace_entities(0x16A78, 0x16E13, 0x16E14)

    # Sixth screen with Peterchys, Walking Bombs, and Holograns; keep the dropping platforms
    replace_entities(0x16A7A, 0x16E14, 0x16E2E, random.choice([0x08]))
    edit_nes_byte(GAME_PATH, 0x16E18, 0x5A)
    edit_nes_byte(GAME_PATH, 0x16E19, 0x5A)
    edit_nes_byte(GAME_PATH, 0x16E1B, 0x5A)
    edit_nes_byte(GAME_PATH, 0x16E1D, 0x5A)
    edit_nes_byte(GAME_PATH, 0x16E21, 0x5A)
    edit_nes_byte(GAME_PATH, 0x16E22, 0x5A)
    edit_nes_byte(GAME_PATH, 0x16E24, 0x5A)
    edit_nes_byte(GAME_PATH, 0x16E25, 0x5A)
    edit_nes_byte(GAME_PATH, 0x16E26, 0x5A)
    edit_nes_byte(GAME_PATH, 0x16E27, 0x5A)
    edit_nes_byte(GAME_PATH, 0x16E28, 0x5A)
    edit_nes_byte(GAME_PATH, 0x16E29, 0x5A)
    edit_nes_byte(GAME_PATH, 0x16E2B, 0x5A)

    # Seventh screen with Peterchys
    replace_entities(0x16A7C, 0x16E2E, 0x16E30)

    # Eighth screen is a door transition

    # Ninth screen with the first Doc Robot boss
    edit_nes_byte(GAME_PATH, 0x16E30, RANDOMIZED_DOC_ROBOTS[6][0])
    edit_nes_byte(GAME_PATH, 0x16A80, RANDOMIZED_DOC_ROBOTS[6][1])

    # Tenth screen with Hammer Joes; leave the health pickup
    replace_entities(0x16A82, 0x16E32, 0x16E35)

    # Eleventh screen with Parasyus and Mechakkeros
    replace_entities(0x16A84, 0x16E35, 0x16E44)

    # Twelfth screen with Giant Springer
    replace_entities(0x16A86, 0x16E44, 0x16E45)

    # Thirteenth screen is a door transition

    # Randomize the second Doc Robot boss
    edit_nes_byte(GAME_PATH, 0x16E45, RANDOMIZED_DOC_ROBOTS[7][0])
    edit_nes_byte(GAME_PATH, 0x16A8A, RANDOMIZED_DOC_ROBOTS[7][1])


def randomize_wily_1_entities():
# Randomizes the entities for the first Wily fortress stage.

    # First screen with 1-up, Komasaburos, E-Tank; I'm removing the free items because I'm evil >:)
    replace_entities(0x18A70, 0x18E10, 0x18E14)

    # Second screen with Penpens
    replace_entities(0x18A72, 0x18E14, 0x18E1E)

    # Third screen with 1-up... this one can stay
    #replace_entities(0x18A74, 0x18E14, 0x18E1E)

    # Fourth screen with a bunch of items; remove the free health that's available after the first wall
    replace_entities(0x18A76, 0x18E27, 0x18E28, random.choice([0x06, 0x09, 0x19, 0x1B]))

    # Fifth screen with Hammer Joes
    replace_entities(0x18A78, 0x18E28, 0x18E2C)

    # Sixth screen, only randomize to graphics sets that contain Yoku blocks; also take one health pickup away >:)
    replace_entities(0x18A7A, 0x18E2C, 0x18E2D, random.choice([0x09, 0x19]))

    # Seventh screen with weapon energy, leave it alone

    # Eighth screen is door

    # Leave Kamegoro Maker untouched


def randomize_wily_2_entities():
# Randomizes the entities for the second Wily fortress stage.

    # First screen with just the dropping platforms; leave this alone
    #replace_entities(0x1AA70, 0x1AE10, 0x1AE13)

    # Second screen with more platforms and weapon energy; leave this alone
    #replace_entities(0x1AA72, 0x1AE13, 0x1AE17)

    # Third screen with 1-up... replace this with an enemy for evil reasons >:)
    replace_entities(0x1AA74, 0x1AE18, 0x1AE19, random.choice([0x08]))

    # Fourth screen with Wanaans and Have "Su" Bees; replace these and also most of the items because what is this some sort of charity shop lmao
    replace_entities(0x1AA76, 0x1AE19, 0x1AE33)
    edit_nes_byte(GAME_PATH, 0x1AE28, 0x52)
    edit_nes_byte(GAME_PATH, 0x1AE2B, 0x51)
    edit_nes_byte(GAME_PATH, 0x1AE2F, 0x54)
    edit_nes_byte(GAME_PATH, 0x1AE31, 0x52)

    # What a lengthy stage, am I right... anyways leave Yellow Devil MK-II alone


def randomize_wily_3_entities():
# Randomizes the entities for the third Wily fortress stage.

    # First screen with New Shotman
    replace_entities(0x1CA70, 0x1CE10, 0x1CE11)

    # Second screen with New Shotman and weapon energy... I'll leave these
    replace_entities(0x1CA72, 0x1CE11, 0x1CE12, random.choice([0x06, 0x09, 0x19, 0x1B]))

    # Third screen with Walking Bombs and Holograns; I'll leave the 1-up here but not the health
    replace_entities(0x1CA74, 0x1CE17, 0x1CE26)
    edit_nes_byte(GAME_PATH, 0x1CE1A, 0x55)
    edit_nes_byte(GAME_PATH, 0x1CE23, 0x52)

    # Fourth screen; this screen pisses me off so bad that I'm making the executive decision to actually move this enemy in the player's way
    replace_entities(0x1CA76, 0x1CE26, 0x1CE27)
    edit_nes_byte(GAME_PATH, 0x1CD26, 0xB0)

    # Fifth screen with Bikkys
    replace_entities(0x1CA78, 0x1CE27, 0x1CE29)

    # Sixth screen; I think it would be hilarious to replace the moving platforms but I won't
    
    # Seventh screen; I think it would be hilarious to replace the moving platforms but I won't

    # Eighth screen; don't bother taking items away from the player here

    # Leave Holograph Mega Mans alone


def scramble_stage_entities():
# This scrambles all the stage entities.

    # Robot Masters
    randomize_needle_man_entities()
    randomize_magnet_man_entities()
    randomize_gemini_man_entities()
    randomize_hard_man_entities()
    randomize_top_man_entities()
    randomize_snake_man_entities()
    randomize_spark_man_entities()
    randomize_shadow_man_entities()

    # Doc Robots
    randomize_doc_needle_entities()
    randomize_doc_gemini_entities()
    randomize_doc_spark_entities()
    randomize_doc_shadow_entities()

    # Wily Fortress
    randomize_wily_1_entities()
    randomize_wily_2_entities()
    randomize_wily_3_entities()


def scramble_entity_properties():
# This scrambles certain properties of the entities in the game.

    # Dada (entity ID 00)
    edit_nes_byte(GAME_PATH, 0x38B65, random.randint(0x01, 0x05)) # Dada jump height 1 (default 03)
    edit_nes_byte(GAME_PATH, 0x38B66, random.randint(0x01, 0x05)) # Dada jump height 2 (default 03)
    edit_nes_byte(GAME_PATH, 0x38B67, random.randint(0x05, 0x09)) # Dada jump height 3 (default 07)

    # Potton (entity ID 01)
    edit_nes_byte(GAME_PATH, 0x38B98, random.randint(0x00, 0x0E)) # Horizontal distance before Potton drops head (default 04)

    # New Shotman (entity ID 02)
    edit_nes_byte(GAME_PATH, 0x39DCC, random.randint(0x0E, 0x2E)) # Time until New Shotman first begins shooting (default 1E)
    edit_nes_byte(GAME_PATH, 0x39E29, random.randint(0x0E, 0x2E)) # Time until New Shotman begins shooting again after the first time (default 1E)
    edit_nes_byte(GAME_PATH, 0x39DDE, random.randint(0x30, 0x70)) # Distance for shooting arcing bullets (default 50)
    edit_nes_byte(GAME_PATH, 0x39E34, random.randint(0x01, 0x05)) # Times that New Shotman shoots before resetting pattern (default 03)
    edit_nes_byte(GAME_PATH, 0x39E38, random.randint(0x3A, 0x7A)) # Delay between bullets being shot during multi-shot volley (default 5A)
    edit_nes_byte(GAME_PATH, 0x39E8C, random.randint(0x01, 0x03)) # Speed of horizontal shots (default 01)
    #edit_nes_byte(GAME_PATH, 0x39E87, 0x80) # Minor speed adjustment for horizontal New Shotman shots (do not edit, causes issues) (default 80)
    edit_nes_byte(GAME_PATH, 0x39EC4, random.randint(0x02, 0x06)) # Height of arcing shots (default 04)
    #edit_nes_byte(GAME_PATH, 0x39EBF, 0x00) # Minor speed adjustment for height of arcing New Shotman shots (do not edit, causes issues) (default 00)

    # Hammer Joe (entity ID 03)
    edit_nes_byte(GAME_PATH, 0x38C18, random.randint(0x0E, 0x2E)) # Time before Hammer Joe throws hammer (default 1E)
    edit_nes_byte(GAME_PATH, 0x38CC6, random.randint(0x01, 0x05)) # Thrown hammer speed (default 03)
    edit_nes_byte(GAME_PATH, 0x38CC1, random.randint(0x01, 0xFF)) # Minor speed adjustment for thrown hammer speed (default 33)
    edit_nes_byte(GAME_PATH, 0x38CDA, random.randint(0x01, 0x03)) # HP of thrown hammer (default 01)

    # Bubukan (entity ID 04)

    # Needle obstacle (entity IDs 22 and 23)
    edit_nes_byte(GAME_PATH, 0x3B352, random.randint(0x10, 0x2A)) # Length of time that needle obstacles are extended for (default 1E)

    # Top Man top platforms (entity ID 27)
    edit_nes_byte(GAME_PATH, 0x3B259, random.choice([0x01, 0x02])) # Vertical speed, any setting higher than 2 makes it almost impossible to cross in Top Man's stage (default 01)


def scramble_enemy_weakness_tables():
# Scrambles the amount of damage that each special weapon does to the enemies in the game. The buster's table is not altered in this.

    for i in range(0x14210, 0x14A10):
        if i > 0x14610 and i < 0x14710: # This is specifically for Top Spin; in the base game it either kills a normal enemy in one hit or is completely ineffective, so we will preserve the idea here
            edit_nes_byte(GAME_PATH, i, random.choice([0x00, 0x0A]))
        else:
            edit_nes_byte(GAME_PATH, i, random.choice([0x00, 0x00, 0x01, 0x01, 0x02, 0x02, 0x06, 0x0A]))


def randomize_needle_man_boss():
# Randomizes Needle Man's boss attributes.

    edit_nes_byte(GAME_PATH, 0x88A6, random.randint(0x02, 0x06)) # Speed of Needle Man's needles (default 04)
    edit_nes_byte(GAME_PATH, 0xC0C9, random.randint(0x01, 0x02)) # Related to number of needles are shot per round? (default 01)
    edit_nes_byte(GAME_PATH, 0xC0F9, random.randint(0x0B, 0x16)) # This value governs how Needle Man moves in the air. The lower the value, the longer he stays in the air and shoots needles (default 10)
    # edit_nes_byte(GAME_PATH, 0xC19F, 0x01) # Related to jump height (default 01)
    edit_nes_byte(GAME_PATH, 0xC1B0, random.randint(0x04, 0x07)) # Related to jump height (default 06)
    edit_nes_byte(GAME_PATH, 0xC1B1, random.randint(0x07, 0x0A)) # Related to jump height (default 09)
    edit_nes_byte(GAME_PATH, 0xC1B8, random.randint(0x05, 0x07)) # Related to jump height (default 06)
    edit_nes_byte(GAME_PATH, 0xC1E2, random.randint(0x01, 0x03)) # Related to Needle Man's horizontal jump speed (default 02)
    edit_nes_byte(GAME_PATH, 0xC1E6, random.randint(0x01, 0x05)) # Related to Needle Man's horizontal jump speed (default 03)
    edit_nes_byte(GAME_PATH, 0xC1E7, random.randint(0x01, 0x03)) # Related to Needle Man's horizontal jump speed (default 02)


def randomize_magnet_man_boss():
# Randomizes Magnet Man's boss attributes.

    edit_nes_byte(GAME_PATH, 0xC2D1, random.randint(0x03, 0x05)) # Delay time between each jump (default 04)
    edit_nes_byte(GAME_PATH, 0xC30F, random.randint(0xA0, 0xF0)) # Timer for Magnet Man's pulling phase (default F0)
    edit_nes_byte(GAME_PATH, 0xC34C, random.randint(0x02, 0x0A)) # Delay time between Magnet Missiles being fired (default 06)
    edit_nes_byte(GAME_PATH, 0xC366, random.randint(0x01, 0x06)) # Number of Magnet Missiles used before falling back to the ground (default 03)
    edit_nes_byte(GAME_PATH, 0xC381, random.randint(0x03, 0x09)) # Gravity after firing Magnet Missile (default 06)
    edit_nes_byte(GAME_PATH, 0xC42C, random.randint(0x02, 0x06)) # First jump height (default 04)
    edit_nes_byte(GAME_PATH, 0xC42D, random.randint(0x04, 0x08)) # Second jump height (default 06)
    edit_nes_byte(GAME_PATH, 0xC42F, random.randint(0xA3, 0xC8)) # Horizontal distance Magnet Man travels with each jump? (default B3)
    edit_nes_byte(GAME_PATH, 0xC432, random.randint(0x00, 0x02)) # Also related to horizontal jumping distance? (default 01)
    edit_nes_byte(GAME_PATH, 0xC433, random.randint(0x01, 0x04)) # Also related to horizontal jumping distance? (default 02)
    edit_nes_byte(GAME_PATH, 0xC469, random.randint(0x02, 0x06)) # Speed of Magnet Missile (default 04)


def randomize_gemini_man_boss():
# Randomizes Gemini Man's boss attributes.

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


def randomize_hard_man_boss():
# Randomizes Hard Man's boss attributes.

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


def randomize_top_man_boss():
# Randomizes Top Man's boss attributes.

    edit_nes_byte(GAME_PATH, 0xC57D, random.randint(0x28, 0x88)) # Time until Top Man starts spinning after shooting (default 78)
    edit_nes_byte(GAME_PATH, 0xC593, random.randint(0xC0, 0xF0)) # How far Top Man goes to the right before stopping (default D0)
    edit_nes_byte(GAME_PATH, 0xC5A0, random.randint(0x10, 0x40)) # How far Top Man goes to the left before stopping (default 30)
    edit_nes_byte(GAME_PATH, 0xC5EF, random.randint(0x09, 0x13)) # Where tops originate from (default 0E)
    edit_nes_byte(GAME_PATH, 0xC602, random.randint(0x02, 0x07)) # Speed of thrown tops (default 04)
    edit_nes_byte(GAME_PATH, 0xC67D, random.randint(0x03, 0x07)) # Impacts speed of thrown tops (default 05)


def randomize_snake_man_boss():
# Randomizes Snake Man's boss attributes.

    edit_nes_byte(GAME_PATH, 0xA8A4, random.randint(0x01, 0x04)) # Speed of snakes that Snake Man shoots (default 02)
    edit_nes_byte(GAME_PATH, 0xE610, random.randint(0x0A, 0x1F)) # Time until Snake Man moves after shooting Search Snake (default 1A)
    edit_nes_byte(GAME_PATH, 0xE64F, random.randint(0x08, 0x24)) # Number of snakes Snake Man shoots, or some timer related to it? (default 14)
    edit_nes_byte(GAME_PATH, 0xE66F, random.randint(0x01, 0x05)) # Height of snakes shot? (default 03)
    edit_nes_byte(GAME_PATH, 0xE6BC, random.randint(0x05, 0x07)) # Snake Man jump height setting; lower settings seem to cause him to get stuck (default 05)
    edit_nes_byte(GAME_PATH, 0xE6BD, random.randint(0x06, 0x09)) # Snake Man's jump height when shooting Search Snake (default 08)


def randomize_spark_man_boss():
# Randomizes Spark Man's boss attributes.

    edit_nes_byte(GAME_PATH, 0xE360, random.randint(0x04, 0x07)) # Spark Man's jump height (default 06)
    edit_nes_byte(GAME_PATH, 0xE393, random.randint(0x01, 0x05)) # Number of time Spark Man jumps before attacking (random, possibly determined in RAM?) (default 03)
    edit_nes_byte(GAME_PATH, 0xE396, random.randint(0x00, 0x02)) # Related to Spark Man's jump quantity (default 01)
    # edit_nes_byte(GAME_PATH, 0xE3BE, 0x21) # Some value related to jumping settings (default 21)
    # edit_nes_byte(GAME_PATH, 0xE3C3, 0x20) # Value related to jumping settings (default 20)
    edit_nes_byte(GAME_PATH, 0xE415, random.randint(0x44, 0x67)) # Time that Spark Man waits after firing the large spark, seems to screw with the large spark attack if edited (default 64)
    # edit_nes_byte(GAME_PATH, 0xE440, 0x07) # Number of sparks Spark Man shoots? Better not to edit (default 07)
    # edit_nes_byte(GAME_PATH, 0xE469, 0x00) # Related to small sparks (default 00)
    edit_nes_byte(GAME_PATH, 0xE4C7, random.randint(0x01, 0x04)) # Speed of large spark (default 02)
    # edit_nes_byte(GAME_PATH, 0xE4E9, 0x99) # 0xE4E7 - E4FE # Jumping settings (default 99)
    # edit_nes_byte(GAME_PATH, 0xE4ED, 0x0E) # 0xE4E7 - E4FE # Jumping settings (default 0E)
    # edit_nes_byte(GAME_PATH, 0xE4F0, 0x80) # 0xE4E7 - E4FE # Jumping settings (default 80)
    edit_nes_byte(GAME_PATH, 0xE50B, random.randint(0x00, 0x02)) # 0xE50B - E513 # Messes with small sparks (default 00)
    edit_nes_byte(GAME_PATH, 0xE50C, random.randint(0x01, 0x03)) # 0xE50B - E513 # Messes with small sparks (default 01)
    edit_nes_byte(GAME_PATH, 0xE50D, random.randint(0x01, 0x03)) # 0xE50B - E513 # Messes with small sparks (default 02)
    edit_nes_byte(GAME_PATH, 0xE50E, random.randint(0x01, 0x03)) # 0xE50B - E513 # Messes with small sparks (default 01)
    edit_nes_byte(GAME_PATH, 0xE50F, random.randint(0x00, 0x02)) # 0xE50B - E513 # Messes with small sparks (default 00)
    edit_nes_byte(GAME_PATH, 0xE510, random.randint(0x00, 0x03)) # 0xE50B - E513 # Messes with small sparks (default 01)
    edit_nes_byte(GAME_PATH, 0xE511, random.randint(0x01, 0x03)) # 0xE50B - E513 # Messes with small sparks (default 02)
    edit_nes_byte(GAME_PATH, 0xE512, random.randint(0x01, 0x03)) # 0xE50B - E513 # Messes with small sparks (default 01)
    edit_nes_byte(GAME_PATH, 0xE513, random.randint(0x00, 0x02)) # 0xE50B - E513 # Messes with small sparks (default 00)


def randomize_shadow_man_boss():
# Randomizes Shadow Man's boss attributes.

    edit_nes_byte(GAME_PATH, 0xC6D1, random.randint(0x60, 0xA0)) # Influences how far Shadow Man moves forward during jump (default 80)
    edit_nes_byte(GAME_PATH, 0xC6D6, random.randint(0x00, 0x01)) # Influences how far Shadow Man moves forward during jump (default 00)
    edit_nes_byte(GAME_PATH, 0xC70C, random.randint(0x02, 0x08)) # Delay time for jumping after landing (default 04)
    edit_nes_byte(GAME_PATH, 0xC71D, random.randint(0x01, 0x05)) # Number of times Shadow Man will jump until shooting Shadow Blade (default 03)
    edit_nes_byte(GAME_PATH, 0xC79C, random.randint(0x02, 0x06)) # Sliding speed (default 04)
    edit_nes_byte(GAME_PATH, 0xC7BA, random.randint(0x08, 0x2A)) # Delay for how long Shadow Man holds up arm before throwing Shadow Blades (default 14)
    edit_nes_byte(GAME_PATH, 0xC87C, random.randint(0x03, 0x05)) # 0xC87C - C883 Jumping settings (default 04)
    edit_nes_byte(GAME_PATH, 0xC87D, random.randint(0x05, 0x07)) # 0xC87C - C883 Jumping settings (default 06)
    edit_nes_byte(GAME_PATH, 0xC87E, random.randint(0x07, 0x09)) # 0xC87C - C883 Jumping settings (default 08)
    edit_nes_byte(GAME_PATH, 0xC87F, random.randint(0x05, 0x07)) # 0xC87C - C883 Jumping settings (default 06)
    edit_nes_byte(GAME_PATH, 0xC880, random.randint(0x00, 0x01)) # 0xC87C - C883 Jumping settings (default 00)              
    edit_nes_byte(GAME_PATH, 0xC881, random.randint(0x00, 0x02)) # 0xC87C - C883 Jumping settings (default 01)
    edit_nes_byte(GAME_PATH, 0xC882, random.randint(0x00, 0x01)) # 0xC87C - C883 Jumping settings (default 00)
    edit_nes_byte(GAME_PATH, 0xC883, random.randint(0x00, 0x02)) # 0xC87C - C883 Jumping settings (default 01)
    edit_nes_byte(GAME_PATH, 0xC8ED, random.randint(0x01, 0x05)) # Speed of top Shadow Blade (default 03)
    edit_nes_byte(GAME_PATH, 0xC8EF, random.randint(0x02, 0x06)) # Speed of bottom Shadow Blade (default 04)


def randomize_doc_metal_boss():
# Randomizes Doc Metal's boss attributes.

    edit_nes_byte(GAME_PATH, 0x86FD, random.randint(0x84, 0xC4)) # Delay time for Doc Metal throwing the Metal Blade when the battle starts (default B4)
    edit_nes_byte(GAME_PATH, 0x873A, random.randint(0x84, 0xC4)) # Delay time for Doc Metal throwing the Metal Blade after the first time (default B4)
    edit_nes_byte(GAME_PATH, 0x8729, random.randint(0x06, 0x09)) # Jumping height when Doc Metal jumps to the other side of the room (default 08)
    edit_nes_byte(GAME_PATH, 0x8789, random.randint(0x05, 0x09)) # Delay time between Metal Blades being thrown (default 07)
    edit_nes_byte(GAME_PATH, 0x8853, random.randint(0x05, 0x09)) # Jumping height setting (default 08)
    edit_nes_byte(GAME_PATH, 0x8854, random.randint(0x01, 0x07)) # Jumping height setting (default 04)
    edit_nes_byte(GAME_PATH, 0x8855, random.randint(0x03, 0x09)) # Jumping height setting (default 06)
    edit_nes_byte(GAME_PATH, 0x8856, random.randint(0x07, 0x0D)) # Gravity setting (default 0A)
    edit_nes_byte(GAME_PATH, 0x8857, random.randint(0x05, 0x0B)) # Gravity setting (default 08)
    edit_nes_byte(GAME_PATH, 0x8858, random.randint(0x0A, 0x0F)) # Gravity setting (default 0D)
    edit_nes_byte(GAME_PATH, 0x8859, random.randint(0x07, 0x0D)) # Gravity setting (default 0A)
    edit_nes_byte(GAME_PATH, 0x88A6, random.randint(0x03, 0x07)) # Speed of Metal Blades (default 05)


def randomize_doc_air_boss():
# Randomizes Doc Air's boss attributes.

    edit_nes_byte(GAME_PATH, 0xA5B7, random.randint(0x01, 0x05)) # Number of times Doc Air shoots before jumping (default 03)
    edit_nes_byte(GAME_PATH, 0xA5D6, random.randint(0x76, 0xB6)) # Delay timer for when Doc Air shoots tornados after the first volley (default 96)
    edit_nes_byte(GAME_PATH, 0xA68D, random.randint(0xC4, 0xCC)) # X position where Doc Air lands on the ground on the right side (default C8)
    edit_nes_byte(GAME_PATH, 0xA691, random.randint(0x38, 0x3C)) # X position where Doc Air lands on the ground on the left side (default 38)
    edit_nes_byte(GAME_PATH, 0xA6CB, random.randint(0x00, 0x10)) # Air Shooter speed setting (default 00)
    edit_nes_byte(GAME_PATH, 0xA6D7, random.randint(0x00, 0x10)) # Air Shooter speed setting (default 10)
    edit_nes_byte(GAME_PATH, 0xA6DF, random.randint(0x00, 0x10)) # Air Shooter speed setting (default 00)
    edit_nes_byte(GAME_PATH, 0xA6ED, random.randint(0x00, 0x10)) # Air Shooter speed setting (default 00)
    edit_nes_byte(GAME_PATH, 0xA705, random.randint(0x03, 0x07)) # Doc Air jump height 1 (default 05)
    edit_nes_byte(GAME_PATH, 0xA706, random.randint(0x06, 0x0A)) # Doc Air jump height 2 (default 08)
    edit_nes_byte(GAME_PATH, 0xA707, random.randint(0x4A, 0x8A)) # Doc Air jump horizontal velocity 1 (default 6A)
    edit_nes_byte(GAME_PATH, 0xA708, random.randint(0xBA, 0xFA)) # Doc Air jump horizontal velocity 2 (default DA)

    # All of the following is related to tornados
    edit_nes_byte(GAME_PATH, 0xA70B, random.randint(0x40, 0x4F)) # Delay timer for tornados (default 44)
    edit_nes_byte(GAME_PATH, 0xA70C, random.randint(0x40, 0x4F)) # Delay timer for tornados (default 4A)
    edit_nes_byte(GAME_PATH, 0xA70D, random.randint(0x40, 0x4F)) # Delay timer for tornados (default 42)
    edit_nes_byte(GAME_PATH, 0xA70E, random.randint(0x40, 0x4F)) # Delay timer for tornados (default 43)
    edit_nes_byte(GAME_PATH, 0xA70F, random.randint(0x40, 0x4F)) # Delay timer for tornados (default 43)
    edit_nes_byte(GAME_PATH, 0xA710, random.randint(0x00, 0xFF)) # Y position for tornados (default 00)
    edit_nes_byte(GAME_PATH, 0xA711, random.randint(0x00, 0xFF)) # Y position for tornados (default F0)
    edit_nes_byte(GAME_PATH, 0xA712, random.randint(0x00, 0xFF)) # Y position for tornados (default 50)
    edit_nes_byte(GAME_PATH, 0xA713, random.randint(0x00, 0xFF)) # Y position for tornados (default 3C)
    edit_nes_byte(GAME_PATH, 0xA714, random.randint(0x00, 0xFF)) # Y position for tornados (default 00)
    edit_nes_byte(GAME_PATH, 0xA715, random.randint(0x00, 0xFF)) # Y position for tornados (default 00)
    edit_nes_byte(GAME_PATH, 0xA721, random.randint(0x00, 0xFF)) # Y position for tornados (default A7)
    edit_nes_byte(GAME_PATH, 0xA722, random.randint(0x00, 0xFF)) # Y position for tornados (default 88)
    edit_nes_byte(GAME_PATH, 0xA723, random.randint(0x00, 0xFF)) # Y position for tornados (default 50)
    edit_nes_byte(GAME_PATH, 0xA724, random.randint(0x00, 0xFF)) # Y position for tornados (default D4)
    edit_nes_byte(GAME_PATH, 0xA725, random.randint(0x00, 0xFF)) # Y position for tornados (default D0)
    edit_nes_byte(GAME_PATH, 0xA726, random.randint(0x00, 0xFF)) # Y position for tornados (default D0)
    edit_nes_byte(GAME_PATH, 0xA727, random.randint(0x00, 0xFF)) # Y position for tornados (default B9)
    edit_nes_byte(GAME_PATH, 0xA72E, random.randint(0x00, 0x04)) # Speed setting for tornados (default 04)
    edit_nes_byte(GAME_PATH, 0xA72F, random.randint(0x00, 0x04)) # Speed setting for tornados (default 03)
    edit_nes_byte(GAME_PATH, 0xA730, random.randint(0x00, 0x04)) # Speed setting for tornados (default 03)
    edit_nes_byte(GAME_PATH, 0xA731, random.randint(0x00, 0x04)) # Speed setting for tornados (default 02)
    edit_nes_byte(GAME_PATH, 0xA732, random.randint(0x00, 0x04)) # Speed setting for tornados (default 02)
    edit_nes_byte(GAME_PATH, 0xA733, random.randint(0x00, 0x04)) # Speed setting for tornados (default 00)
    edit_nes_byte(GAME_PATH, 0xA734, random.randint(0x00, 0x04)) # Speed setting for tornados (default 03)
    edit_nes_byte(GAME_PATH, 0xA735, random.randint(0x00, 0x04)) # Speed setting for tornados (default 03)
    edit_nes_byte(GAME_PATH, 0xA736, random.randint(0x00, 0x04)) # Speed setting for tornados (default 02)
    edit_nes_byte(GAME_PATH, 0xA737, random.randint(0x00, 0x04)) # Speed setting for tornados (default 02)
    edit_nes_byte(GAME_PATH, 0xA738, random.randint(0x00, 0x04)) # Speed setting for tornados (default 01)
    edit_nes_byte(GAME_PATH, 0xA739, random.randint(0x00, 0x04)) # Speed setting for tornados (default 00)
    edit_nes_byte(GAME_PATH, 0xA73A, random.randint(0x00, 0x04)) # Speed setting for tornados (default 03)
    edit_nes_byte(GAME_PATH, 0xA73B, random.randint(0x00, 0x04)) # Speed setting for tornados (default 02)
    edit_nes_byte(GAME_PATH, 0xA73C, random.randint(0x00, 0x04)) # Speed setting for tornados (default 02)
    edit_nes_byte(GAME_PATH, 0xA73D, random.randint(0x00, 0x04)) # Speed setting for tornados (default 01)
    edit_nes_byte(GAME_PATH, 0xA73E, random.randint(0x00, 0x04)) # Speed setting for tornados (default 00)
    edit_nes_byte(GAME_PATH, 0xA73F, random.randint(0x00, 0x04)) # Speed setting for tornados (default FF)
    edit_nes_byte(GAME_PATH, 0xA740, random.randint(0x00, 0x04)) # Speed setting for tornados (default 03)
    edit_nes_byte(GAME_PATH, 0xA741, random.randint(0x00, 0x04)) # Speed setting for tornados (default 03)
    edit_nes_byte(GAME_PATH, 0xA742, random.randint(0x00, 0x04)) # Speed setting for tornados (default 02)
    edit_nes_byte(GAME_PATH, 0xA743, random.randint(0x00, 0x04)) # Speed setting for tornados (default 01)
    edit_nes_byte(GAME_PATH, 0xA744, random.randint(0x00, 0x04)) # Speed setting for tornados (default 01)
    edit_nes_byte(GAME_PATH, 0xA745, random.randint(0x00, 0x04)) # Speed setting for tornados (default FF)
    edit_nes_byte(GAME_PATH, 0xA746, random.randint(0x00, 0x04)) # Speed setting for tornados (default 03)
    edit_nes_byte(GAME_PATH, 0xA747, random.randint(0x00, 0x04)) # Speed setting for tornados (default 03)
    edit_nes_byte(GAME_PATH, 0xA748, random.randint(0x00, 0x04)) # Speed setting for tornados (default 02)
    edit_nes_byte(GAME_PATH, 0xA749, random.randint(0x00, 0x04)) # Speed setting for tornados (default 01)
    edit_nes_byte(GAME_PATH, 0xA74A, random.randint(0x00, 0x04)) # Speed setting for tornados (default 00)
    edit_nes_byte(GAME_PATH, 0xA74B, random.randint(0x00, 0x04)) # Speed setting for tornados (default 00)
    edit_nes_byte(GAME_PATH, 0xA74C, random.randint(0x00, 0x04)) # Speed setting for tornados (default 00)
    edit_nes_byte(GAME_PATH, 0xA74D, random.randint(0x00, 0xFF)) # X position for tornados (default B1)
    edit_nes_byte(GAME_PATH, 0xA74E, random.randint(0x00, 0xFF)) # X position for tornados (default 3C)
    edit_nes_byte(GAME_PATH, 0xA74F, random.randint(0x00, 0xFF)) # X position for tornados (default 50)
    edit_nes_byte(GAME_PATH, 0xA750, random.randint(0x00, 0xFF)) # X position for tornados (default 76)
    edit_nes_byte(GAME_PATH, 0xA751, random.randint(0x00, 0xFF)) # X position for tornados (default 00)
    edit_nes_byte(GAME_PATH, 0xA752, random.randint(0x00, 0xFF)) # X position for tornados (default 2B)
    edit_nes_byte(GAME_PATH, 0xA753, random.randint(0x00, 0xFF)) # X position for tornados (default 3C)
    edit_nes_byte(GAME_PATH, 0xA754, random.randint(0x00, 0xFF)) # X position for tornados (default 31)
    edit_nes_byte(GAME_PATH, 0xA755, random.randint(0x00, 0xFF)) # X position for tornados (default 6B)
    edit_nes_byte(GAME_PATH, 0xA756, random.randint(0x00, 0xFF)) # X position for tornados (default DB)
    edit_nes_byte(GAME_PATH, 0xA757, random.randint(0x00, 0xFF)) # X position for tornados (default 00)
    edit_nes_byte(GAME_PATH, 0xA758, random.randint(0x00, 0xFF)) # X position for tornados (default A0)
    edit_nes_byte(GAME_PATH, 0xA759, random.randint(0x00, 0xFF)) # X position for tornados (default 31)
    edit_nes_byte(GAME_PATH, 0xA75A, random.randint(0x00, 0xFF)) # X position for tornados (default 76)
    edit_nes_byte(GAME_PATH, 0xA75B, random.randint(0x00, 0xFF)) # X position for tornados (default B5)
    edit_nes_byte(GAME_PATH, 0xA75C, random.randint(0x00, 0xFF)) # X position for tornados (default F0)
    edit_nes_byte(GAME_PATH, 0xA75D, random.randint(0x00, 0xFF)) # X position for tornados (default FC)
    edit_nes_byte(GAME_PATH, 0xA75E, random.randint(0x00, 0xFF)) # X position for tornados (default E0)
    edit_nes_byte(GAME_PATH, 0xA75F, random.randint(0x00, 0xFF)) # X position for tornados (default 3C)
    edit_nes_byte(GAME_PATH, 0xA760, random.randint(0x00, 0xFF)) # X position for tornados (default D4)
    edit_nes_byte(GAME_PATH, 0xA761, random.randint(0x00, 0xFF)) # X position for tornados (default 90)
    edit_nes_byte(GAME_PATH, 0xA762, random.randint(0x00, 0xFF)) # X position for tornados (default 90)
    edit_nes_byte(GAME_PATH, 0xA763, random.randint(0x00, 0xFF)) # X position for tornados (default FD)
    edit_nes_byte(GAME_PATH, 0xA764, random.randint(0x00, 0xFF)) # X position for tornados (default C0)
    edit_nes_byte(GAME_PATH, 0xA765, random.randint(0x00, 0xFF)) # X position for tornados (default 3C)
    edit_nes_byte(GAME_PATH, 0xA766, random.randint(0x00, 0xFF)) # X position for tornados (default 50)
    edit_nes_byte(GAME_PATH, 0xA767, random.randint(0x00, 0xFF)) # X position for tornados (default DB)
    edit_nes_byte(GAME_PATH, 0xA768, random.randint(0x00, 0xFF)) # X position for tornados (default F8)
    edit_nes_byte(GAME_PATH, 0xA769, random.randint(0x00, 0xFF)) # X position for tornados (default FE)
    edit_nes_byte(GAME_PATH, 0xA76A, random.randint(0x00, 0x04)) # More speed settings for tornados (default 00)
    edit_nes_byte(GAME_PATH, 0xA76B, random.randint(0x00, 0x04)) # More speed settings for tornados (default 00)
    edit_nes_byte(GAME_PATH, 0xA76C, random.randint(0x00, 0x04)) # More speed settings for tornados (default 02)
    edit_nes_byte(GAME_PATH, 0xA76D, random.randint(0x00, 0x04)) # More speed settings for tornados (default 03)
    edit_nes_byte(GAME_PATH, 0xA76E, random.randint(0x00, 0x04)) # More speed settings for tornados (default 03)
    edit_nes_byte(GAME_PATH, 0xA76F, random.randint(0x00, 0x04)) # More speed settings for tornados (default 04)
    edit_nes_byte(GAME_PATH, 0xA770, random.randint(0x00, 0x04)) # More speed settings for tornados (default 01)
    edit_nes_byte(GAME_PATH, 0xA771, random.randint(0x00, 0x04)) # More speed settings for tornados (default 01)
    edit_nes_byte(GAME_PATH, 0xA772, random.randint(0x00, 0x04)) # More speed settings for tornados (default 03)
    edit_nes_byte(GAME_PATH, 0xA773, random.randint(0x00, 0x04)) # More speed settings for tornados (default 03)
    edit_nes_byte(GAME_PATH, 0xA774, random.randint(0x00, 0x04)) # More speed settings for tornados (default 03)
    edit_nes_byte(GAME_PATH, 0xA775, random.randint(0x00, 0x04)) # More speed settings for tornados (default 04)
    edit_nes_byte(GAME_PATH, 0xA776, random.randint(0x00, 0x04)) # More speed settings for tornados (default 01)
    edit_nes_byte(GAME_PATH, 0xA777, random.randint(0x00, 0x04)) # More speed settings for tornados (default 03)
    edit_nes_byte(GAME_PATH, 0xA778, random.randint(0x00, 0x04)) # More speed settings for tornados (default 03)
    edit_nes_byte(GAME_PATH, 0xA779, random.randint(0x00, 0x04)) # More speed settings for tornados (default 03)
    edit_nes_byte(GAME_PATH, 0xA77A, random.randint(0x00, 0x04)) # More speed settings for tornados (default 03)
    edit_nes_byte(GAME_PATH, 0xA77B, random.randint(0x00, 0x04)) # More speed settings for tornados (default 03)
    edit_nes_byte(GAME_PATH, 0xA77C, random.randint(0x00, 0x04)) # More speed settings for tornados (default 01)
    edit_nes_byte(GAME_PATH, 0xA77D, random.randint(0x00, 0x04)) # More speed settings for tornados (default 02)
    edit_nes_byte(GAME_PATH, 0xA77E, random.randint(0x00, 0x04)) # More speed settings for tornados (default 02)
    edit_nes_byte(GAME_PATH, 0xA77F, random.randint(0x00, 0x04)) # More speed settings for tornados (default 03)
    edit_nes_byte(GAME_PATH, 0xA780, random.randint(0x00, 0x04)) # More speed settings for tornados (default 03)
    edit_nes_byte(GAME_PATH, 0xA781, random.randint(0x00, 0x04)) # More speed settings for tornados (default 03)
    edit_nes_byte(GAME_PATH, 0xA782, random.randint(0x00, 0x04)) # More speed settings for tornados (default 01)
    edit_nes_byte(GAME_PATH, 0xA783, random.randint(0x00, 0x04)) # More speed settings for tornados (default 02)
    edit_nes_byte(GAME_PATH, 0xA784, random.randint(0x00, 0x04)) # More speed settings for tornados (default 03)
    edit_nes_byte(GAME_PATH, 0xA785, random.randint(0x00, 0x04)) # More speed settings for tornados (default 03)
    edit_nes_byte(GAME_PATH, 0xA786, random.randint(0x00, 0x04)) # More speed settings for tornados (default 03)
    edit_nes_byte(GAME_PATH, 0xA787, random.randint(0x00, 0x04)) # More speed settings for tornados (default 03)


def randomize_doc_bubble_boss():
# Randomizes Doc Bubble's boss attributes.

    edit_nes_byte(GAME_PATH, 0xA216, random.randint(0x30, 0x50)) # How high Doc Bubble goes up before descending (default 50)
    edit_nes_byte(GAME_PATH, 0xA21F, random.randint(0x01, 0x02)) # Doc Bubble landing speed (default 01)
    # edit_nes_byte(GAME_PATH, 0xA236, 0x00) # Number of bubbles shot (default 00)
    edit_nes_byte(GAME_PATH, 0xA2DE, random.randint(0x01, 0x05)) # Number of bubbles shot (default 03)
    edit_nes_byte(GAME_PATH, 0xA2E8, random.randint(0x01, 0x03)) # Number of bubbles shot (default 02)          
    edit_nes_byte(GAME_PATH, 0xA2B1, random.randint(0x01, 0x02)) # Doc Bubble horizontal speed (default 01)
    edit_nes_byte(GAME_PATH, 0xA2D2, random.randint(0x03, 0x07)) # Number of bullets shot while Doc Bubble ascends (default 05)
    edit_nes_byte(GAME_PATH, 0xA35E, random.randint(0x03, 0x07)) # Initial jump height of bubbles (default 05)
    edit_nes_byte(GAME_PATH, 0xA383, random.randint(0x03, 0x07)) # Jump height of bubbles after initial launch (default 05)
    edit_nes_byte(GAME_PATH, 0xA362, random.randint(0x01, 0x03)) # Horizontal speed of bubbles (default 01)
    edit_nes_byte(GAME_PATH, 0xA363, random.randint(0x02, 0x06)) # Horizontal speed of bullets (default 04)
    edit_nes_byte(GAME_PATH, 0xA364, random.randint(0x0E, 0x2E)) # Delay time between bubbles being shot (default 1E)


def randomize_doc_quick_boss():
# Randomizes Doc Quick's boss attributes.

    edit_nes_byte(GAME_PATH, 0xA43B, random.randint(0x01, 0x05)) # Speed at which Doc Quick runs at you during running phase (default 02)
    edit_nes_byte(GAME_PATH, 0xA440, random.randint(0x2C, 0x4C)) # Length of Doc Quick's running phase (default 3C)
    edit_nes_byte(GAME_PATH, 0xA4AB, random.randint(0x01, 0x05)) # Number of boomerangs Doc Quick shoots (minus 1) (default 02)
    edit_nes_byte(GAME_PATH, 0xA4C8, random.randint(0x15, 0x35)) # Length of time before boomerangs halt after initially being shot (default 25)
    edit_nes_byte(GAME_PATH, 0xA544, random.randint(0x10, 0x2C)) # Length of time until boomerangs home in on the player after stopping initially (default 1F)
    edit_nes_byte(GAME_PATH, 0xA50B, random.randint(0x03, 0x09)) # Table for Doc Quick jump heights (A50B - A50E) (default 06)
    edit_nes_byte(GAME_PATH, 0xA50C, random.randint(0x05, 0x0A)) # Table for Doc Quick jump heights (A50B - A50E) (default 08)
    edit_nes_byte(GAME_PATH, 0xA50D, random.randint(0x06, 0x0A)) # Table for Doc Quick jump heights (A50B - A50E) (default 09)
    edit_nes_byte(GAME_PATH, 0xA50E, random.randint(0x05, 0x0A)) # Table for Doc Quick jump heights (A50B - A50E) (default 08)
    edit_nes_byte(GAME_PATH, 0xA513, random.randint(0x01, 0x05)) # Table for number of jumps Doc Quick will do before running (A513 - A518) (randomly decides between these) (default 03)
    edit_nes_byte(GAME_PATH, 0xA514, random.randint(0x01, 0x05)) # Table for number of jumps Doc Quick will do before running (A513 - A518) (randomly decides between these) (default 02)
    edit_nes_byte(GAME_PATH, 0xA515, random.randint(0x01, 0x05)) # Table for number of jumps Doc Quick will do before running (A513 - A518) (randomly decides between these) (default 02)
    edit_nes_byte(GAME_PATH, 0xA516, random.randint(0x01, 0x05)) # Table for number of jumps Doc Quick will do before running (A513 - A518) (randomly decides between these) (default 01)
    edit_nes_byte(GAME_PATH, 0xA517, random.randint(0x01, 0x05)) # Table for number of jumps Doc Quick will do before running (A513 - A518) (randomly decides between these) (default 01)
    edit_nes_byte(GAME_PATH, 0xA518, random.randint(0x01, 0x05)) # Table for number of jumps Doc Quick will do before running (A513 - A518) (randomly decides between these) (default 01)
    edit_nes_byte(GAME_PATH, 0xA52D, random.randint(0x02, 0x06)) # Speed of boomerangs (default 04)


def randomize_doc_crash_boss():
# Randomizes Doc Crash's boss attributes.

    edit_nes_byte(GAME_PATH, 0x84E0, random.randint(0xBC, 0xDC)) # Distance Doc Crash walks to the right side of the screen (default CC)
    edit_nes_byte(GAME_PATH, 0x84EF, random.randint(0x24, 0x44)) # Distance Doc Crash walks to the left side of the screen (default 34)
    edit_nes_byte(GAME_PATH, 0x8520, random.randint(0x76, 0xB6)) # Delay between Crash Bomb phases when fire button is not presssed (default 96) 
    edit_nes_byte(GAME_PATH, 0x855F, random.randint(0x01, 0x02)) # Doc Crash walk speed (default 01)
    edit_nes_byte(GAME_PATH, 0x85AF, random.randint(0x05, 0x09)) # Doc Crash jump height (default 07)
    edit_nes_byte(GAME_PATH, 0x85CD, random.randint(0x00, 0x02)) # Distance variable for Doc Crash's jump (default 01) 
    edit_nes_byte(GAME_PATH, 0x85CE, random.randint(0x00, 0x02)) # Distance variable for Doc Crash's jump (default 01)
    edit_nes_byte(GAME_PATH, 0x85CF, random.randint(0x00, 0x02)) # Distance variable for Doc Crash's jump (default 01)
    edit_nes_byte(GAME_PATH, 0x85D0, random.randint(0x01, 0x03)) # Distance variable for Doc Crash's jump (default 02)
    edit_nes_byte(GAME_PATH, 0x864B, random.randint(0x0E, 0x2E)) # Delay for Crash Bomb explosion (default 1E)
    edit_nes_byte(GAME_PATH, 0x8654, random.randint(0x02, 0x07)) # Speed of Crash Bomb (default 04)


def randomize_doc_flash_boss():
# Randomizes Doc Flash's boss attributes.    

    edit_nes_byte(GAME_PATH, 0x80A3, random.randint(0x03, 0x08)) # Jump height (default 04)
    edit_nes_byte(GAME_PATH, 0x80DB, random.randint(0x04, 0x0B)) # Delay between shots (default 08)
    edit_nes_byte(GAME_PATH, 0x80E9, random.randint(0x02, 0x0B)) # Number of shots fired (default 06)
    edit_nes_byte(GAME_PATH, 0x80F3, random.randint(0x30, 0x90)) # Delay between each usage of Time Stopper (default 60)


def randomize_doc_heat_boss():
# Randomizes Doc Heat's boss attributes.    
    
    edit_nes_byte(GAME_PATH, 0xA147, random.randint(0x01, 0x07)) # Number of fire projectiles shot; set this too high and the game becomes a laggy mess (minus 01) (default 02)
    edit_nes_byte(GAME_PATH, 0xA1B6, random.randint(0x0F, 0x5F)) # Doc Heat tackle delay 1 (default 1E)
    edit_nes_byte(GAME_PATH, 0xA1B7, random.randint(0x0F, 0x5F)) # Doc Heat tackle delay 2 (default 3C)
    edit_nes_byte(GAME_PATH, 0xA1B8, random.randint(0x0F, 0x5F)) # Doc Heat tackle delay 3 (default 5A)
    edit_nes_byte(GAME_PATH, 0xA1BE, random.randint(0x02, 0x06)) # Fire projectile 1 vertical speed (default 04)
    edit_nes_byte(GAME_PATH, 0xA1BF, random.randint(0x03, 0x09)) # Fire projectile 2 vertical speed (default 06)
    edit_nes_byte(GAME_PATH, 0xA1C0, random.randint(0x06, 0x0A)) # Fire projectile 3 vertical speed (default 08)
    edit_nes_byte(GAME_PATH, 0xA1C1, random.randint(0x14, 0x44)) # Fire projectile 1 horizontal speed (default 1C)
    edit_nes_byte(GAME_PATH, 0xA1C2, random.randint(0x14, 0x44)) # Fire projectile 2 horizontal speed (default 2A)
    edit_nes_byte(GAME_PATH, 0xA1C3, random.randint(0x14, 0x44)) # Fire projectile 3 horizontal speed (default 34)


def randomize_doc_wood_boss():
# Randomizes Doc Wood's boss attributes.    
    
    edit_nes_byte(GAME_PATH, 0x8285, random.randint(0x02, 0x08)) # Doc Wood initial jump height (default 04)
    edit_nes_byte(GAME_PATH, 0x8337, random.randint(0x02, 0x08)) # Doc Wood jump height after first time (default 04)
    edit_nes_byte(GAME_PATH, 0x8295, random.randint(0x0C, 0x17)) # Delay time for when small leaves appear (default 12)
    edit_nes_byte(GAME_PATH, 0x829A, random.randint(0x40, 0x90)) # Length of time Doc Wood stays open after throwing Leaf Shield (default 60)
    edit_nes_byte(GAME_PATH, 0x8379, random.randint(0x40, 0x90)) # Length of time Doc Wood stays open after throwing Leaf Shield after the first time (default 60)
    edit_nes_byte(GAME_PATH, 0x82E3, random.randint(0x08, 0x18)) # Related to length of time Doc Wood stays open after throwing Leaf Shield after the first time (default 0F)
    edit_nes_byte(GAME_PATH, 0x82A8, random.randint(0x0D, 0x17)) # Delay for falling leaves (default 12)
    edit_nes_byte(GAME_PATH, 0x82BA, random.randint(0x18, 0x3F)) # Delay time for how long falling leaves stay up before falling (default 2E)
    edit_nes_byte(GAME_PATH, 0x82D5, random.randint(0x10, 0x38)) # Delay time for Doc Wood throwing Leaf Shield after falling leaves begin to fall (default 24)
    edit_nes_byte(GAME_PATH, 0x83CC, random.randint(0x02, 0x06)) # Speed of thrown Leaf Shield (default 04)
    edit_nes_byte(GAME_PATH, 0x8430, random.randint(0x52, 0x72)) # Speed of falling leaves (default 62)
    edit_nes_byte(GAME_PATH, 0x8438, random.randint(0x01, 0x03)) # Speed of falling leaves (default 01)
    edit_nes_byte(GAME_PATH, 0x8459, random.randint(0x30, 0xE0)) # X position of falling leaf 1 (default 40)
    edit_nes_byte(GAME_PATH, 0x845A, random.randint(0x30, 0xE0)) # X position of falling leaf 2 (default 70)
    edit_nes_byte(GAME_PATH, 0x845B, random.randint(0x30, 0xE0)) # X position of falling leaf 3 (default A0)
    edit_nes_byte(GAME_PATH, 0x845C, random.randint(0x30, 0xE0)) # X position of falling leaf 4 (default D0)
    edit_nes_byte(GAME_PATH, 0x847D, random.randint(0x0A, 0x15)) # Controls leftwards sway of falling leaves (default 0F)
    edit_nes_byte(GAME_PATH, 0x84A5, random.randint(0x0A, 0x15)) # Controls rightwards sway of falling leaves (default 0F)


def randomize_kamegoro_maker_boss():
# Randomizes Kamegoro Maker's boss attributes.

    edit_nes_byte(GAME_PATH, 0x2578D, random.randint(0x02, 0x04)) # HP of individual turtles (default 03)
    edit_nes_byte(GAME_PATH, 0x257E2, random.randint(0x02, 0x05)) # Turtle speed 1 (default 00)
    edit_nes_byte(GAME_PATH, 0x257E3, random.randint(0x02, 0x05)) # Turtle speed 2 (default 01)
    edit_nes_byte(GAME_PATH, 0x257E4, random.randint(0x02, 0x05)) # Turtle speed 3 (default 01)
    edit_nes_byte(GAME_PATH, 0x257E5, random.randint(0x02, 0x05)) # Turtle speed 4 (default 02)
    edit_nes_byte(GAME_PATH, 0x257E6, random.randint(0x02, 0x05)) # Turtle speed 5 (default 03)
    edit_nes_byte(GAME_PATH, 0x257E7, random.randint(0x02, 0x05)) # Turtle speed 6 (default 04)
    edit_nes_byte(GAME_PATH, 0x257F3, random.randint(0x48, 0x98)) # Time before turtle removes shell (default 78)
    edit_nes_byte(GAME_PATH, 0x25814, int(read_nes_byte(GAME_PATH, 0x257F3), 16)) # Time before turtle removes shell (default 78)
    edit_nes_byte(GAME_PATH, 0x25A26, random.randint(0x01, 0x03)) # Health of turtle shell (default 01)
    edit_nes_byte(GAME_PATH, 0x25AF6, random.randint(0x1C, 0x4C)) # Time from appearance to start for water vortex (default 3C)
    edit_nes_byte(GAME_PATH, 0x25B36, random.randint(0x58, 0x88)) # Time between vortex telegraph and vortex emerging (default 78)
    edit_nes_byte(GAME_PATH, 0x25C10, random.randint(0x01, 0x04)) # Vortex speed (default 02)
    edit_nes_byte(GAME_PATH, 0x25C82, random.randint(0x01, 0x04)) # Speed at which Mega Man is moved by vortexes (default 02)


def randomize_yellow_devil_mkii_boss():
# Randomizes Yellow Devil MK-II's boss attributes.

    edit_nes_byte(GAME_PATH, 0x240A1, random.randint(0x7F, 0xFF)) # Time after entering the room until Yellow Devil MK-II starts appearing from the left (default FF)
    edit_nes_byte(GAME_PATH, 0x24105, random.choice([0x02, 0x04])) # Yellow Devil MK-II block speed; seems to cause issues with Yellow Devil MK-II building itself if the speed value is not a simiar factor to the default (default 04)
    edit_nes_byte(GAME_PATH, 0x24141, random.randint(0x01, 0x05)) # Number of times to shoot bullet on the left side (default 03)
    edit_nes_byte(GAME_PATH, 0x2435D, random.randint(0x01, 0x05)) # Number of times to shoot bullet on the right side (default 03)
    edit_nes_byte(GAME_PATH, 0x241BB, random.randint(0x02, 0x06)) # Bullet speed (default 04)
    edit_nes_byte(GAME_PATH, 0x241D4, random.randint(0x0A, 0x1F)) # Delay between bullet shots (default 15)
    edit_nes_byte(GAME_PATH, 0x241EA, random.randint(0x0F, 0x2C)) # Delay between last bullet and next block movement phase (default 1E)
    edit_nes_byte(GAME_PATH, 0x2444F, random.randint(0x22, 0x4C)) # Delay until bullets being shot on right side (default 3C)
    edit_nes_byte(GAME_PATH, 0x244FA, random.randint(0x03, 0x07)) # Bouncing block Y speed (default 04)
    edit_nes_byte(GAME_PATH, 0x244F5, random.randint(0x01, 0xFF)) # Minor adjustment for bouncing block Y speed (default A3)
    edit_nes_byte(GAME_PATH, 0x24504, random.randint(0x01, 0x02)) # Bouncing block X speed (default 01)
    edit_nes_byte(GAME_PATH, 0x244FF, random.randint(0x01, 0xFF)) # Minor adjustment for bouncing block X speed (default BD)

    # Block variables (do not touch, these are complicated); still trying to locate a way to change the order the block are sent in but it seems very challenging to coordinate
    #for i in range(0x245AD, 0x245C5): # X positions where pieces stop (coming from right side)?
        #edit_nes_byte(GAME_PATH, i, random.choice([0x58, 0x68, 0x78, 0x88, 0x98]))
    #for i in range(0x245C5, 0x245DD): # Y positions where pieces stop (coming from right side)?
        #edit_nes_byte(GAME_PATH, i, random.choice([0xA8]))
    #for i in range(0x245DD, 0x245F5): # X positions where pieces stop (coming from left side)
        #edit_nes_byte(GAME_PATH, i, random.choice([0x18, 0x28, 0x38, 0x48, 0x58]))
    #for i in range(0x245F5, 0x2460D): # Y positions where pieces stop (coming from left side)?
        #edit_nes_byte(GAME_PATH, i, random.choice([0xA8]))
    #for i in range(0x24611, 0x24628): # Affects block height... very hard to understand, seems to be related to drawing as it does not impact the actual height of block objects
        #edit_nes_byte(GAME_PATH, i, random.choice([0x22, 0x24, 0x26, 0x28, 0x2C, 0x30]))
    #for i in range(0x24629, 0x24640): # Affects block height... very hard to understand, seems to be related to drawing since this also does not impact the block object height
        #edit_nes_byte(GAME_PATH, i, random.choice([0x22, 0x24, 0x26, 0x28, 0x2C, 0x30]))

    '''
    # Some data visualization for the above (original values)
    98 58 88 98 68 78 88 58 68 88 78 68 78 98 58 78 68 58 98 78 88 88 68 58 # 0x245AD - 0x245C4: these Y values seem to always apply to the stopping points of individual block transition
    E8 E8 E8 D8 E8 E8 D8 D8 D8 C8 D8 C8 C8 B8 C8 B8 B8 B8 A8 A8 B8 A8 A8 A8 # 0x245C5 - 0x245DC: these X values are for the stopping point for first transition of blocks from the left to the right?
    18 18 18 28 18 18 28 28 28 38 28 38 38 48 38 48 48 48 58 58 48 58 58 58 # 0x245DD - 0x245F4: maybe this actually controls the block object height?
    A8 A8 A8 B8 A8 A8 B8 B8 B8 C8 B8 C8 C8 D8 C8 D8 D8 D8 E8 E8 D8 E8 E8 E8
    26 2C 26 28 28 2C 28 26 28 2C 26 2C 26 2C 2C 26 26 26 2C 24 26 28 26 00 # 0x24611 - 0x24628: related to drawn block locations?
    26 2C 22 2C 28 28 28 26 24 30 22 2C 22 30 28 26 26 22 2C 30 26 28 26 00 # 0x24629 - 0x24640: related to drawn block locations?
    '''

    # These values seem to control the drawn parts of the Yellow Devil, also not worth editing
    #yellow_devil_block_order = [0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F, 0x10, 0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17]
    #random.shuffle(yellow_devil_block_order)
    #for i in range(0x24641, 0x24659):
        #edit_nes_byte(GAME_PATH, i, yellow_devil_block_order[i - 0x24641])
    #random.shuffle(yellow_devil_block_order)
    #for i in range(0x24659, 0x24671):
        #edit_nes_byte(GAME_PATH, i, yellow_devil_block_order[i - 0x24659])


def randomize_holograph_mega_mans_boss():
# Randomizes Holograph Mega Mans' boss attributes.

    # Note that movement speed of the non-imposter is in the sprite speed table; 0x543 (default 01)
    pass


def scramble_boss_behaviors():
# Scrambles the AI for the bosses in the game.

    # Robot Masters
    randomize_needle_man_boss()
    randomize_magnet_man_boss()
    randomize_gemini_man_boss()
    randomize_hard_man_boss()
    randomize_top_man_boss()
    randomize_snake_man_boss()
    randomize_spark_man_boss()
    randomize_shadow_man_boss()

    # Doc Robots
    randomize_doc_metal_boss()
    randomize_doc_air_boss()
    randomize_doc_bubble_boss()
    randomize_doc_quick_boss()
    randomize_doc_crash_boss()
    randomize_doc_flash_boss()
    randomize_doc_heat_boss()
    randomize_doc_wood_boss()

    # Wily fortress bosses
    randomize_kamegoro_maker_boss()
    randomize_yellow_devil_mkii_boss()
    randomize_holograph_mega_mans_boss()
    

def assign_weaknesses(mode, *args):
# A helper function for assigning weaknesses to bosses; mode determines whether the weakness generation is for Robot Masters/Doc Robots or fortress bosses, *args is the table of damage values for weakness weapons since this varies 

    # Mode 1 is for the Robot Masters and Doc Robots
    if mode == 1:
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

        # Mega Man 3 Robot Masters and Doc Robots all have 2 weaknesses so let's preserve that in the randomization
        weaknesses_1 = [0, 1, 2, 3, 4, 5, 6, 7]
        random.shuffle(weaknesses_1)
        weaknesses_2 = [0, 1, 2, 3, 4, 5, 6, 7]
        random.shuffle(weaknesses_2)

        # This prevents a boss from being weak to the same weapon "twice" from the above randomization; shuffle weaknesses 2 list until no entries are in the same place in the lists
        overlapping_weaknesses = True
        while(overlapping_weaknesses):
            random.shuffle(weaknesses_2)
            weakness_overlap_counter = 0
            for i in range(len(weaknesses_1)):
                if weaknesses_1[i] != weaknesses_2[i]:
                    weakness_overlap_counter += 1
            if weakness_overlap_counter == 8:
                overlapping_weaknesses = False

        # These loops randomly set immunities, weaknesses and semi-weaknesses across the damage tables
        for i in range(len(effectiveness)):
            for j in range(i):
                effectiveness[i][j] = random.choice([0x00, 0x00, 0x01, 0x01, 0x01, 0x02])
            effectiveness[i][weaknesses_1[i]] = 0x04
            effectiveness[i][weaknesses_2[i]] = random.choice(args[0])

        # Return the generated effectiveness table
        return effectiveness

    # Otherwise do a different procedure for the fortress bosses
    else:
        # This table contains damage schemas for the fortress bosses; for now these tables are fairly similar to the originals but offer a little bit of randomness in terms of exact damage value
        effectiveness = [
        [0x05, 0x05, 0x02, 0x01, 0x01, 0x01, 0x01, 0x00], # Kamegoro Maker, give it a few different weakness options; exact damage values matter a bit less here since it's a on a per-turtle basis
        [random.randint(0x04, 0x07), 0x03, 0x01, 0x01, 0x01, 0x00, 0x00, 0x00], # Yellow Devil MK-II, change the primary weakness value around a little bit
        [random.randint(0x04, 0x07), random.randint(0x04, 0x07), 0x03, 0x02, 0x01, 0x01, 0x00, 0x00], # Holograph Mega Mans, they normally have two severe weaknesses so preserve that here    
        [random.randint(0x04, 0x07), random.randint(0x04, 0x07), 0x04, 0x02, 0x01, 0x00, 0x00, 0x00], # Wily Machine 3 phase 1; very weak to two things
        [random.randint(0x04, 0x07), 0x04, 0x02, 0x02, 0x01, 0x01, 0x00, 0x00], # Wily Machine 3 phase 2; very weak to one thing and relatively weak to another
        [random.randint(0x02, 0x04), 0x02, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00], # Gamma phase 1; only vulnerable to two weapons
        [0x02, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00] # Gamma phase 2; only vulnerable to two weapons
        ]

        # Shuffle those individual lists up
        for i in effectiveness:
            random.shuffle(i)

        # Return generated effectiveness table
        return effectiveness


def scramble_boss_weakness_tables():
# Scrambles the weaknesses of the bosses in the game. Damage tables are listed by weapon, which is how this list is structured. See the attached notes for more details on the enemy damage tables.
    
    # Run helper function to get a weakness table for Robot Masters
    robot_master_weaknesses = assign_weaknesses(1, [0x04, 0x04, 0x04, 0x05, 0x07, 0x07, 0x07, 0x07])
    doc_robot_weaknesses = assign_weaknesses(1, [0x04, 0x04, 0x04, 0x04, 0x04, 0x04, 0x07, 0x07])
    fortress_weaknesses = assign_weaknesses(2)
    
    # Two Robot Masters & Doc Robots take two damage from the Mega Buster. These tables randomly assign that property
    buster_weaknesses = [0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x02, 0x02]
    random.shuffle(buster_weaknesses)
    doc_buster_weaknesses = [0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x02, 0x02]
    random.shuffle(doc_buster_weaknesses)

    # Loop through and assign all weaknesses to Robot Masters and Doc Robots
    counter = 0
    for i in range(0x14100, 0x14A00, 0x100):
        if i == 0x14100: # This first segment is for the Mega Buster, which we want to make do only 1 or 2 damage to bosses. No boss should be immune to the Mega Buster
            # Doc Robots (yes these are first in memory interestingly)
            edit_nes_byte(GAME_PATH, i + 0xB0, buster_weaknesses[0]) # VS Doc Flash
            edit_nes_byte(GAME_PATH, i + 0xB1, buster_weaknesses[1]) # VS Doc Wood
            edit_nes_byte(GAME_PATH, i + 0xB2, buster_weaknesses[2]) # VS Doc Crash
            edit_nes_byte(GAME_PATH, i + 0xB3, buster_weaknesses[3]) # VS Doc Metal
            edit_nes_byte(GAME_PATH, i + 0xC0, buster_weaknesses[4]) # VS Doc Bubble
            edit_nes_byte(GAME_PATH, i + 0xC1, buster_weaknesses[5]) # VS Doc Heat
            edit_nes_byte(GAME_PATH, i + 0xC2, buster_weaknesses[6]) # VS Doc Quick
            edit_nes_byte(GAME_PATH, i + 0xC3, buster_weaknesses[7]) # VS Doc Air

            # Robot Masters
            edit_nes_byte(GAME_PATH, i + 0xD0, doc_buster_weaknesses[0]) # VS Needle Man
            edit_nes_byte(GAME_PATH, i + 0xD7, doc_buster_weaknesses[0]) # Also VS Needle Man but specifically for the head hammer extended state
            edit_nes_byte(GAME_PATH, i + 0xD1, doc_buster_weaknesses[1]) # VS Magnet Man
            edit_nes_byte(GAME_PATH, i + 0xD2, doc_buster_weaknesses[2]) # VS Top Man
            edit_nes_byte(GAME_PATH, i + 0xD3, doc_buster_weaknesses[3]) # VS Shadow Man
            edit_nes_byte(GAME_PATH, i + 0xD8, doc_buster_weaknesses[3]) # VS Shadow Man but specifically for the sliding state
            edit_nes_byte(GAME_PATH, i + 0xE0, doc_buster_weaknesses[4]) # VS Hard Man
            edit_nes_byte(GAME_PATH, i + 0xE2, doc_buster_weaknesses[5]) # VS Spark Man
            edit_nes_byte(GAME_PATH, i + 0xE4, doc_buster_weaknesses[6]) # VS Snake Man
            edit_nes_byte(GAME_PATH, i + 0xE6, doc_buster_weaknesses[7]) # VS Gemini Man
            edit_nes_byte(GAME_PATH, i + 0xE7, doc_buster_weaknesses[7]) # VS Gemini Man's clone (yes it has a separate damage table for some reason)
        
        else:
            # Doc Robots (yes these are first in memory interestingly)
            edit_nes_byte(GAME_PATH, i + 0xB0, doc_robot_weaknesses[counter][0]) # VS Doc Flash Man
            edit_nes_byte(GAME_PATH, i + 0xB1, doc_robot_weaknesses[counter][1]) # VS Doc Wood Man
            edit_nes_byte(GAME_PATH, i + 0xB2, doc_robot_weaknesses[counter][2]) # VS Doc Crash Man
            edit_nes_byte(GAME_PATH, i + 0xB3, doc_robot_weaknesses[counter][3]) # VS Doc Metal Man
            edit_nes_byte(GAME_PATH, i + 0xC0, doc_robot_weaknesses[counter][4]) # VS Doc Bubble Man
            edit_nes_byte(GAME_PATH, i + 0xC1, doc_robot_weaknesses[counter][5]) # VS Doc Heat Man
            edit_nes_byte(GAME_PATH, i + 0xC2, doc_robot_weaknesses[counter][6]) # VS Doc Quick Man
            edit_nes_byte(GAME_PATH, i + 0xC3, doc_robot_weaknesses[counter][7]) # VS Doc Air Man

            # Robot Masters
            edit_nes_byte(GAME_PATH, i + 0xD0, robot_master_weaknesses[counter][0]) # VS Needle Man
            edit_nes_byte(GAME_PATH, i + 0xD7, robot_master_weaknesses[counter][0]) # Also VS Needle Man but specifically for the head hammer extended state
            edit_nes_byte(GAME_PATH, i + 0xD1, robot_master_weaknesses[counter][1]) # VS Magnet Man
            edit_nes_byte(GAME_PATH, i + 0xD2, robot_master_weaknesses[counter][2]) # VS Top Man
            edit_nes_byte(GAME_PATH, i + 0xD3, robot_master_weaknesses[counter][3]) # VS Shadow Man
            edit_nes_byte(GAME_PATH, i + 0xD8, robot_master_weaknesses[counter][3]) # VS Shadow Man but specifically for the sliding state
            edit_nes_byte(GAME_PATH, i + 0xE0, robot_master_weaknesses[counter][4]) # VS Hard Man
            edit_nes_byte(GAME_PATH, i + 0xE2, robot_master_weaknesses[counter][5]) # VS Spark Man
            edit_nes_byte(GAME_PATH, i + 0xE4, robot_master_weaknesses[counter][6]) # VS Snake Man
            edit_nes_byte(GAME_PATH, i + 0xE6, robot_master_weaknesses[counter][7]) # VS Gemini Man
            edit_nes_byte(GAME_PATH, i + 0xE7, robot_master_weaknesses[counter][7]) # VS Gemini Man's clone (yes it has a separate damage table for some reason)

            # Wily Fortress bosses; these are arranged on a per-boss basis rather than by weapon for the previous bosses so the formatting is slightly different
            edit_nes_byte(GAME_PATH, i + 0x101, fortress_weaknesses[0][counter]) # VS Kamegoro Maker
            edit_nes_byte(GAME_PATH, i + 0xF0, fortress_weaknesses[1][counter]) # VS Yellow Devil MK-II
            edit_nes_byte(GAME_PATH, i + 0x105, fortress_weaknesses[2][counter]) # VS Holograph Mega Mans
            edit_nes_byte(GAME_PATH, i + 0xF5, fortress_weaknesses[3][counter]) # VS Wily Machine 3 phase 1
            edit_nes_byte(GAME_PATH, i + 0xF3, fortress_weaknesses[4][counter]) # VS Wily Machine 3 phase 2
            edit_nes_byte(GAME_PATH, i + 0xF8, fortress_weaknesses[5][counter]) # VS Gamma phase 1
            edit_nes_byte(GAME_PATH, i + 0xF9, fortress_weaknesses[6][counter]) # VS Gamma phase 2
            counter += 1 


def fix_scanline():
# Fixes the annoying scanline issue on the stage select. Yep, it's one byte.

    edit_nes_byte(GAME_PATH, 0x3C4E0, 0xCF)


def fix_softlocks():
# This removes the spots where the player can be softlocked by running out of energy for Rush Coil / Rush Jet.

    # Doc Gemini fix for the room with Poles where you can be softlocked if all Poles are killed and no energy is left for utilities; this moves an Electric Gabyoall into that room to die from
    replace_entities(0x12A76, 0x12E2F, 0x12E33, random.choice([0x03]))
    edit_nes_byte(GAME_PATH, 0x12B2F, 0x0D)
    edit_nes_byte(GAME_PATH, 0x12C2F, 0xA0)
    edit_nes_byte(GAME_PATH, 0x12D2F, 0x92)
    edit_nes_byte(GAME_PATH, 0x12E2F, 0x64)

    # Doc Gemini fix for midpoint; adds wheel
    edit_nes_byte(GAME_PATH, 0x12A7C, 0x27)
    edit_nes_byte(GAME_PATH, 0x12B34, 0x12)
    edit_nes_byte(GAME_PATH, 0x12C34, 0x37)
    edit_nes_byte(GAME_PATH, 0x12D34, 0x86)
    edit_nes_byte(GAME_PATH, 0x12E34, 0x58)

    # Doc Spark fix for beginning; adds wheel 
    edit_nes_byte(GAME_PATH, 0x14A70, 0x28)
    edit_nes_byte(GAME_PATH, 0x14C10, 0xAA)
    edit_nes_byte(GAME_PATH, 0x14D10, 0x86)
    edit_nes_byte(GAME_PATH, 0x14E10, 0x59)

    # Wily 3 fix for beginning; adds wheel
    edit_nes_byte(GAME_PATH, 0x1CA70, 0x28)
    edit_nes_byte(GAME_PATH, 0x1CC10, 0x47)
    edit_nes_byte(GAME_PATH, 0x1CD10, 0x8D)
    edit_nes_byte(GAME_PATH, 0x1CE10, 0x59)


def rebalance_difficulty():
# Makes some modifications to smooth out the difficulty curve of the game, especially when assets are randomized.

    # Nerf Doc Quick damage
    edit_nes_byte(GAME_PATH, 0x140C2, 0x06) # Doc Quick contact damage (default 08)

    # Nerf Doc Wood damage
    edit_nes_byte(GAME_PATH, 0x1404C, 0x04) # Leaf Shield damage (default 08)
    edit_nes_byte(GAME_PATH, 0x140B1, 0x06) # Doc Wood contact damage (default 08)
    edit_nes_byte(GAME_PATH, 0x140B9, 0x04) # Leaf Shield damage (default 08)


def activate_burst_chaser():
# Speeds up the game a bit by increasing Mega Man's speed, bullet speed, and a few other variables.

    edit_nes_byte(GAME_PATH, 0x3CD57, 0x03) # Mega Man's movement speed (default 01)
    edit_nes_byte(GAME_PATH, 0x3D166, 0x07) # Bullet speed (default 04)
    edit_nes_byte(GAME_PATH, 0x3D77D, 0x4C) # Invicibility time after taking damage (default 3C)
    edit_nes_byte(GAME_PATH, 0x3D3D5, 0x04) # Mega Man's sliding speed (default 02)
    edit_nes_byte(GAME_PATH, 0x3D4CC, 0x02) # Ladder climbing speed (default 01)
    edit_nes_byte(GAME_PATH, 0x3CFB8, 0x02) # Rush Jet vertical speed (default 01)


if __name__ == "__main__":
# Mix it all up! These are the core randomizer features; mix and match as you please
    
    # Title screen and stage select related
    scramble_title_screen_palette()
    scramble_stage_order() # not currently functional
    scramble_stage_select_palettes()
    scramble_robot_master_names()

    # Related to stages
    scramble_stage_palettes()
    scramble_music()

    # Related to special weapons
    scramble_weapon_locations()
    scramble_weapon_palettes()
    scramble_weapon_energy_costs()
    scramble_weapon_behaviors()

    # Related to enemies, gimmicks, and entities
    scramble_sprite_palettes()
    scramble_sprite_health()
    scramble_sprite_speed()
    scramble_miniboss_behaviors()
    scramble_stage_entities()
    scramble_entity_properties()
    scramble_enemy_weakness_tables()

    # Related to bosses
    scramble_boss_behaviors()
    scramble_boss_weakness_tables() # Make sure to scramble boss tables after enemy tables, otherwise the enemy scrambling will overwrite those memory values

    # Bonus stuff
    fix_scanline() # Disable if you want to preserve the annoying scanline issue on the stage select...?
    fix_softlocks() # Disable if you want to add the opportunity to be softlocked back into the game
    rebalance_difficulty() # Disable for harsher damage values, which might make a randomized playthrough much more challenging
    activate_burst_chaser() # Disable if not playing Burst Chaser mode