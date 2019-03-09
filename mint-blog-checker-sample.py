#!/usr/bin/env python

# Copyright 2019 Scott Caudle
#
#    This file is part of mint-blog-checker-sample.
#
#    mint-blog-checker-sample is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    mint-blog-checker-sample is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with mint-blog-checker-sample.  If not, see <https://www.gnu.org/licenses/>.


import gtk
import subprocess
import glib


class BlogCheckerThingy():

    global icon

    def __init__(self):
        self.icon = gtk.StatusIcon()
        self.set_icon_off()
        self.icon.connect('popup-menu', self.on_right_click)
        self.icon.connect('activate', self.on_left_click)
        self.check_blog_for_newrss()
        #6 hour timer
        glib.timeout_add_seconds(21600, self.check_blog_for_newrss)

    def open_blog(self, data=None):
        self.set_icon_off()
        subprocess.call(['xdg-open', "https://blog.linuxmint.com/"])

    def close_app(self, data=None):
        gtk.main_quit()

    def make_menu(self, event_button, event_time, data=None):
        menu = gtk.Menu()
        open_item = gtk.MenuItem("View Blog")
        close_item = gtk.MenuItem("Close App")

        #Append the menu items  
        menu.append(open_item)
        menu.append(close_item)
        #add callbacks
        open_item.connect_object("activate", self.open_blog, "Open App")
        close_item.connect_object("activate", self.close_app, "Close App")
        #Show the menu items
        open_item.show()
        close_item.show()

        #Popup the menu
        menu.popup(None, None, None, event_button, event_time)

    def on_right_click(self, data, event_button, event_time):
        self.make_menu(event_button, event_time)

    def on_left_click(self, event):
        self.open_blog()

    def compare_time_from_parsed_blog_file(self):
        #check oldtime file
        with open('oldtime', 'r') as oldtime:
            old = oldtime.read()

        #open new time file
        with open('time', 'r') as time:
            new = time.read()

        #compare times
        #if they are different there is new blog entry
        if new != old:
            from shutil import copyfile
            copyfile("time", "oldtime")
            return True #to turn on blog-on icon
        #else they are the same then nothing new
        else:
            return False

    def check_blog_for_newrss(self):

        subprocess.call(['sh', "get-blog-time"])
        if self.compare_time_from_parsed_blog_file():
            self.set_icon_on()
        return True #restart timeout again

    def set_icon_on(self):
        self.icon.set_from_file("rss-on.png")
        self.icon.set_title("on")

    def set_icon_off(self):
        self.icon.set_from_file("rss-off.png")
        self.icon.set_title("off")

test3 = BlogCheckerThingy()
gtk.main()


