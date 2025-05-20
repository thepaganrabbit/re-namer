import tkinter as tk
from tkinter import StringVar, filedialog
from PIL import Image, ImageTk
import json
import csv
import os
import os.path
import shutil
from functools import partial


class Renamer:

    def __init__(self, winSize, title="Renamer"):
        self.to_url = ""
        self.from_url = ""
        self.filename = './filenamestemp.csv'
        self.paths_filename = "./paths.json"
        self.to_or_fro = {
            "from_path": "",
            "to_path": ""
        }
        self.current_file = ''
        self.isUnlocked = [False, False]
        self.folder_files = []
        self.root = tk.Tk()
        self.root.geometry(winSize)
        self.title = tk.Label(self.root, text=title, font=('Courier', 24))
        self.from_label = tk.Label(
            self.root, text="From", font=('Courier', 14))
        self.to_label = tk.Label(self.root, text="To", font=('Courier', 14))
        self.from_input = tk.Entry(self.root, width=40)
        self.from_button = tk.Button(
            self.root, text="GET", command=partial(self.open_file_dialog, 1))
        self.to_input = tk.Entry(self.root, width=40)
        self.to_button = tk.Button(
            self.root, text="GET", command=partial(self.open_file_dialog, 2))
        self.write_button = tk.Button(self.root,
                                      text="Write",
                                      command=self.write_urls,
                                      width=40,
                                      background="blue",
                                      foreground='white',
                                      height=2,
                                      padx=20)
        self.load_button = tk.Button(
            self.root, text="LOAD", command=self.load_files)
        self.file_listbox = tk.Listbox(self.root, width=20)
        self.rename_input = tk.Entry(self.root, width=40)
        self.nex_button = tk.Button(
            self.root, text="pop", width=20, command=self.pop_next_name)
        self.image_label = tk.Label(self.root);
        self.to_input.bind('<KeyPress>', self.rename_and_move)
        self.defaults()

    def open_file_dialog(self, tf):
        if tf == 1:
            from_url = filedialog.askdirectory()
            self.from_input.insert(0, from_url)
        else:
            to_url = filedialog.askdirectory()
            self.to_input.insert(0, to_url)

    def placements(self):
        self.from_input.grid(row=2, column=2, columnspan=3)
        self.title.grid(row=1, column=1, columnspan=6)
        self.from_label.grid(row=2, column=1)
        self.from_button.grid(row=2, column=5)
        self.to_label.grid(row=2, column=7, pady=15, padx=20)
        self.to_input.grid(row=2, column=8, columnspan=3)
        self.to_button.grid(row=2, column=11)
        self.write_button.grid(row=4, column=2, pady=20)
        self.load_button.grid(row=7, column=1)
        self.file_listbox.grid(row=8, column=1, rowspan=4, padx=24)
        self.nex_button.grid(row=8, column=2)
        self.image_label.grid(row=4, column=7, columnspan=5, rowspan=5)

    def defaults(self):
        if os.path.isfile(self.paths_filename):
            with open(self.paths_filename, 'r') as pts:
                rt_pt = json.loads(pts.read())
                self.from_input.insert(0, rt_pt['from_path'])
                self.to_input.insert(0, rt_pt['to_path'])
                pts.close()
        if os.path.isfile(self.filename):
            self.get_location_files()
        if not os.path.isfile(self.filename):
            with open(self.filename, 'w') as cf:
                cf.write('')
                cf.close()
        if not os.path.isfile(self.paths_filename):
            with open(self.paths_filename, 'w') as cf:
                cf.write('\{\}')
                cf.close()

    def write_urls(self):
        self.to_url = self.to_input.get()
        self.from_url = self.from_input.get()
        with open(self.paths_filename, 'w') as writer:
            if len(self.from_url) > 0 and len(self.to_url) > 0:
                data = {
                    "from_path": self.from_url,
                    "to_path": self.to_url
                }
                writer.write(json.dumps(data))
            else:
                writer.close()
                return
            writer.close()

    def get_to_fro(self):
        with open("paths.json", 'r') as paths:
            self.get_to_fro = json.load(paths)
            paths.close()

    def get_location_files(self):
        for root, dirs, files in os.walk(self.to_or_fro['from_path']):
            for file in files:
                self.folder_files.append(str(os.path.basename(file)))

        with open(self.filename, 'w') as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            for line in self.folder_files:
                writer.writerow(line.split(r"\.(png|jpeg|jpg|gif|webm)"))
            csv_file.close()

    def get_files_from_csv(self):
        with open(self.filename, 'r') as fol_files:
            arr = csv.reader(fol_files)
            for a in arr:
                self.folder_files.append(a[0])

    def load_files(self):
        for f in self.load_files:
            self.file_listbox.insert(0, f)

    def check_if_ready(self):
        if len(self.folder_files) > 0 and len(self.to_or_fro['from_path']) > 5:
            return True
        else:
            return False

    def clean_get_files(self): 
        if self.check_if_ready():
            self.folder_files = self.get_location_files()

    def pop_next_name(self):
        self.current_file = ""
        if self.check_if_ready():
            arr = self.clean_get_files()
            self.current_file = arr[0]
            img_sized = 750,480
            image = Image.open(str(self.to_or_fro['from_path'] + '/' + arr[0]))
            image.thumbnail(img_sized, Image.Resampling.LANCZOS)
            photo_image = ImageTk.PhotoImage(image)
            self.image_label.config(text=self.current_file, image=photo_image, width=440, height=300)
            self.image_label.image = photo_image
            self.to_input.focus()
            
    def rename_and_move(self, event):
        if event.keysym == 'Return':
            to = str(self.to_or_fro['to_path'] + '/' + self.to_input.get())
            origin = str(self.to_or_fro['from_path'] + '/' + self.current_file)
            os.rename(origin, to)
            shutil.move(to, self.to_or_fro['to_path'])
            self.to_input.delete(0, tk.END)
            self.to_input.config(state='normal')
            self.to_input.focus()
    
    def run(self):
        self.root.mainloop()