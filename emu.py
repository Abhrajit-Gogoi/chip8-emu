

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

class cpu (pyglet.window.Window)

    def initialise(self):
        self.clear()
        self.memory = [0]*4096
        self.display_buffer = [0]*64*32
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
                

    # clear screen function
    def _0zzz(self):
        extracted_op = self.opcode & 0xf0ff
        try:
            self.funcmap[extracted_op]()
        except:
            log(f"unknown instruction {self.opcode}")

    # the clear screen function
    def _0zz0(self):
        log("clearing screen...")
        self.display_buffer = [0]*64*32
        self.should_draw = True
    # return from subroutine
    def _0zze(self):
        log("return from subroutine")
        self.pc = self.stack.pop()


    #jump instruction
    def _1zzz(self):
        log("jumps to address NNN")
        self.pc = self.opcode & 0x0fff





    # =================================== FUNCMAP ========================================
    
    def func(self):
        self.funcmap = { 0x000: self._0zzz,
                        0x0e0: self._0zz0,
                        0x0ee: self._0zze
        }

