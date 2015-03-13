#!/usr/bin/python

import time
import datetime
from Adafruit_LEDBackpack import LEDBackpack

# ===========================================================================
# 7-Segment Display
# ===========================================================================

# The colon row
COLON_ROW = 2  

# This class is meant to be used with the four-character, seven segment
# displays available from Adafruit

class SevenSegment:

   # Enum creator
   def enum(**enums):
      return type('Enum', (), enums)

   disp = None
 
   # Hexadecimal character lookup table (row 1 = 0..9, row 2 = A..F)
   digits = [ 0x3F, 0x06, 0x5B, 0x4F, 0x66, 0x6D, 0x7D, 0x07, 0x7F, 0x6F, \
                   0x77, 0x7C, 0x39, 0x5E, 0x79, 0x71 ] 

   # The parts of the colon
   ColonParts = enum(POINT                   = 0b00010000,
                     LEFT_COLON_FULL		 = 0b00001100,
                     LEFT_COLON_BOTTOM_POINT = 0b00001000,
                     LEFT_COLON_TOP_POINT    = 0b00000100,
                     RIGHT_COLON             = 0b00000010)

   # Constructor
   def __init__(self, address=0x70, debug=False):
      if (debug):
         print "Initializing a new instance of LEDBackpack at 0x%02X" % address
      self.disp = LEDBackpack(address=address, debug=debug)

   def writeDigitRaw(self, charNumber, value):
      "Sets a digit using the raw 16-bit value"
      if (charNumber > 7):
         return
      # Set the appropriate digit
      self.disp.setBufferRow(charNumber, value)

   def writeDigit(self, charNumber, value, dot=False):
      "Sets a single decimal or hexademical value (0..9 and A..F)"
      if (charNumber > 7):
         return
      if (value > 0xF):
         return
      # Set the appropriate digit
      self.disp.setBufferRow(charNumber, self.digits[value] | (dot << 7))

   def setColonRaw(self, state=True):
      "Enables or disables the colon character"
      # General for 7segments
      # Warning: This function assumes that the colon is character '2',
      # which is the case on 4 char displays, but may need to be modified
      # if another display type is used
      if (state):
         self.disp.setBufferRow(COLON_ROW, 0xFFFF)
      else:
         self.disp.setBufferRow(COLON_ROW, 0)

   def setColon(self, colonPart=ColonParts.RIGHT_COLON, state=True):
      "Enables or disables a specific colon character"
      # Specific for 7Segment model Luckylight L1311094A
      #                   					   KW4-12041CLA
      # and backpack model Adafruit HT16K33
	  # (Not tested on any other model)
	  # colonPart should be called as SevenSegment.ColonParts.PART_NAME
      if (state):
         self.disp.setBufferRow(COLON_ROW, self.disp.getBufferRow(COLON_ROW) | colonPart)
      else:
         self.disp.setBufferRow(COLON_ROW, self.disp.getBufferRow(COLON_ROW) & ~colonPart)
