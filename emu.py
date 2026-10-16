

import itertools
import os
import pyglet
import random
import sys
import time

from pyglet.sprite import Sprite

KEY_MAP = {pyglet.window.key._1: 0x1,
           pyglet.window.key._2: 0x2,
           pyglet.window.key._3: 0x3,
           pyglet.window.key._4: 0xc,
           pyglet.window.key.Q: 0x4,
           pyglet.window.key.W: 0x5,
           pyglet.window.key.E: 0x6,
           pyglet.window.key.R: 0xd,
           pyglet.window.key.A: 0x7,
           pyglet.window.key.S: 0x8,
           pyglet.window.key.D: 0x9,
           pyglet.window.key.F: 0xe,
           pyglet.window.key.Z: 0xa,
           pyglet.window.key.X: 0,
           pyglet.window.key.C: 0xb,
           pyglet.window.key.V: 0xf
          }




logging = False

def log(str):
    if logging == True:
        print(str)

class cpu (pyglet.window.Window): # the start of the class ===============================================
    

    def initialise(self):
        self.clear()
        self.memory = [0]*4096
        self.display_buffer = [0]*64*32
        self.stack = []
        self.key_inputs = [0]*16
        self.opcode = 0
        self.index = 0
        self.gpio = [0]*16

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
            self.memory[i+0x200] = binary
            i+=1    





    # defining the cycle
    def cycle(self):
        # this turns the 2 nibbles memory into 4 nibbles by using bitwise or
        self.opcode = (self.memory[self.pc] << 8) | (self.memory[self.pc + 1])

        # this isolateds the second and the third nibble
        self.vx = (self.opcode & 0x0f00) >> 8
        self.vy = (self.opcode & 0x00f0) >> 4

        #after:
        self.pc +=2

        extracted_op = self.opcode & 0xf00
        try:
            self.funcmap[extracted_op]() # this calls the associated method
        except:
            print(f"unknown instruction: {self.opcode}")

        # delay timers
        if self.delay_timer > 0:
            self.delay_timer -= 1
        if self.sound_timer > 0:
            self.sound_timer -= 1
            if self.sound_timer == 0:
                # play a sound 
                print()
                

    # ======================================================== INSTRUCTIONS ===============================================================================
    # =====================================================================================================================================================

    # handles the 0x0ZZZ family
    def _0ZZZ(self):
        extracted_op = self.opcode & 0xf0ff
        try:
            self.funcmap[extracted_op]()
        except:
            log(f"unknown instruction {self.opcode}")

    # 1. the clear screen function
    def _0ZZ0(self):
        log("clearing screen...")
        self.display_buffer = [0]*64*32
        self.should_draw = True
        
    # return from subroutine
    def _0ZZE(self):
        log("return from subroutine")
        self.pc = self.stack.pop()

    #jump instruction
    def _1ZZZ(self):
        log("jumps to address NNN")
        self.pc = self.opcode & 0x0fff

    # 0x2NNN call addr
    def _2ZZZ(self):
        self.stack.append(self.pc)
        self.pc = self.opcode & 0x0fff

    # drawing character instruction
    def _FZ29(self):
        log("set index to point to a character")
        self.index = (5*(self.gpio[self.vx])) & 0xfff

    # the 0x3xNN instruction
    def _3ZZZ(self):
        if self.gpio[self.vx] == (self.opcode & 0x00ff):
            self.pc+=2

    # the 0x4XNN instruction
    def _4ZZZ(self):
        log("Skips the next instuction if vx is not equal to NN")
        if self.gpio[self.vx] != (self.opcode & 0x00ff):
            self.pc += 2

    # comparing instruction
    def _5ZZZ(self):
        log("skips if vx = vy")
        if self.gpio[self.vx] == self.gpio[self.vy]:
            self.pc +=2

    # 0x6xNN instruction
    def _6ZZZ(self):
        self.gpio[self.vx] = self.opcode & 0x00ff

    # 0x7xNN add
    def _7ZZZ(self):
        self.gpio[self.vx] += (self.opcode & 0x00ff)

    # vx = vy 
    def _8ZZZ(self):
        extracted_op = self.opcode & 0xf00f
        try:
            self.funcmap[extracted_op]()
        except:
            log(f"unknown instruction {self.opcode}")

    # 0x8NN0
    def _8ZZ0(self):
        self.gpio[self.vx] = self.gpio[self.vy]

    # 8nn1
    def _8ZZ1(self):
        self.gpio[self.vx] = self.gpio[self.vx] | self.gpio[self.vy]

    # 8nn2
    def _8ZZ2(self):
        self.gpio[self.vx] = self.gpio[self.vx] & self.gpio[self.vy]

    # 8nn3
    def _8ZZ3(self):
        self.gpio[self.vx] = self.gpio[self.vx] ^ self.gpio[self.vy]

    # 8nn4 
    def _8ZZ4(self):
        if self.gpio[self.vx]+self.gpio[self.vy] > 0xff:
            self.gpio[0xf] = 1
        else:
            self.gpio[0xf] =0
        self.gpio[self.vx] = 0xff & (self.gpio[self.vx] + self.gpio[self.vy])
        
    
    


    # THE DRAWING SPRITE INSTRUCTION
    def _DZZZ(self):
        log("Draw a sprite")
        self.gpio[0xf] = 0
        x = self.gpio[self.vx] & 0xff
        y = self.gpio[self.vy] & 0xff
        height = self.opcode & 0x000f
        row = 0
        while row < height:
            curr_row = self.memory[row + self.index]
            pixel_offset = 0
            while pixel_offset < 8:
                loc = x + pixel_offset + ((y + row) * 64)
                pixel_offset += 1
                if (y + row) >= 32 or (x + pixel_offset - 1) >= 64:
                    # ignore pixels outside the screen
                    continue
                mask = 1 << 8-pixel_offset
                curr_pixel = (curr_row & mask) >> (8-pixel_offset)
                self.display_buffer[loc] ^= curr_pixel
                if self.display_buffer[loc] == 0:
                    self.gpio[0xf] = 1
                else:
                    self.gpio[0xf] = 0
            row += 1
        self.should_draw = True


    # the actual draw function
    def draw(self):
        if not self.should_draw:
            return

        self.clear()
    
        # Use enumerate to get index and value simultaneously, 
        # filtering out zero values immediately.
        for i, val in enumerate(self.display_buffer):
            if val:
                # Pre-calculated integer division (//) ensures safe math
                self.pixel.blit((i % 64) * 10, 310 - ((i // 64) * 10))

        self.flip()
        self.should_draw = False






    def on_key_press(self, symbol, modifiers):
        log(f"key pressed: {symbol}")
        if symbol in KEY_MAP.keys():
            self.key_inputs[KEY_MAP[symbol]] =1
            if self.key_wait:
                self.key_wait = False
            else:
                super(cpu, self).on_key_press(symbol, modifiers)


    def on_key_release(self, symbol, modifiers):
        log("Key released: %r" % symbol)
        if symbol in KEY_MAP.keys():
            self.key_inputs[KEY_MAP[symbol]] = 0










    # =================================== FUNCMAP ========================================
    
    def __init__(self, *args, **kwargs):
        super(cpu, self).__init__(*args, **kwargs)
        self.funcmap = {0x0000: self._0ZZZ,
                        0x00e0: self._0ZZ0,
                        0x00ee: self._0ZZE,
                        0x1000: self._1ZZZ,
                        0x2000: self._2ZZZ,
                        0x3000: self._3ZZZ,
                        0x4000: self._4ZZZ,
                        0x5000: self._5ZZZ,
        }

