import tkinter as tk
from tkinter import StringVar, filedialog
from PIL import Image, ImageTk
import json
import csv
import os
import os.path
import shutil
from functools import partial
import sys
import random


class Renamer:

    def __init__(self, winSize, title="Renamer"):
        self.filename = './filenamestemp.csv'
        self.paths_filename = "./paths.json"
        self.counter = 0
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
        self.rename_label = tk.Label(self.root)
        self.nex_button = tk.Button(
            self.root, text="pop", width=20, command=self.pop_next_name)
        self.image_label = tk.Label(self.root)
        self.rename_input.bind('<KeyPress>', self.rename_and_move)
        self.btm_img_1_label = tk.Label(self.root)
        self.btm_img_2_label = tk.Label(self.root)
        self.btm_img_3_label = tk.Label(self.root)
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
        self.from_label.grid(row=2, column=1, columnspan=2)
        self.from_button.grid(row=2, column=5)
        self.to_label.grid(row=2, column=7, pady=15, padx=20)
        self.to_input.grid(row=2, column=8, columnspan=3)
        self.to_button.grid(row=2, column=11)
        self.write_button.grid(row=4, column=2, pady=20)
        self.load_button.grid(row=7, column=1)
        self.file_listbox.grid(row=8, column=1, rowspan=4, padx=24)
        self.nex_button.grid(row=8, column=2)
        self.image_label.grid(row=4, column=7, columnspan=5, rowspan=5)
        self.rename_input.grid(row=7, column=2, padx=20)
        self.rename_label.grid(row=9, column=2)
        self.btm_img_1_label.grid(row=23, column=1, columnspan=2)
        self.btm_img_2_label.grid(row=23, column=2, columnspan=2)
        self.btm_img_3_label.grid(row=23, column=3, columnspan=2)

    def defaults(self):
        if not os.path.isfile(self.filename):
            with open(self.filename, 'w') as cf:
                cf.write('')
                cf.close()
        if not os.path.isfile(self.paths_filename):
            with open(self.paths_filename, 'w') as cf:
                cf.write('{}')
                cf.close()
        if os.path.isfile(self.paths_filename):
            with open(self.paths_filename, 'r') as pts:
                rt_pt = json.load(pts)
                if 'from_path' in rt_pt and len(rt_pt['from_path']) > 0:
                    self.to_or_fro = rt_pt
                    self.from_input.insert(0, rt_pt['from_path'])
                    self.to_input.insert(0, rt_pt['to_path'])
                pts.close()
        if os.path.isfile(self.filename) and 'from_path' in self.to_or_fro and len(self.to_or_fro['from_path']) > 0:
            self.get_location_files()
        if len(self.folder_files) > 0:
            for file in self.folder_files:
                self.file_listbox.insert(0, file)
            self.current_file = self.folder_files[0]
            self.load_btm_images()

    def write_urls(self):
        self.to_or_fro['to_path'] = self.to_input.get()
        self.to_or_fro['from_path'] = self.from_input.get()
        with open(self.paths_filename, 'w') as writer:
            if len(self.to_or_fro['from_path']) > 0 and len(self.to_or_fro['to_path']) > 0:
                data = {
                    "from_path": self.to_or_fro['from_path'],
                    "to_path": self.to_or_fro['to_path']
                }
                writer.write(json.dumps(data))
            else:
                writer.close()
                return
            writer.close()
        self.get_location_files()
        self.load_files()
        self.load_btm_images()

    def get_to_fro(self):
        with open("paths.json", 'r') as paths:
            self.get_to_fro = json.load(paths)
            paths.close()

    def load_btm_images(self):
        # image 1
        img_sized = 440, 240
        image = Image.open(
            str(self.to_or_fro['from_path'] + '/' + self.folder_files[2]))
        image.thumbnail(img_sized, Image.Resampling.LANCZOS)
        photo_image = ImageTk.PhotoImage(image)
        self.btm_img_1_label.config(image=photo_image)
        self.btm_img_1_label.image = photo_image
        # image 2
        image2 = Image.open(
            str(self.to_or_fro['from_path'] + '/' + self.folder_files[1]))
        image2.thumbnail(img_sized, Image.Resampling.LANCZOS)
        photo_image2 = ImageTk.PhotoImage(image2)
        self.btm_img_2_label.config(image=photo_image2)
        self.btm_img_2_label.image = photo_image2
        # image 3
        image3 = Image.open(
            str(self.to_or_fro['from_path'] + '/' + self.folder_files[0]))
        image3.thumbnail(img_sized, Image.Resampling.LANCZOS)
        photo_image3 = ImageTk.PhotoImage(image3)
        self.btm_img_3_label.config(image=photo_image3)
        self.btm_img_3_label.image = photo_image3

    def get_location_files(self):
        self.folder_files = os.listdir(self.to_or_fro['from_path'])
        # for (root, dirs, files) in os.walk(self.to_or_fro['from_path']):
        #     print(files)
        #     for file in files:
        #         self.folder_files.append(str(os.path.basename(file)))
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
        if len(self.to_or_fro['from_path']) > 0:
            self.get_location_files()
        for file in self.folder_files:
            self.file_listbox.insert(0, file)

    def check_if_ready(self):
        if len(self.folder_files) > 0 and len(self.to_or_fro['from_path']) > 5:
            return True
        else:
            return False

    def clean_get_files(self):
        if self.check_if_ready():
            self.get_location_files()

    def pop_next_name(self):
        if self.check_if_ready():
            # self.clean_get_files()
            img_sized = 940, 480
            image = Image.open(
                str(self.to_or_fro['from_path'] + '/' + self.current_file))
            image.thumbnail(img_sized, Image.Resampling.LANCZOS)
            photo_image = ImageTk.PhotoImage(image)
            self.image_label.config(text=self.current_file, image=photo_image)
            self.rename_label.config(text=self.current_file)
            self.image_label.image = photo_image
            self.rename_input.focus()

    def filtered_img_arr(self, arr, str):
        arr.remove(str)
        fixed_arr = [arr[0], arr[1], arr[2]]
        return fixed_arr

    def rename_and_move(self, event):
        if event.keysym == 'Return':
            self.counter = self.counter + 1
            input_text = self.rename_input.get()
            command = input_text.split('<')
            if len(command) > 1:
                cmd = command[len(command) - 1].replace(' ', '')
                if cmd == 'gen':
                    print('should have changed')
                    input_text = str(
                        command[0] + str(random.randint(0, sys.maxsize)))
            ending = self.current_file.split(".")
            end_len = len(ending) - 1
            to = str(self.to_or_fro['from_path'] +
                     '/' + input_text + '.' + ending[end_len])
            origin = str(self.to_or_fro['from_path'] + '/' + self.current_file)
            os.rename(origin, to)
            if input_text == '-delete-':
                os.remove(to)
                self.current_file = self.folder_files.pop()
                self.rename_input.delete(0, tk.END)
                self.pop_next_name()
                self.rename_input.focus()
            else:
                shutil.move(to, self.to_or_fro['to_path'])
                old_file = self.current_file
                self.current_file = self.folder_files.pop()
                if old_file in self.folder_files:
                    self.folder_files.remove(old_file)
                    self.load_btm_images()
                if self.counter == 2:
                    self.load_files()
                self.rename_input.delete(0, tk.END)
                self.pop_next_name()
                self.rename_input.focus()

    def run(self):
        self.root.mainloop()


r_name = Renamer('1140x820', 'Renamer')

r_name.placements()

r_name.run()
