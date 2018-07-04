# Copyright (c) 2014 Adafruit Industries
# Author: Tony DiCola
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
import time

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

from Adafruit_LED_Backpack import Matrix8x8

time_delay = 0.2

def writeMessage(text):
	for letter in list(text):
		# First create an 8x8 1 bit color image.
		image = Image.new('1', (8, 8))

		# Then create a draw instance.
		draw = ImageDraw.Draw(image)
		draw.text((2, -2),    letter,  font=font, fill=255)
		
		# Draw the image on the display buffer.
		display.set_image(image)
		
		# Draw the buffer to the display hardware.
		display.write_display()
		
		time.sleep(wait)
		display.clear()

def animateMessage(text):
        
        # Create image the size of the message
        image = Image.new('1', (len(text)*8, 8))

        # Then create a draw instance.
        draw = ImageDraw.Draw(image)
        letterCnt = 0
        textSize = 0

        # Create an image of letters
        for letter in list(text):
            draw.text((2 + letterCnt * textSize, -2), letter,  font=font, fill=255)
            textSize = draw.textsize(letter, font=font)[0]
            letterCnt = letterCnt + 1
        
        # Create a scroll of images
        scroll = display.horizontal_scroll(image)
        
        # Display list of images
        display.animate(scroll,time_delay)

def drawCross():
	# First create an 8x8 1 bit color image.
	image = Image.new('1', (8, 8))
	
	# Then create a draw instance.
	draw = ImageDraw.Draw(image)
	
	# Draw a rectangle with colored outline
	draw.rectangle((0,0,7,7), outline=255, fill=0)
	
	# Draw an X with two lines.
	draw.line((1,1,6,6), fill=255)
	draw.line((1,6,6,1), fill=255)
	
	# Draw the image on the display buffer.
	display.set_image(image)
        
        scroll = display.horizontal_scroll(image)
        display.animate(scroll,time_delay)
	
	# Draw the buffer to the display hardware.
	display.write_display()


# Create display instance on default I2C address (0x70) and bus number.
display = Matrix8x8.Matrix8x8()

# Alternatively, create a display with a specific I2C address and/or bus.
# display = Matrix8x8.Matrix8x8(address=0x74, busnum=1)

font = ImageFont.load_default()

# Initialize the display. Must be called once before using the display.
display.begin()

animateMessage("SWIFT")
#writeMessage("54321")
#drawCross()
		
time.sleep(0.5)
		
display.clear()
display.write_display()

# See the SSD1306 library for more examples of using the Python Imaging Library
# such as drawing text: https://github.com/adafruit/Adafruit_Python_SSD1306
