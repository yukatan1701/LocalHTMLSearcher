import sys
import os
import re
import gi
import pathlib

gi.require_version("Gtk", "3.0")
gi.require_version('WebKit2', '4.0')
from gi.repository import Gtk, WebKit2, Gdk, Pango

# data = filename + link
class ListData:
  filename = None
  path = None
  def __init__(self, filename: str, path: str):
    self.filename = filename
    self.path = path

def findMatches(folder: str, text: str) -> list:
  try:
    dest_dir = os.listdir(folder)
  except Exception as ex:
    print(ex)
    quit(1)
  os.chdir(folder)
  html_list = [f for f in dest_dir if re.search(r"\b.html", f) is not None]
  mList = []
  for fname in html_list:
    text_file = open(fname, 'r')
    if text_file is None:
      print('Failed to open file {}'.format(fname))
      continue
    absPath = os.path.abspath(fname)
    #print(absPath)
    html_text = text_file.read().lower()
    if html_text.rfind(text) != -1:
      print("[MATCH] {}".format(fname))
      uri = pathlib.Path(absPath).as_uri()
      mList.append(ListData(fname, uri))
    text_file.close()
  return mList

class Handler:
  def __init__(self, parent):
    self.parent = parent

  def onDestroy(self, *args):
    Gtk.main_quit()

  def onSearch(self, *args):
    text = self.parent.entry.get_text()
    folder = self.parent.dirChooser.get_filename()
    if folder is None:
      return
    if len(text) == 0 or text.count(' ') == len(text):
      return
    print("Trying to search '{}'...".format(text))
    matchList = findMatches(folder, text)
    self.parent.updateListbox(matchList)
  
  def entryKeyPress(self, widget, ev, data=None):
    if ev.keyval == 65293 or ev.keyval == Gdk.KEY_KP_Enter:
      print('Enter')
      self.onSearch()

class Window:
  def __init__(self):
    self.builder = Gtk.Builder()
    self.builder.add_from_file("ui.glade")
    self.builder.connect_signals(Handler(self))
    self.window = self.builder.get_object("window")
    self.scroll = self.builder.get_object("scroll")
    self.entry = self.builder.get_object("entrySearch")
    self.paned = self.builder.get_object("paned")
    self.dirChooser = self.builder.get_object("dirChooser")
    self.paned.set_position(int(self.window.get_size()[0] * 0.3))
    self.webview = WebKit2.WebView()
    self.webview.load_uri('file:///home/yukatan/Документы/universiada database/_task1.html')
    self.scroll.add(self.webview)
    self.listbox = self.builder.get_object("listbox")
    self.fillList()

    self.dirChooser.set_filename('/home/yukatan/Документы/universiada database/')
    self.entry.set_text('коши')
    self.window.show_all()
    Gtk.main()

  def updateListbox(self, matches: list):
    print("Total matches:", len(matches))
    for row in self.listbox:
      self.listbox.remove(row)
    print("Listbox cleared.")
    for match in matches:
      print('meow')
      row = Gtk.ListBoxRow()
      hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=20)
      btest = Gtk.Label.new("<b>{}</b>".format(match.filename))
      blabel = Gtk.Label.new("{}".format(match.path))
      blabel.set_ellipsize(Pango.EllipsizeMode.START)
      btest.set_use_markup(True)
      blabel.set_halign(Gtk.Align.START)
      hbox.pack_start(btest, False, True, 0)
      hbox.pack_end(blabel, True, True, 0)
      row.add(hbox)
      self.listbox.add(row)
    self.listbox.show_all()
    print('updated.')

  def fillList(self):
    for i in range(10):
      row = Gtk.ListBoxRow()
      hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=20)
      btest = Gtk.Label.new("<b>Test {}</b>".format(i))
      blabel = Gtk.Label.new("Some text {}".format(i))
      btest.set_use_markup(True)
      blabel.set_halign(Gtk.Align.START)
      hbox.pack_start(btest, False, True, 0)
      hbox.pack_end(blabel, True, True, 0)
      row.add(hbox)
      self.listbox.add(row)

window = Window()