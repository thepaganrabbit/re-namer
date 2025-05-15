import tkinter as tk
from tkinter import StringVar, filedialog
from PIL import Image, ImageTk
import json
import csv
import os
import os.path

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
    fr_input.insert(0, fr_url)
    print(fr_url)


fr_input = tk.Entry(root, width=40)
fr_input.grid(row=2, column=2, columnspan=3)

# handle enter button for submission
fr_input.bind("<Return>", get_from_url)

btn_fr = tk.Button(root, text="GET", command=open_from_file_dialog)
btn_fr.grid(row=2, column=5)

# TO INPUT


def get_to_url(event=None):
    to_input.get()

# Handle button press to get path vie dialog


def open_to_file_dialog():
    to_url = filedialog.askdirectory()
    to_input.insert(0, to_url)


to_label = tk.Label(root, text="To", font=('Courier', 14))
to_label.grid(row=2, column=7, pady=15, padx=20)

to_input = tk.Entry(root, width=40)
to_input.grid(row=2, column=8, columnspan=3)

btn_to = tk.Button(root, text="GET", command=open_to_file_dialog)
btn_to.grid(row=2, column=11)

if os.path.isfile("paths.json"):
     with open("./paths.json", 'r') as pts:
        rt_pt = json.loads(pts.read())
        fr_input.insert(0, rt_pt['from_path'])
        to_input.insert(0, rt_pt['to_path'])
        pts.close()

# write URLS to file

def write_urls():
    to_url = to_input.get()
    fr_url = fr_input.get()
    with open('./paths.json', 'w') as writer:
        if len(fr_url) > 0 and len(to_url) > 0:
            data = {
                "from_path": fr_url,
                "to_path": to_url
            }
            writer.write(json.dumps(data))
        else:
            writer.close()
            return


btn_write = tk.Button(root,
                      text="Write",
                      command=write_urls,
                      width=40,
                      background="blue",
                      foreground='white',
                      height=2,
                      padx=20)
btn_write.grid(row=4, column=2, pady=20)


# list
filename = './filenamestemp.csv'

folder_files = []

def get_to_fro(): 
    to_fro = None
    with open("paths.json", 'r') as paths:
        to_fro = json.load(paths)
        paths.close()
    return to_fro
    

def get_location_files():
    to_fro = get_to_fro()
    simple_files = []
    for root, dirs, files in os.walk(to_fro['from_path']):
        for file in files:
            simple_files.append(os.path.basename(file))
            folder_files.append(str(os.path.basename(file)))
    for f in simple_files:
        l_box.insert(0, f)
    if not os.path.isfile(filename):
        with open(filename, 'w') as cf:
            cf.write('')
            cf.close()

    with open(filename, 'w') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        for line in folder_files:
            writer.writerow(line.split(r"\.(png|jpeg|jpg|gif|webm)"))
        csv_file.close()


load_btn = tk.Button(root, text="LOAD", command=get_location_files)
load_btn.grid(row=7, column=1)

selectionvar = StringVar(value=folder_files)
l_box = tk.Listbox(root, listvariable=selectionvar, width=20)
l_box.grid(row=8, column=1, rowspan=4, padx=24)

# next and renamer input

def get_arr():
    file_arr = []
    with open(filename, 'r') as fol_files:
        arr = csv.reader(fol_files)
        for a in arr:
            file_arr.append(a[0])
    return file_arr

to_input = tk.Entry(root, width=40)
to_input.grid(row=7, column=2, padx=20)

rnme_btn = tk.Button(root,text="Rename", width=20)
rnme_btn.grid(row=9, column=2)


def pop_next_name():
    arr = get_arr()
    base = get_to_fro()['from_path']
    image1 = Image.open(str(base + '/' + arr[0]))
    img_sized = 750,480
    image1.thumbnail(img_sized, Image.Resampling.LANCZOS)
    test = ImageTk.PhotoImage(image1)
    label1 = tk.Label(image=test, width=440, height=300)
    label1.image = test
    label1.grid(row=4, column=7, columnspan=5, rowspan=5)
    to_input.focus()

nxt_btn = tk.Button(root,text="pop", width=20, command=pop_next_name)
nxt_btn.grid(row=8, column=2)

if os.path.isfile(filename):
    with open(filename, 'r') as lst:
        reader = csv.reader(lst)
        csv_list = list(reader)
        for pth in csv_list:
            l_box.insert(0, pth)
        lst.close()

if (len(folder_files) > 0):
    print(folder_files)

root.mainloop()
