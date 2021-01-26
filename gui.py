import sys
import os
import re
import gi

gi.require_version("Gtk", "3.0")
gi.require_version('WebKit2', '4.0')
from gi.repository import Gtk, WebKit2, Gdk

class Handler:
  def onDestroy(self, *args):
    Gtk.main_quit()
  def onSearch(self, *args):
    text = entry.get_text()
    if len(text) == 0 or text.count(' ') == len(text):
      return
    print("Trying to search '{}'...".format(text))
  
  def entryKeyPress(self, widget, ev, data=None):
    if ev.keyval == 65293 or ev.keyval == Gdk.KEY_KP_Enter:
      print('Enter')
      self.onSearch()

def fillList(listbox):
  for i in range(10):
    row = Gtk.ListBoxRow()
    hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)

    btest = Gtk.Button.new_with_label("Test {}".format(i))
    blabel = Gtk.Label.new("Some text {}".format(i))
    blabel.set_halign(Gtk.Align.START)
    hbox.pack_start(btest, False, True, 0)
    hbox.pack_end(blabel, True, True, 0)
    row.add(hbox)
    listbox.add(row)


builder = Gtk.Builder()
builder.add_from_file("ui.glade")
builder.connect_signals(Handler())
window = builder.get_object("window")
scroll = builder.get_object("scroll")
entry = builder.get_object("entrySearch")
paned = builder.get_object("paned")
paned.set_position(int(window.get_size()[0] * 0.3))
webview = WebKit2.WebView()
webview.load_uri('file:///home/yukatan/Документы/universiada database/_task1.html')
scroll.add(webview)
listbox = builder.get_object("listbox")
fillList(listbox)
btest2 = Gtk.Button.new_with_label("Test2")
blabel2 = Gtk.Label.new("Some text 2")

window.show_all()
Gtk.main()