import os
import pickle
import sys
import tkinter as tk
from scrape_odds import odds_dict

place_d = {"kawaguchi": "川口", "isesaki": "伊勢崎", "hamamatsu": "浜松", "iizuka": "飯塚", "sanyo": "山陽"}

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master,  width=800, height=400)

        args = sys.argv 
        filepath = args[1]
        with open(filepath, mode="rb") as f:
            self.races = pickle.load(f)
        # print(self.races[0][0]) # meta
        filename = os.path.basename(filepath)

        self.dt, place_en, _ = filename.split("_")
        self.place_jp = place_d[place_en]
        self.race = 1
        self.odds_d = {}

        self.master.title(f"{self.dt} {self.place_jp}")

        # self.bg_color = self.master.cget("background")
        self.bg_color = "pink"

        self.create_frame_races()
        self.create_frame_racetitle()
        self.create_frame_buttons()
        self.create_frame_racer()
        self.create_frame_odds()
        self.create_frame_bettype()
        self.create_frame_wheel()
        self.create_frame_box()
        self.create_frame_output()
        self.grid_propagate(False) # 子フレームのgridに対し親フレームサイズ固定
        self.pack()

    def create_frame_races(self):
        frame_races = tk.Frame(self, pady=5, padx=5, bg=self.bg_color)

        r = [race[0][2] for race in self.races if race[0]]
        r += ["-" for _ in range(12-len(r))]
        btn_race1 = tk.Button(frame_races, text=f"{r[0]}", command=lambda: self.select_race(r[0]))
        btn_race2 = tk.Button(frame_races, text=f"{r[1]}", command=lambda: self.select_race(r[1]))
        btn_race3 = tk.Button(frame_races, text=f"{r[2]}", command=lambda: self.select_race(r[2]))
        btn_race4 = tk.Button(frame_races, text=f"{r[3]}", command=lambda: self.select_race(r[3]))
        btn_race5 = tk.Button(frame_races, text=f"{r[4]}", command=lambda: self.select_race(r[4]))
        btn_race6 = tk.Button(frame_races, text=f"{r[5]}", command=lambda: self.select_race(r[5]))
        btn_race7 = tk.Button(frame_races, text=f"{r[6]}", command=lambda: self.select_race(r[6]))
        btn_race8 = tk.Button(frame_races, text=f"{r[7]}", command=lambda: self.select_race(r[7]))
        btn_race9 = tk.Button(frame_races, text=f"{r[8]}", command=lambda: self.select_race(r[8]))
        btn_race10 = tk.Button(frame_races, text=f"{r[9]}", command=lambda: self.select_race(r[9]))
        btn_race11 = tk.Button(frame_races, text=f"{r[10]}", command=lambda: self.select_race(r[10]))
        btn_race12 = tk.Button(frame_races, text=f"{r[11]}", command=lambda: self.select_race(r[11]))
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

        frame_races.grid(row=0, column=0, columnspan=3, padx=10)

    def create_frame_racetitle(self):
        self.racetitle = tk.StringVar()
        self.racetitle.set("1R " + self.races[0][0][3])

        frame_racetitle = tk.Frame(self, padx=5, pady=7, bg=self.bg_color)
        label_racetitle = tk.Label(frame_racetitle, textvariable=self.racetitle)
        label_racetitle.pack(side=tk.LEFT)        

        frame_racetitle.grid(row=0, column=4, pady=5, sticky=tk.NW)

    def create_frame_buttons(self):
        frame_buttons = tk.Frame(self, bg=self.bg_color)

        frame_odds_update = tk.Frame(frame_buttons, bg=self.bg_color)
        btn_odds_update = tk.Button(frame_odds_update, text="update", command=lambda: self.update())
        btn_odds_update.pack()
        
        frame_odds_update.grid(row=0, column=0, padx=10, pady=5)

        frame_odds_calc = tk.Frame(frame_buttons, bg=self.bg_color)
        btn_odds_calc = tk.Button(frame_odds_calc, text="calc", command=lambda: self.update())
        btn_odds_calc.pack()
        
        frame_odds_calc.grid(row=0, column=1, padx=10, pady=5)

        frame_buttons.grid(row=0, column=4, padx=10, pady=5, sticky=tk.NE)

    def create_frame_racer(self):
        self.entry_df = self.races[0][1]
        self.racers = []
        for i, tpl in enumerate(self.entry_df.itertuples()):
            racer_info = tpl._2.split()
            racer = str(i+1) + " " + " ".join(racer_info[:2])
            self.racers.append(racer)
        self.racers += ["" for _ in range(8-len(self.racers))]

        self.racer1 = tk.StringVar()
        self.racer2 = tk.StringVar()
        self.racer3 = tk.StringVar()
        self.racer4 = tk.StringVar()
        self.racer5 = tk.StringVar()
        self.racer6 = tk.StringVar()
        self.racer7 = tk.StringVar()
        self.racer8 = tk.StringVar()
        self.racer1.set(self.racers[0])
        self.racer2.set(self.racers[1])
        self.racer3.set(self.racers[2])
        self.racer4.set(self.racers[3])
        self.racer5.set(self.racers[4])
        self.racer6.set(self.racers[5])
        self.racer7.set(self.racers[6])
        self.racer8.set(self.racers[7])

        frame_racers = tk.Frame(self, padx=5, pady=5, bg=self.bg_color)
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
        
        frame_racers.grid(row=1, column=0, rowspan=3, padx=10, sticky=tk.EW)

    def create_frame_odds(self):        
        self.odds1 = tk.StringVar()
        self.odds2 = tk.StringVar()
        self.odds3 = tk.StringVar()
        self.odds4 = tk.StringVar()
        self.odds5 = tk.StringVar()
        self.odds6 = tk.StringVar()
        self.odds7 = tk.StringVar()
        self.odds8 = tk.StringVar()
        self.odds1.set("")
        self.odds2.set("")
        self.odds3.set("")
        self.odds4.set("")
        self.odds5.set("")
        self.odds6.set("")
        self.odds7.set("")
        self.odds8.set("")

        frame_odds = tk.Frame(self, padx=5, pady=5, bg=self.bg_color)
        label_odds1 = tk.Label(frame_odds, textvariable=self.odds1)
        label_odds2 = tk.Label(frame_odds, textvariable=self.odds2)
        label_odds3 = tk.Label(frame_odds, textvariable=self.odds3)
        label_odds4 = tk.Label(frame_odds, textvariable=self.odds4)
        label_odds5 = tk.Label(frame_odds, textvariable=self.odds5)
        label_odds6 = tk.Label(frame_odds, textvariable=self.odds6)
        label_odds7 = tk.Label(frame_odds, textvariable=self.odds7)
        label_odds8 = tk.Label(frame_odds, textvariable=self.odds8)
        label_odds1.pack(anchor=tk.E)
        label_odds2.pack(anchor=tk.E)
        label_odds3.pack(anchor=tk.E)
        label_odds4.pack(anchor=tk.E)
        label_odds5.pack(anchor=tk.E)
        label_odds6.pack(anchor=tk.E)
        label_odds7.pack(anchor=tk.E)
        label_odds8.pack(anchor=tk.E)

        frame_odds.grid(row=1, column=1, rowspan=3, sticky=tk.EW)

    def create_frame_bettype(self):
        frame_bettype = tk.LabelFrame(self, text="bet type")
        var = tk.IntVar()
        var.set(0)
        rbn_win = tk.Radiobutton(frame_bettype, value=0, variable=var, text="win")
        rbn_exacta = tk.Radiobutton(frame_bettype, value=1, variable=var, text="exacta")
        rbn_quinella = tk.Radiobutton(frame_bettype, value=2, variable=var, text="quinella")
        rbn_tierce = tk.Radiobutton(frame_bettype, value=3, variable=var, text="tierce")
        rbn_trio = tk.Radiobutton(frame_bettype, value=4, variable=var, text="trio")
        rbn_wide = tk.Radiobutton(frame_bettype, value=5, variable=var, text="wide")
        rbn_win.grid(row=0, column=0)
        rbn_exacta.grid(row=0, column=1)
        rbn_quinella.grid(row=0, column=2)
        rbn_tierce.grid(row=0, column=3)
        rbn_trio.grid(row=0, column=4)
        rbn_wide.grid(row=0, column=5)
        frame_bettype.grid(row=1, column=4, columnspan=3, sticky=tk.W)

    def create_frame_wheel(self):
        frame_wheel = tk.Frame(self, bg=self.bg_color)

        frame_wheel1st = tk.LabelFrame(frame_wheel, text="wheel 1st")
        chk1 = tk.Checkbutton(frame_wheel1st, text="1")
        chk2 = tk.Checkbutton(frame_wheel1st, text="2")
        chk3 = tk.Checkbutton(frame_wheel1st, text="3")
        chk4 = tk.Checkbutton(frame_wheel1st, text="4")
        chk5 = tk.Checkbutton(frame_wheel1st, text="5")
        chk6 = tk.Checkbutton(frame_wheel1st, text="6")
        chk7 = tk.Checkbutton(frame_wheel1st, text="7")
        chk8 = tk.Checkbutton(frame_wheel1st, text="8")
        chk1.grid(row=0, column=0)
        chk2.grid(row=0, column=1)
        chk3.grid(row=0, column=2)
        chk4.grid(row=0, column=3)
        chk5.grid(row=1, column=0)
        chk6.grid(row=1, column=1)
        chk7.grid(row=1, column=2)
        chk8.grid(row=1, column=3)

        frame_wheel1st.grid(row=0, column=0, sticky=tk.NW)

        frame_wheel2nd = tk.LabelFrame(frame_wheel, text="2nd")
        chk1 = tk.Checkbutton(frame_wheel2nd, text="1")
        chk2 = tk.Checkbutton(frame_wheel2nd, text="2")
        chk3 = tk.Checkbutton(frame_wheel2nd, text="3")
        chk4 = tk.Checkbutton(frame_wheel2nd, text="4")
        chk5 = tk.Checkbutton(frame_wheel2nd, text="5")
        chk6 = tk.Checkbutton(frame_wheel2nd, text="6")
        chk7 = tk.Checkbutton(frame_wheel2nd, text="7")
        chk8 = tk.Checkbutton(frame_wheel2nd, text="8")
        chk1.grid(row=0, column=0)
        chk2.grid(row=0, column=1)
        chk3.grid(row=0, column=2)
        chk4.grid(row=0, column=3)
        chk5.grid(row=1, column=0)
        chk6.grid(row=1, column=1)
        chk7.grid(row=1, column=2)
        chk8.grid(row=1, column=3)

        frame_wheel2nd.grid(row=0, column=1, padx=10, sticky=tk.NW)

        frame_wheel3rd = tk.LabelFrame(frame_wheel, text="3rd")
        chk1 = tk.Checkbutton(frame_wheel3rd, text="1")
        chk2 = tk.Checkbutton(frame_wheel3rd, text="2")
        chk3 = tk.Checkbutton(frame_wheel3rd, text="3")
        chk4 = tk.Checkbutton(frame_wheel3rd, text="4")
        chk5 = tk.Checkbutton(frame_wheel3rd, text="5")
        chk6 = tk.Checkbutton(frame_wheel3rd, text="6")
        chk7 = tk.Checkbutton(frame_wheel3rd, text="7")
        chk8 = tk.Checkbutton(frame_wheel3rd, text="8")
        chk1.grid(row=0, column=0)
        chk2.grid(row=0, column=1)
        chk3.grid(row=0, column=2)
        chk4.grid(row=0, column=3)
        chk5.grid(row=1, column=0)
        chk6.grid(row=1, column=1)
        chk7.grid(row=1, column=2)
        chk8.grid(row=1, column=3)

        frame_wheel3rd.grid(row=0, column=3, sticky=tk.NW)

        frame_wheel.grid(row=2, column=4, sticky=tk.NS)

    def create_frame_box(self):
        frame_box = tk.LabelFrame(self, text="box")
        chk1 = tk.Checkbutton(frame_box, text="1")
        chk2 = tk.Checkbutton(frame_box, text="2")
        chk3 = tk.Checkbutton(frame_box, text="3")
        chk4 = tk.Checkbutton(frame_box, text="4")
        chk5 = tk.Checkbutton(frame_box, text="5")
        chk6 = tk.Checkbutton(frame_box, text="6")
        chk7 = tk.Checkbutton(frame_box, text="7")
        chk8 = tk.Checkbutton(frame_box, text="8")
        chk1.grid(row=0, column=0)
        chk2.grid(row=0, column=1)
        chk3.grid(row=0, column=2)
        chk4.grid(row=0, column=3)
        chk5.grid(row=0, column=4)
        chk6.grid(row=0, column=5)
        chk7.grid(row=0, column=6)
        chk8.grid(row=0, column=7)

        frame_box.grid(row=3, column=4, sticky=tk.NS+tk.W)

    def create_frame_output(self):
        frame_output = tk.Frame(self, bg=self.bg_color)
        label_numofbets = tk.Label(frame_output, text="Number of Bets:")
        label_number_bets = tk.Label(frame_output, text="6")
        label_synodds = tk.Label(frame_output, text="Syntheic Odds:")
        label_syntheic_odds = tk.Label(frame_output, text="3.3")
        label_numofbets.pack(side="left")
        label_number_bets.pack(side="left")
        label_synodds.pack(side="left")
        label_syntheic_odds.pack(side="left")
        frame_output.grid(row=4, column=0, padx=10, pady=7, sticky=tk.NW)

    def select_race(self, race):
        racetitle_text = "no race"
        if race.isdigit():
            racetitle_text = race + "R " + self.races[int(race)-1][0][3]    
            self.race = int(race)
            self.entry_df = self.races[self.race-1][1]
            self.racers = []
            for i, tpl in enumerate(self.entry_df.itertuples()):
                racer_info = tpl._2.split()
                racer = str(i+1) + " " + " ".join(racer_info[:2])
                self.racers.append(racer)
            self.racers += ["" for _ in range(8-len(self.racers))]
        else:
            self.racers = ["" for _ in range(8)]

        self.racetitle.set(racetitle_text)
        self.racer1.set(self.racers[0])
        self.racer2.set(self.racers[1])
        self.racer3.set(self.racers[2])
        self.racer4.set(self.racers[3])
        self.racer5.set(self.racers[4])
        self.racer6.set(self.racers[5])
        self.racer7.set(self.racers[6])
        self.racer8.set(self.racers[7])
        self.odds1.set("")
        self.odds2.set("")
        self.odds3.set("")
        self.odds4.set("")
        self.odds5.set("")
        self.odds6.set("")
        self.odds7.set("")
        self.odds8.set("")

    def update(self):
        self.odds_d = odds_dict(self.dt, self.place_jp, self.race)
        win_odds = []
        for racer in self.racers:
            if racer:
                win_odds.append(self.odds_d[racer[0]])
            else:
                win_odds.append(" ")
        self.odds1.set(win_odds[0])
        self.odds2.set(win_odds[1])
        self.odds3.set(win_odds[2])
        self.odds4.set(win_odds[3])
        self.odds5.set(win_odds[4])
        self.odds6.set(win_odds[5])
        self.odds7.set(win_odds[6])
        self.odds8.set(win_odds[7])

    def run(self):
        self.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = Application(master=root)
    app.run()