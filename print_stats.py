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
def get_cpu_temperature():
    process = Popen(['vcgencmd', 'measure_temp'], stdout=PIPE)
    output, _error = process.communicate()
    return float(output[output.index('=') + 1:output.rindex("'")])

def main():

    max_temp = 85.0

    #while(1):
        #print "CPU temp: %f\r" % get_cpu_temperature(),
        #print "CPU usage: %f\r" % psutil.cpu_percent()
        #print "CPU temp: %f, CPU usage: %f\r" % (get_cpu_temperature(), psutil.cpu_percent()),
        #print('CPU temp: '+str(get_cpu_temperature())+', CPU usage: '+str(psutil.cpu_percent()), end='\r')
    
    #ram = psutil.used_phymem()
    ram = psutil.virtual_memory()
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

    while(1):
        print "RAM usage: %f\r" % ram.percent,
        #print "CPU usage: %f\r" % psutil.cpu_percent()

    print "CPU temp: %f" % get_cpu_temperature()
    print "CPU usage: %f" % psutil.cpu_percent()
    print "RAM usage: %f" % ram.percent

if __name__ == '__main__':
    main()

# See the SSD1306 library for more examples of using the Python Imaging Library
# such as drawing text: https://github.com/adafruit/Adafruit_Python_SSD1306
