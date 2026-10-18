# Chip 8 simulator

CHIP-8 is an interpreted programming language and virtual machine created in the mid-1970s by Joseph Weisbecker.

## Overview and History

• Origin: Designed by Joseph Weisbecker for the RCA 1802 microprocessor, running on early 8-bit microcomputers like the COSMAC VIP and Telmac 1800.
• Purpose: Built to use less memory than BASIC while remaining easier to write than native machine code.
• Emulator "Hello World": Implementing a CHIP-8 emulator is a classic starter project for learning computer emulation.

## System Specifications

• Memory: 4 KB (4,096 bytes) of addressable RAM, with programs starting at memory address 0x200 (512).
• Registers: Sixteen 8-bit general-purpose data registers (V0 through VF), where VF acts as a flag (such as a carry/borrow flag).
• Index Register: One 16-bit address register named I.
• Stack: A 16-level stack used for handling subroutine calls and returns.
• Timers: Two 8-bit registers (a delay timer and a sound timer) that decrement automatically at 60 Hz.
• Display: A 64 x 32 pixel monochrome screen (or 128 x 64 for Super-CHIP extensions) updated via XOR sprite drawing.
• Input: A 16-key hexadecimal keypad (arranged from 0 to F).
• Instruction Set: Around 35 two-byte opcodes stored in big-endian format.

## the blog:

https://omokute.blogspot.com/ 

## how to run:

- step-1: clone the repository:
    '''
    git clone https://github.com/Abhrajit-Gogoi/chip8-emu
    '''