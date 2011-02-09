#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2009 Jérémie Decock (http://www.jdhp.org)

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.


# TODO :
# - save img
# - filters : black & white, gray, contrast, ...
# - read input streams instead files (to be used with a pipe from dd or cat)
# - ARROW_UP and ARROW_DOWN keys
# - Verify files with less than 512*3 bytes
# - Fix bug with empty (0 byte) files


import os, sys
import getopt
import pygtk
pygtk.require('2.0')
import gtk

program_name = 'binviewer'

def usage():
    print '''Usage : ./binviewer -f filename
    
    Create a graphical representation of a binary file.

    -f, --file
        the binary file to display
    '''

def destroy(widget):
    gtk.main_quit()

def main():
    # Parse options ###################
    filename = ''

    try:
        opts, args = getopt.getopt(sys.argv[1:], 'f:h', ["file=", "help"])
    except getopt.GetoptError, err:
        print str(err) # will print something like "option -x not recognized"
        usage()
        sys.exit(1)

    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit(0)
        elif o in ("-f", "--file"):
            filename = a
        else:
            assert False, "unhandled option"

    if filename == '':
        usage()
        sys.exit(2)

    # Create window ###################
    window = gtk.Window(gtk.WINDOW_TOPLEVEL)
    window.set_title(program_name + ' (' + filename + ')')
    window.set_default_size(640, 480)
    window.connect('destroy', destroy)
    window.maximize()

    # Scrolled window #################
    sw = gtk.ScrolledWindow()
    sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)
    window.add(sw)

    # Pixbuf ##########################
    fd     = open(filename, 'rb')
    data   = fd.read()
    fd.close()
    
    width          = 512
    bits_per_pixel = 3
    bytes          = len(data)
    height         = (bytes / (width * bits_per_pixel)) + 1
    bytes_to_fill  = width * height * bits_per_pixel - bytes
    data += '\xff' * bytes_to_fill # TODO use background color

    print 'bytes          : ', bytes
    print 'width (px)     : ', width
    print 'height (px)    : ', height
    print 'bits per pixel : ', bits_per_pixel
    print 'bytes to fill  : ', bytes_to_fill
    
    pixbuf = gtk.gdk.pixbuf_new_from_data(data, gtk.gdk.COLORSPACE_RGB, False, 8, width, height, 3 * width)

    # Image ###########################
    image = gtk.Image()
    image.set_from_pixbuf(pixbuf)
    sw.add_with_viewport(image)

    # Show all ########################
    image.show()
    sw.show()
    window.show()

    # GTK main loop ###################
    gtk.main()
    return 0

if __name__ == '__main__':
    main()
