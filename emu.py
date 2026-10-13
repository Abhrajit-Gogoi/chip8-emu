import pyglet



class cpu (pyglet.window.Window)

def initialise(self):
    self.clear()
    self.memory = [0]*4096
    self.displaybuffer = [0]*64*32
    self.stack = []
    self.key_inputs = [0]*16
    self.opcode = 0
    self.index = 0

    self.delay_timer = 0 
    self.sound_timer = 0
    self.should_draw = False

    self.pc = 0x200

    i=0
    while i<80:
        # load 80-char fontset
        self.memory[i] = self.fonts[i]
        i += 1


# load rom function
def load_Rom(self, rom_path):
    log(f"Loading {rom_path}...")
    binary = open(rom_path, "rb").read()
    i=0
    while i<len(binary):
        self.memory[i+0x200] = ord(binary[i])
        i+=1



    