#!/usr/bin/env python
#
# Script queries the CPU usage, temperature and RAM usage and 
# displays the results visually using the 8x8 LED attached to the pi.

from __future__ import division
from subprocess import PIPE, Popen
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

from Adafruit_LED_Backpack import Matrix8x8

import time
import psutil

# Constants
time_delay = 0.2
max_temp_diff = 30.0
avg_temp = 55.0
max_pixel_index = 7
bar_width = 2
font = ImageFont.load_default()

# Create display instance on default I2C address (0x70) and bus number.
display = Matrix8x8.Matrix8x8()
# Alternatively, create a display with a specific I2C address and/or bus.
# display = Matrix8x8.Matrix8x8(address=0x74, busnum=1)

# Writes a message of text to the display
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
		
		time.sleep(time_delay)
		display.clear()

# Creates a scrolling message of text
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

# Draws a cross on the display
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
	
	# Draw the buffer to the display hardware.
	display.write_display()

# Draws a bar on the display with a width
def drawBar(loc_x, bar_height, draw):
    # Can't draw line of height 0 with a width of two, so draw some pixels instead
    if bar_height == 0:
        draw.point([loc_x, 0, loc_x + 1, 0], fill=255)
    else:
        # Draw a line with a given height and width.
        draw.line((loc_x,0,loc_x,bar_height), fill=255, width = bar_width)

# Gets the CPU temperature using vcgencmd
def get_cpu_temperature():
    process = Popen(['vcgencmd', 'measure_temp'], stdout=PIPE)
    output, _error = process.communicate()
    return float(output[output.index('=') + 1:output.rindex("'")])

# Plots the CPU usage, temperature and RAM usage to the 8x8 LED display
def plotStats():

    # Get each stat.
    cpu_temp = get_cpu_temperature()
    cpu_usage = psutil.cpu_percent()
    ram_usage = psutil.virtual_memory().percent
    
    # Convert each stat into a bar height
    temp_bar_height = int(abs(cpu_temp - avg_temp) / max_temp_diff * max_pixel_index)
    cpu_bar_height = int(cpu_usage / 100.0 * max_pixel_index)
    ram_bar_height = int(ram_usage / 100.0 * max_pixel_index)
    
    # First create an 8x8 1 bit color image.
    image = Image.new('1', (8, 8))
    
    # Then create a draw instance.
    draw = ImageDraw.Draw(image)

    # Draw each stat as a bar on the display.
    drawBar(1,temp_bar_height,draw)
    drawBar(3,cpu_bar_height,draw)
    drawBar(5,ram_bar_height,draw)

    #print "CPU temp: %f" % cpu_temp
    #print "CPU usage: %f" % cpu_usage
    #print "RAM usage: %f" % ram_usage

    # Draw the image on the display buffer.
    display.set_image(image)
    
    # Draw the buffer to the display hardware.
    display.write_display()

def main():

    # Initialize the display. Must be called once before using the display.
    display.begin()
  
    # Loop forever and update the display periodically
    while(1):
        plotStats()
        time.sleep(0.1)

    display.clear()
    display.write_display()

if __name__ == '__main__':
    main()

# See the SSD1306 library for more examples of using the Python Imaging Library
# such as drawing text: https://github.com/adafruit/Adafruit_Python_SSD1306
