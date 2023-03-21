from rich import print

# The following is the sequence of events that occurs when a key is pressed on the Enigma machine:
# 1. The key is pressed
# Before the key is sent to the rotors, the rightmost rotor is rotated
# If the rightmost rotor completes a full rotation, the rotor to its left is rotated
# If the rightmost rotor completes a full rotation and the rotor to its left completes a full rotation, the rotor to its left is rotated
# 2. The key is sent to the plugboard
# The plugboard is a set of wires that can be used to swap letters
# 3. The key is sent to each rotor in order
# The rotors scramble the key
# 4. The key is sent to the reflector
# The reflector is a set of wires that can be used to swap letters, similar to the plugboard
# 5. The key is sent back through the rotors in reverse order

# 6. The key is sent to the plugboard
# 7. The key is sent to the lampboard
# The seventh step is the only step that is visible to the user

# Each rotor has 26 positions
# One for each letter of the alphabet
rotor_positions = []
PLUGBOARD = []
# On the Model C Enigma Machine, the one that was solved by Hut 8, there were 2 reflector positions
# One for each letter of the alphabet
# Unlike the rotors, the reflector does not rotate
reflector_position = 0

# Based on the UKW rotor, introduced in 1941
ROTOR_WIRING = [
    ("A", "Q"),
    ("B", "Y"),
    ("C", "H"),
    ("D", "O"),
    ("E", "G"),
    ("F", "N"),
    ("G", "E"),
    ("H", "C"),
    ("I", "V"),
    ("J", "P"),
    ("K", "U"),
    ("L", "Z"),
    ("M", "T"),
    ("N", "F"),
    ("O", "D"),
    ("P", "J"),
    ("Q", "A"),
    ("R", "X"),
    ("S", "W"),
    ("T", "M"),
    ("U", "K"),
    ("V", "I"),
    ("W", "S"),
    ("X", "R"),
    ("Y", "B"),
    ("Z", "L")
]

REFLECTOR_WIRING_A = [
    ("A", "E"),
    ("B", "J"),
    ("C", "M"),
    ("D", "Z"),
    ("E", "A"),
    ("F", "L"),
    ("G", "Y"),
    ("H", "X"),
    ("I", "V"),
    ("J", "B"),
    ("K", "W"),
    ("L", "F"),
    ("M", "C"),
    ("N", "R"),
    ("O", "Q"),
    ("P", "U"),
    ("Q", "O"),
    ("R", "N"),
    ("S", "T"),
    ("T", "S"),
    ("U", "P"),
    ("V", "I"),
    ("W", "K"),
    ("X", "H"),
    ("Y", "G"),
    ("Z", "D")
]

REFLECTOR_WIRING_B = [
    ("A", "Y"),
    ("B", "R"),
    ("C", "U"),
    ("D", "H"),
    ("E", "Q"),
    ("F", "S"),
    ("G", "L"),
    ("H", "D"),
    ("I", "P"),
    ("J", "X"),
    ("K", "N"),
    ("L", "G"),
    ("M", "O"),
    ("N", "K"),
    ("O", "M"),
    ("P", "I"),
    ("Q", "E"),
    ("R", "B"),
    ("S", "F"),
    ("T", "Z"),
    ("U", "C"),
    ("V", "W"),
    ("W", "V"),
    ("X", "J"),
    ("Y", "A"),
    ("Z", "T")
]

def importConfig():
    config_desired = input("Would you like to import a configuration? (Y/N): ")
    if config_desired.upper() != "Y": return False
    config = input("Please input your configuration: ")
    config = config.split(":")
    if len(config) != 3:
        print("Invalid configuration")
        return
    rotors = config[0]
    if len(rotors) != 3 and len(rotors) != 4:
        print("Invalid configuration")
        return
    for i in range(len(rotors)):
        rotor_positions.append(ord(rotors[i]) - 65)
    plugboard = config[1]
    if len(plugboard) % 2 != 0:
        print("Invalid configuration")
        return
    for i in range(0, len(plugboard), 2):
        PLUGBOARD.append((plugboard[i], plugboard[i + 1]))
    reflector = config[2]
    if len(reflector) != 1:
        print("Invalid configuration")
        return
    reflector_position = ord(reflector) - 65

    return True

def config():


    def setRotorsNum():
        rotors = input("How many rotors do you want to use? (3 or 4): ")
        if (rotors != "3" and rotors != "4"):
            print("Please enter a valid number of rotors")
            return setRotorsNum()

        return int(rotors)


    def setRotorPosition(index):
        rotor_setting = input("Enter the starting position of rotor " + str(i + 1) + ": ")
        if (not rotor_setting.isalpha() or len(rotor_setting) != 1):
            print("Please enter a valid starting position")
            return setRotorPosition(index)
        
        rotor_positions.append(ord(rotor_setting) - 65)

    num_rotors = setRotorsNum()
    for i in range(num_rotors):
        setRotorPosition(i)

    def setPlugboardLen():
        _len = input("How many plugboard wires do you want to plug in? (1 - 13): ")
        if (not _len.isnumeric() or int(_len) < 0 or int(_len) > 13):
            print("Please enter a valid number of plugboard wires")
            return setPlugboardLen()
        
        return int(_len)

    def setPlugboard(index, num_rotors = setPlugboardLen()):
        if (index == num_rotors):
            return

        wire_input = input("Enter the two letters you want to swap.\nType PREV to go to the previous entry and NEXT to go to the next entry: ")
        
        match wire_input:
            case "PREV":
                if (index == 0):
                    print("You are already on the first entry")
                    setPlugboard(index)
                    return
                setPlugboard(index - 1)
            case "NEXT":
                if (index == num_rotors - 1):
                    print("You are already on the last entry")
                    setPlugboard(index)
                    return
                setPlugboard(index + 1)
            case _:
                if (not wire_input.isalpha() or len(wire_input) != 2):
                    print("Please enter a valid pair of letters")
                    setPlugboard(index)
                    return
                
                wire_input = wire_input.upper()

                # Because we need to know both the letters and the order in which they are swapped, we need to use a list of tuples
                wire = (
                    wire_input[0],
                    wire_input[1]
                )

                PLUGBOARD.append(wire)
                print()
                setPlugboard(index + 1)

    setPlugboard(0)

    def setReflectorPosition():
        reflector_setting = input("Enter the starting position of the reflector (1 or 2): ")
        
        match reflector_setting:
            case "1":
                reflector_position = 0
            case "2":
                reflector_position = 1
            case _:
                print("Please enter a valid starting position")
                setReflectorPosition()
                return


    setReflectorPosition()

    def createConfigString():
        config_string = ""
        for i in range(num_rotors):
            config_string += chr(rotor_positions[i] + 65)
        config_string += ":"
        for i in range(num_rotors):
            config_string += chr(rotor_positions[i] + 65)
        config_string += ":"
        for i in range(len(PLUGBOARD)):
            config_string += PLUGBOARD[i][0] + PLUGBOARD[i][1]
        config_string += ":"
        config_string += str(reflector_position + 1)
        return config_string

    # Log the settings of the Enigma machine
    def logSettings():
        print(f"""


        [bold red]Enigma Settings:[/bold red]

        Number of rotors: [white on blue]{len(rotor_positions)}[/white on blue]
        Rotor positions: [white on blue]{rotor_positions}[/white on blue]

        Plugboard: [white on green]{PLUGBOARD}[/white on green]

        Reflector position: [white on red]{reflector_position + 1}[/white on red]

        Config: [white on yellow]{createConfigString()}[/white on yellow]
        """)
        print("Is this correct? (Y/N)")
        if (input().upper() == "Y"):
            return
        
        config()
    
    logSettings()

if not importConfig(): config()

def encrypt(message):
    def rotorMoveStep(rotor = 0):
        rotor_pos = rotor_positions[rotor]
        rotor_pos = rotor_pos + 1
        if (rotor_pos > 25):
            rotor_pos = 0
            rotorMoveStep(rotor + 1)
        rotor_positions[rotor] = rotor_pos
    
    def plugboardStep(key):
        for i in range(0, len(PLUGBOARD)):
            if (PLUGBOARD[i][0] == key):
                return PLUGBOARD[i][1]
        return key
    
    def rotorWiringStep(key, rotor):
        offset = rotor_positions[rotor]

        index = ord(key) - 65 + offset
        if (index > 25):
            index = index - 26
        
        return ROTOR_WIRING[index][1]
    
    def rotorTransversalStep(key, backwards):
        if (backwards):
            for i in reversed(range(0, len(rotor_positions))):
                return rotorWiringStep(key, i)

        for i in range(0, len(rotor_positions)):
            return rotorWiringStep(key, i)
    
    def reflectorStep(key):
        wiring = REFLECTOR_WIRING_A if reflector_position == 0 else REFLECTOR_WIRING_B

        for i in range(0, len(wiring)):
            if (wiring[i][0] == key):
                return wiring[i][1]
        
        raise Exception("Invalid key")
    
    def encryptKey(key):
        rotorMoveStep()
        k0 = plugboardStep(key)
        k1 = rotorTransversalStep(k0, False)
        k2 = reflectorStep(k1)
        k3 = rotorTransversalStep(k2, True)
        k4 = plugboardStep(k3)
        return k4
    
    for i in range(0, len(message)):
        print(encryptKey(message[i]), end = "")

encrypt("HELLO")
