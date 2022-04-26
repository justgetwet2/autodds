import os
import pickle
import sys
import tkinter as tk
# from tkinter import ttk

class App():
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("800x400+50+50")

        args = sys.argv 
        filepath = args[1]
        with open(filepath, mode="rb") as f:
            self.races = pickle.load(f)
        # print(self.races[0][0])

        filename = os.path.basename(filepath)
        dt, place_en, _ = filename.split("_")
        place_d = {"kawaguchi": "川口", "isesaki": "伊勢崎", "hamamatsu": "浜松", "iizuka": "飯塚", "sanyo": "山陽"}
        place = place_d[place_en]

        self.root.title(f"{dt} {place}")

        default_color = self.root.cget("background")

        # bgcolor = default_color
        bgcolor = "pink"
        frame_races = tk.Frame(self.root, pady=5, padx=5, bg=bgcolor)

        r = [n for n in range(1, len(self.races)+1)]
        r += ["-" for _ in range(12-len(r))]
        btn_race1 = tk.Button(frame_races, text=f"{r[0]}", command=lambda: self.change_race(r[0]))
        btn_race2 = tk.Button(frame_races, text=f"{r[1]}", command=lambda: self.change_race(r[1]))
        btn_race3 = tk.Button(frame_races, text=f"{r[2]}", command=lambda: self.change_race(r[2]))
        btn_race4 = tk.Button(frame_races, text=f"{r[3]}", command=lambda: self.change_race(r[3]))
        btn_race5 = tk.Button(frame_races, text=f"{r[4]}", command=lambda: self.change_race(r[4]))
        btn_race6 = tk.Button(frame_races, text=f"{r[5]}", command=lambda: self.change_race(r[5]))
        btn_race7 = tk.Button(frame_races, text=f"{r[6]}", command=lambda: self.change_race(r[6]))
        btn_race8 = tk.Button(frame_races, text=f"{r[7]}", command=lambda: self.change_race(r[7]))
        btn_race9 = tk.Button(frame_races, text=f"{r[8]}", command=lambda: self.change_race(r[8]))
        btn_race10 = tk.Button(frame_races, text=f"{r[9]}", command=lambda: self.change_race(r[9]))
        btn_race11 = tk.Button(frame_races, text=f"{r[10]}", command=lambda: self.change_race(r[10]))
        btn_race12 = tk.Button(frame_races, text=f"{r[11]}", command=lambda: self.change_race(r[11]))
        # btn_race13 = tk.Button(frame_races, text=f"{r[12]}", command=lambda: self.change_race(r[12]))

        btn_race1.pack(side=tk.LEFT, anchor=tk.NW, padx=2)
        btn_race2.pack(side=tk.LEFT, anchor=tk.NW, padx=2)
        btn_race3.pack(side=tk.LEFT, anchor=tk.NW, padx=2)
        btn_race4.pack(side=tk.LEFT, anchor=tk.NW, padx=2)
        btn_race5.pack(side=tk.LEFT, anchor=tk.NW, padx=2)
        btn_race6.pack(side=tk.LEFT, anchor=tk.NW, padx=2)
        btn_race7.pack(side=tk.LEFT, anchor=tk.NW, padx=2)
        btn_race8.pack(side=tk.LEFT, anchor=tk.NW, padx=2)
        btn_race9.pack(side=tk.LEFT, anchor=tk.NW, padx=2)
        btn_race10.pack(side=tk.LEFT, anchor=tk.NW, padx=2)
        btn_race11.pack(side=tk.LEFT, anchor=tk.NW, padx=2)
        btn_race12.pack(side=tk.LEFT, anchor=tk.NW, padx=2)
        # btn_race13.pack(side=tk.LEFT, anchor=tk.NW, padx=2)

        frame_races.grid(row=0, column=0, columnspan=5, padx=10)

        self.racetitle = tk.StringVar()
        self.racetitle.set("1R " + self.races[0][0][3])

        frame_racetitle = tk.Frame(self.root, padx=5, pady=7, bg=bgcolor)
        label_racetitle = tk.Label(frame_racetitle, textvariable=self.racetitle)
        label_racetitle.pack(side=tk.LEFT)
        frame_racetitle.grid(row=0, column=6, pady=5)

        # racer
        self.entry_df = self.races[0][1]
        racers = []
        for i, tpl in enumerate(self.entry_df.itertuples()):
            racer_info = tpl._2.split()
            racer = str(i+1) + " " + " ".join(racer_info[:2])
            racers.append(racer)
        racers += ["" for _ in range(8-len(racers))]

        self.racer1 = tk.StringVar()
        self.racer2 = tk.StringVar()
        self.racer3 = tk.StringVar()
        self.racer4 = tk.StringVar()
        self.racer5 = tk.StringVar()
        self.racer6 = tk.StringVar()
        self.racer7 = tk.StringVar()
        self.racer8 = tk.StringVar()
        self.racer1.set(racers[0])
        self.racer2.set(racers[1])
        self.racer3.set(racers[2])
        self.racer4.set(racers[3])
        self.racer5.set(racers[4])
        self.racer6.set(racers[5])
        self.racer7.set(racers[6])
        self.racer8.set(racers[7])

        frame_racers = tk.Frame(self.root, padx=5, pady=5, bg=bgcolor)
        label_racer1 = tk.Label(frame_racers, textvariable=self.racer1)
        label_racer2 = tk.Label(frame_racers, textvariable=self.racer2)
        label_racer3 = tk.Label(frame_racers, textvariable=self.racer3)
        label_racer4 = tk.Label(frame_racers, textvariable=self.racer4) 
        label_racer5 = tk.Label(frame_racers, textvariable=self.racer5)
        label_racer6 = tk.Label(frame_racers, textvariable=self.racer6)
        label_racer7 = tk.Label(frame_racers, textvariable=self.racer7)
        label_racer8 = tk.Label(frame_racers, textvariable=self.racer8) 
        label_racer1.pack(anchor=tk.W)
        label_racer2.pack(anchor=tk.W)
        label_racer3.pack(anchor=tk.W)
        label_racer4.pack(anchor=tk.W)
        label_racer5.pack(anchor=tk.W)
        label_racer6.pack(anchor=tk.W)
        label_racer7.pack(anchor=tk.W)
        label_racer8.pack(anchor=tk.W)
        frame_racers.grid(row=1, column=0, padx=10, sticky=tk.EW)

        frame_winodds = tk.Frame(self.root, height=150, width=30, bg=bgcolor)
        frame_winodds.grid(row=1, column=1, sticky=tk.EW)

    def racename(self):
        pass

    def change_race(self, r):
        racetitle_text = ""
        if type(r) == int:
            racetitle_text = str(r) + "R " + self.races[r-1][0][3]    
        self.racetitle.set(racetitle_text)
    
        self.entry_df = self.races[r-1][1]
        racers = []
        for i, tpl in enumerate(self.entry_df.itertuples()):
            racer_info = tpl._2.split()
            racer = str(i+1) + " " + " ".join(racer_info[:2])
            racers.append(racer)
        racers += ["" for _ in range(8-len(racers))]
        self.racer1.set(racers[0])
        self.racer2.set(racers[1])
        self.racer3.set(racers[2])
        self.racer4.set(racers[3])
        self.racer5.set(racers[4])
        self.racer6.set(racers[5])
        self.racer7.set(racers[6])
        self.racer8.set(racers[7])

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    
    app = App()
    app.run()

# root = tk.Tk()

# root.title(f"{dt} {place}")
# root.geometry("800x400+50+50")



# CheckBox = tk.Checkbutton(text=u"self.change_racet")
# # CheckBox.pack()

