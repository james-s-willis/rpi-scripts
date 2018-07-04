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

from __future__ import division
#from __future__ import print_function
from subprocess import PIPE, Popen
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

from Adafruit_LED_Backpack import Matrix8x8

import time
import psutil

time_delay = 0.2
font = ImageFont.load_default()

# Create display instance on default I2C address (0x70) and bus number.
display = Matrix8x8.Matrix8x8()
# Alternatively, create a display with a specific I2C address and/or bus.
# display = Matrix8x8.Matrix8x8(address=0x74, busnum=1)

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
	
	# Draw the buffer to the display hardware.
	display.write_display()

def drawBar(loc_x, height):
    # First create an 8x8 1 bit color image.
    image = Image.new('1', (8, 8))
	
    # Then create a draw instance.
    draw = ImageDraw.Draw(image)

    # Draw an X with two lines.
    #draw.line((1,1,1,1 + height), fill=255, width = 2)
    draw.line((loc_x,0,loc_x,height), fill=255, width = 2)
    #draw.line((1,1,1,6), fill=255)
    
    # Draw the image on the display buffer.
    display.set_image(image)
    
    # Draw the buffer to the display hardware.
    display.write_display()

def get_cpu_temperature():
    process = Popen(['vcgencmd', 'measure_temp'], stdout=PIPE)
    output, _error = process.communicate()
    return float(output[output.index('=') + 1:output.rindex("'")])

def main():

    #max_temp = 85.0
    max_temp = 30.0

    #while(1):
        #print "CPU temp: %f\r" % get_cpu_temperature()
        #print "CPU usage: %f\r" % psutil.cpu_percent(),
        #print "CPU temp: %f, CPU usage: %f\r" % (get_cpu_temperature(), psutil.cpu_percent()),
        #print('CPU temp: '+str(get_cpu_temperature())+', CPU usage: '+str(psutil.cpu_percent()), end='\r')
    
    #ram = psutil.used_phymem()
    #ram_total = ram.total / 2**20       # MiB.
    #ram_used = ram.used / 2**20
    #ram_free = ram.free / 2**20
    #ram_percent_used = ram.percent
    #
    #disk = psutil.disk_usage('/')
    #disk_total = disk.total / 2**30     # GiB.
    #disk_used = disk.used / 2**30
    #disk_free = disk.free / 2**30
    #disk_percent_used = disk.percent
    ## 
    ## Print top five processes in terms of virtual memory usage.
    ## 
    #processes = sorted(
    #    ((p.get_memory_info().vms, p) for p in psutil.process_iter()),
    #    reverse=True
    #)
    #for virtual_memory, process in processes[:5]:
    #    print virtual_memory // 2**20, process.pid, process.name
    
    # Initialize the display. Must be called once before using the display.
    display.begin()
   
    while(1):
        barsize = int(abs(get_cpu_temperature() - 55.0) / max_temp * 7)
        print barsize
        drawBar(1,barsize)
        drawBar(3,barsize)

        #drawBar(get_cpu_temperature() / max_temp * 6)
        time.sleep(0.5)
    
    for i in range(0,6):
        drawBar(i)
        time.sleep(0.5)
    #animateMessage("SWIFT")
    #writeMessage("54321")
    #drawCross()
    		
    time.sleep(0.5)
    		
    display.clear()
    display.write_display()

if __name__ == '__main__':
    main()

# See the SSD1306 library for more examples of using the Python Imaging Library
# such as drawing text: https://github.com/adafruit/Adafruit_Python_SSD1306
