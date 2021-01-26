import sys
import os
import re

#(absolute_dir_path, string) -> results
if len(sys.argv) < 3:
  print("Not enough arguments.")
  quit(1)
folder = sys.argv[1]
text = sys.argv[2].lower()

try:
  dest_dir = os.listdir(folder)
except Exception as ex:
  print(ex)
  quit(1)

os.chdir(folder)

html_list = [f for f in dest_dir if re.search(r"\b.html", f) is not None]
#print(html_list)

count = 0
for fname in html_list:
  text_file = open(fname, 'r')
  if text_file is None:
    print('Failed to open file {}'.format(fname))
    continue
  print(os.path.abspath(fname))
  html_text = text_file.read().lower()
  if html_text.rfind(text) != -1:
    print("[MATCH] {}".format(fname))
    count += 1
  text_file.close()
print("Total matches:", count)