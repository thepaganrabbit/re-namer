import tkinter as tk
from tkinter import filedialog

root = tk.Tk()

root.geometry('1140x480')

fr_url = ''
to_url = ''

title = tk.Label(root, text="Image Renamer", font=('Courier', 24))
title.grid(row=1, column=1, columnspan=6)

# FROM INPUT

from_label = tk.Label(root, text="From", font=('Courier', 14))
from_label.grid(row=2, column=1)

def get_from_url(event=None):
    fr_url = fr_input.get()
    print(fr_url)

# Handle button press to get path vie dialog
def open_from_file_dialog():
    fr_url = filedialog.askdirectory()
    fr_input.insert(0,fr_url)
    print(fr_url)


fr_input = tk.Entry(root, width=40)
fr_input.grid(row=2, column=2, columnspan=3)

# handle enter button for submission
fr_input.bind("<Return>", get_from_url)

btn_fr = tk.Button(root, text="GET", command=open_from_file_dialog)
btn_fr.grid(row=2, column=5)

# TO INPUT

def get_to_url(event=None):
    to_url = to_input.get()
    print(to_url)

# Handle button press to get path vie dialog
def open_to_file_dialog():
    to_url = filedialog.askdirectory()
    to_input.insert(0,to_url)
    print(to_url)

to_label = tk.Label(root, text="To", font=('Courier', 14))
to_label.grid(row=2, column=7)

to_input = tk.Entry(root, width=40)
to_input.grid(row=2, column=8, columnspan=3)

btn_to = tk.Button(root, text="GET", command=open_to_file_dialog)
btn_to.grid(row=2, column=11)

# write URLS to file 
def write_urls():
    with open('./paths.json', 'a') as writer:
        if len(fr_url) > 0 and len(to_url) > 0:
            data = {
                "from_path": fr_url,
                "to_path": to_url
            }
            writer.write(data)
        else:
            writer.close()
            return

btn_write = tk.Button(text="Write", command=write_urls)
btn_write.grid(row=3, column=4)


root.mainloop()