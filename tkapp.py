from calendar import c
import itertools
import numpy as np
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
        self.frame_main = tk.Frame(self, padx=10, pady=3)
        self.frame_bets = tk.Frame(self, padx=10, pady=3)
        self.frame_status = tk.Frame(self)

        # self.bg_color = self.master.cget("background")
        self.bg_color = "pink"

        self.grid_propagate(False) # 子フレームのgridに対し親フレームサイズ固定
        self.create_frame_races()
        self.create_frame_racetitle()
        self.create_frame_buttons()
        self.create_frame_racer()
        self.create_frame_odds()
        self.create_frame_bettype()
        self.create_frame_wheel()
        self.create_frame_box()
        self.create_frame_output()
        self.frame_main.pack()
        
        self.create_frame_bets()
        self.frame_bets.pack(fill=tk.X)

        self.create_status_bar()
        self.frame_status.pack(fill=tk.X)
        
        self.pack()

    def create_status_bar(self):
        status_bar = tk.Label(self.frame_status, text="status bar", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(fill=tk.X)

    def create_frame_races(self):
        frame_races = tk.Frame(self.frame_main, bg=self.bg_color)

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

        frame_races.grid(row=0, column=0, columnspan=3)

    def create_frame_racetitle(self):
        self.racetitle = tk.StringVar()
        self.racetitle.set("1R " + self.races[0][0][3])

        frame_racetitle = tk.Frame(self.frame_main, padx=10, pady=10, bg=self.bg_color)
        label_racetitle = tk.Label(frame_racetitle, textvariable=self.racetitle)
        label_racetitle.pack(side=tk.LEFT)        

        frame_racetitle.grid(row=0, column=4, sticky=tk.NW)

    def create_frame_buttons(self):
        frame_buttons = tk.Frame(self.frame_main, pady=10, bg=self.bg_color)

        frame_odds_update = tk.Frame(frame_buttons, bg=self.bg_color)
        btn_odds_update = tk.Button(frame_odds_update, text="update", command=lambda: self.update())
        btn_odds_update.pack()
        # frame_odds_update.grid(row=0, column=0, padx=10, pady=5)
        frame_odds_update.pack(side="left", padx=5)

        frame_odds_calc = tk.Frame(frame_buttons, bg=self.bg_color)
        btn_odds_calc = tk.Button(frame_odds_calc, text="calc", command=lambda: self.calc())
        btn_odds_calc.pack()     
        # frame_odds_calc.grid(row=0, column=1, padx=10, pady=5)
        frame_odds_calc.pack(side="left", padx=5)

        frame_buttons.grid(row=0, column=4, sticky=tk.NE)

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

        frame_racers = tk.Frame(self.frame_main, padx=5, pady=5, bg=self.bg_color)
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
        
        frame_racers.grid(row=1, column=0, rowspan=3, sticky=tk.EW)

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

        frame_odds = tk.Frame(self.frame_main, padx=5, pady=5, bg=self.bg_color)
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

        frame_odds.grid(row=1, column=1, rowspan=3, sticky=tk.NW)

    def create_frame_bettype(self):
        frame_bettype = tk.LabelFrame(self.frame_main, text="bet type")
        self.radio_var = tk.IntVar(value=0)
        rbn_all = tk.Radiobutton(frame_bettype, value=0, variable=self.radio_var, text="all")
        rbn_win = tk.Radiobutton(frame_bettype, value=1, variable=self.radio_var, text="win")
        rbn_exacta = tk.Radiobutton(frame_bettype, value=2, variable=self.radio_var, text="exacta")
        rbn_quinella = tk.Radiobutton(frame_bettype, value=3, variable=self.radio_var, text="quinella")
        rbn_tierce = tk.Radiobutton(frame_bettype, value=4, variable=self.radio_var, text="tierce")
        rbn_trio = tk.Radiobutton(frame_bettype, value=5, variable=self.radio_var, text="trio")
        rbn_wide = tk.Radiobutton(frame_bettype, value=6, variable=self.radio_var, text="wide")
        rbn_all.pack(side="left")
        rbn_win.pack(side="left")
        rbn_exacta.pack(side="left")
        rbn_quinella.pack(side="left")
        rbn_tierce.pack(side="left")
        rbn_trio.pack(side="left")
        rbn_wide.pack(side="left")
        frame_bettype.grid(row=1, column=4, columnspan=3, padx=5, sticky=tk.NW)

    def create_frame_wheel(self):
        frame_wheel = tk.Frame(self.frame_main, padx=5, bg=self.bg_color)

        frame_wheel1st = tk.LabelFrame(frame_wheel, text="wheel 1st")
        self.chk_w11 = tk.BooleanVar(value=False)
        self.chk_w12 = tk.BooleanVar(value=False)
        self.chk_w13 = tk.BooleanVar(value=False)
        self.chk_w14 = tk.BooleanVar(value=False)
        self.chk_w15 = tk.BooleanVar(value=False)
        self.chk_w16 = tk.BooleanVar(value=False)
        self.chk_w17 = tk.BooleanVar(value=False)
        self.chk_w18 = tk.BooleanVar(value=False)
        self.chk_w21 = tk.BooleanVar(value=False)
        self.chk_w22 = tk.BooleanVar(value=False)
        self.chk_w23 = tk.BooleanVar(value=False)
        self.chk_w24 = tk.BooleanVar(value=False)
        self.chk_w25 = tk.BooleanVar(value=False)
        self.chk_w26 = tk.BooleanVar(value=False)
        self.chk_w27 = tk.BooleanVar(value=False)
        self.chk_w28 = tk.BooleanVar(value=False)
        self.chk_w31 = tk.BooleanVar(value=False)
        self.chk_w32 = tk.BooleanVar(value=False)
        self.chk_w33 = tk.BooleanVar(value=False)
        self.chk_w34 = tk.BooleanVar(value=False)
        self.chk_w35 = tk.BooleanVar(value=False)
        self.chk_w36 = tk.BooleanVar(value=False)
        self.chk_w37 = tk.BooleanVar(value=False)
        self.chk_w38 = tk.BooleanVar(value=False)

        chk11 = tk.Checkbutton(frame_wheel1st, variable=self.chk_w11, text="1")
        chk12 = tk.Checkbutton(frame_wheel1st, variable=self.chk_w12, text="2")
        chk13 = tk.Checkbutton(frame_wheel1st, variable=self.chk_w13, text="3")
        chk14 = tk.Checkbutton(frame_wheel1st, variable=self.chk_w14, text="4")
        chk15 = tk.Checkbutton(frame_wheel1st, variable=self.chk_w15, text="5")
        chk16 = tk.Checkbutton(frame_wheel1st, variable=self.chk_w16, text="6")
        chk17 = tk.Checkbutton(frame_wheel1st, variable=self.chk_w17, text="7")
        chk18 = tk.Checkbutton(frame_wheel1st, variable=self.chk_w18, text="8")
        chk11.grid(row=0, column=0)
        chk12.grid(row=0, column=1)
        chk13.grid(row=0, column=2)
        chk14.grid(row=0, column=3)
        chk15.grid(row=1, column=0)
        chk16.grid(row=1, column=1)
        chk17.grid(row=1, column=2)
        chk18.grid(row=1, column=3)

        frame_wheel1st.grid(row=0, column=0, sticky=tk.NW)

        frame_wheel2nd = tk.LabelFrame(frame_wheel, text="2nd")
        chk21 = tk.Checkbutton(frame_wheel2nd, variable=self.chk_w21, text="1")
        chk22 = tk.Checkbutton(frame_wheel2nd, variable=self.chk_w22, text="2")
        chk23 = tk.Checkbutton(frame_wheel2nd, variable=self.chk_w23, text="3")
        chk24 = tk.Checkbutton(frame_wheel2nd, variable=self.chk_w24, text="4")
        chk25 = tk.Checkbutton(frame_wheel2nd, variable=self.chk_w25, text="5")
        chk26 = tk.Checkbutton(frame_wheel2nd, variable=self.chk_w26, text="6")
        chk27 = tk.Checkbutton(frame_wheel2nd, variable=self.chk_w27, text="7")
        chk28 = tk.Checkbutton(frame_wheel2nd, variable=self.chk_w28, text="8")
        chk21.grid(row=0, column=0)
        chk22.grid(row=0, column=1)
        chk23.grid(row=0, column=2)
        chk24.grid(row=0, column=3)
        chk25.grid(row=1, column=0)
        chk26.grid(row=1, column=1)
        chk27.grid(row=1, column=2)
        chk28.grid(row=1, column=3)

        frame_wheel2nd.grid(row=0, column=1, padx=10, sticky=tk.NW)

        frame_wheel3rd = tk.LabelFrame(frame_wheel, text="3rd")
        chk31 = tk.Checkbutton(frame_wheel3rd, variable=self.chk_w31, text="1")
        chk32 = tk.Checkbutton(frame_wheel3rd, variable=self.chk_w32, text="2")
        chk33 = tk.Checkbutton(frame_wheel3rd, variable=self.chk_w33, text="3")
        chk34 = tk.Checkbutton(frame_wheel3rd, variable=self.chk_w34, text="4")
        chk35 = tk.Checkbutton(frame_wheel3rd, variable=self.chk_w35, text="5")
        chk36 = tk.Checkbutton(frame_wheel3rd, variable=self.chk_w36, text="6")
        chk37 = tk.Checkbutton(frame_wheel3rd, variable=self.chk_w37, text="7")
        chk38 = tk.Checkbutton(frame_wheel3rd, variable=self.chk_w38, text="8")
        chk31.grid(row=0, column=0)
        chk32.grid(row=0, column=1)
        chk33.grid(row=0, column=2)
        chk34.grid(row=0, column=3)
        chk35.grid(row=1, column=0)
        chk36.grid(row=1, column=1)
        chk37.grid(row=1, column=2)
        chk38.grid(row=1, column=3)

        frame_wheel3rd.grid(row=0, column=3, sticky=tk.NW)

        frame_wheel.grid(row=2, column=4, sticky=tk.NS)

    def create_frame_box(self):
        frame_box_etc = tk.Frame(self.frame_main, padx=5, bg=self.bg_color)

        frame_box = tk.LabelFrame(frame_box_etc, text="box")
        self.chk_b1 = tk.BooleanVar(value=False)
        self.chk_b2 = tk.BooleanVar(value=False)
        self.chk_b3 = tk.BooleanVar(value=False)
        self.chk_b4 = tk.BooleanVar(value=False)
        self.chk_b5 = tk.BooleanVar(value=False)
        self.chk_b6 = tk.BooleanVar(value=False)
        self.chk_b7 = tk.BooleanVar(value=False)
        self.chk_b8 = tk.BooleanVar(value=False)
        chk1 = tk.Checkbutton(frame_box, variable=self.chk_b1, text="1")
        chk2 = tk.Checkbutton(frame_box, variable=self.chk_b2, text="2")
        chk3 = tk.Checkbutton(frame_box, variable=self.chk_b3, text="3")
        chk4 = tk.Checkbutton(frame_box, variable=self.chk_b4, text="4")
        chk5 = tk.Checkbutton(frame_box, variable=self.chk_b5, text="5")
        chk6 = tk.Checkbutton(frame_box, variable=self.chk_b6, text="6")
        chk7 = tk.Checkbutton(frame_box, variable=self.chk_b7, text="7")
        chk8 = tk.Checkbutton(frame_box, variable=self.chk_b8, text="8")
        chk1.grid(row=0, column=0)
        chk2.grid(row=0, column=1)
        chk3.grid(row=0, column=2)
        chk4.grid(row=0, column=3)
        chk5.grid(row=0, column=4)
        chk6.grid(row=0, column=5)
        chk7.grid(row=0, column=6)
        chk8.grid(row=0, column=7)

        frame_box.pack(side="left")

        frame_options = tk.LabelFrame(frame_box_etc, text="option")
        self.chk_trn = tk.BooleanVar(value=False)
        chk_turnup = tk.Checkbutton(frame_options, variable=self.chk_trn, text="1st<=>2nd")
        chk_turnup.pack()
        frame_options.pack(side="left", padx=10)

        btn_clear = tk.Button(frame_box_etc, text="clear", command=lambda: self.check_clear())
        btn_clear.pack(side="left", pady=6, anchor=tk.S)

        frame_box_etc.grid(row=3, column=4, sticky=tk.NS+tk.W)

    def create_frame_output(self):
        frame_output = tk.Frame(self.frame_main, padx=3, pady=10, bg=self.bg_color)
        
        self.number_of_bets = tk.StringVar(value="")
        self.syntheic_odds = tk.StringVar(value="")

        tag_number_of_bets = tk.Label(frame_output, text="Number of Bets:")
        label_number_of_bets = tk.Label(frame_output, textvariable=self.number_of_bets)
        tag_syntheic_odds = tk.Label(frame_output, text="Syntheic Odds:")
        label_syntheic_odds = tk.Label(frame_output, textvariable=self.syntheic_odds)
        
        tag_number_of_bets.pack(side="left")
        label_number_of_bets.pack(side="left", padx=10)
        tag_syntheic_odds.pack(side="left", padx=10)
        label_syntheic_odds.pack(side="left")

        frame_output.grid(row=4, column=0, sticky=tk.NW)

    def create_frame_bets(self):
        self.show_bets = tk.Text(self.frame_bets, width=60, height=20)
        self.show_bets.grid(column=0, row=0, pady=10, sticky=tk.N+tk.S+tk.E+tk.W)

    def select_race(self, race):
        self.check_clear()
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

    def check_clear(self):
        self.chk_w11.set(0); self.chk_w12.set(0); self.chk_w13.set(0); self.chk_w14.set(0)
        self.chk_w15.set(0); self.chk_w16.set(0); self.chk_w17.set(0); self.chk_w18.set(0)
        self.chk_w21.set(0); self.chk_w22.set(0); self.chk_w23.set(0); self.chk_w24.set(0)
        self.chk_w25.set(0); self.chk_w26.set(0); self.chk_w27.set(0); self.chk_w28.set(0)
        self.chk_w31.set(0); self.chk_w32.set(0); self.chk_w33.set(0); self.chk_w34.set(0)
        self.chk_w35.set(0); self.chk_w36.set(0); self.chk_w37.set(0); self.chk_w38.set(0)
        self.chk_b1.set(0); self.chk_b2.set(0); self.chk_b3.set(0); self.chk_b4.set(0)
        self.chk_b5.set(0); self.chk_b6.set(0); self.chk_b7.set(0); self.chk_b8.set(0)
        self.chk_trn.set(0)
        self.number_of_bets.set(""); self.syntheic_odds.set("")
        self.show_bets.delete("1.0", tk.END)

    def checked_bets(self):
        w1 = [self.chk_w11.get(), self.chk_w12.get(), self.chk_w13.get(), self.chk_w14.get()]
        w1 += [self.chk_w15.get(), self.chk_w16.get(), self.chk_w17.get(), self.chk_w18.get()]
        idx1 = [i+1 for i, w in enumerate(w1) if w]
        
        w2 = [self.chk_w21.get(), self.chk_w22.get(), self.chk_w23.get(), self.chk_w24.get()]
        w2 += [self.chk_w25.get(), self.chk_w26.get(), self.chk_w27.get(), self.chk_w28.get()]
        idx2 = [i+1 for i, w in enumerate(w2) if w]

        w3 = [self.chk_w31.get(), self.chk_w32.get(), self.chk_w33.get(), self.chk_w34.get()]
        w3 += [self.chk_w35.get(), self.chk_w36.get(), self.chk_w37.get(), self.chk_w38.get()]
        idx3 = [i+1 for i, w in enumerate(w3) if w]

        bx = [self.chk_b1.get(), self.chk_b2.get(), self.chk_b3.get(), self.chk_b4.get()]
        bx += [self.chk_b5.get(), self.chk_b6.get(), self.chk_b7.get(), self.chk_b8.get()]
        idx4 = [i+1 for i, b in enumerate(bx) if b]

        return idx1, idx2, idx3, idx4

    def calc_syntheic_odds(self, l_odds):
        return 1/np.reciprocal(l_odds).sum()

    def calc_wins(self, bets):
        sellctions = [str(bet) for bet in bets]
        oddses = [self.odds_d[str(bet)] for bet in bets]
        syn_odds = self.calc_syntheic_odds(oddses)
        sellctions = [(str(bet), odds) for bet, odds in zip(bets, oddses)]

        return syn_odds, sellctions

    def calc_permutation(self, bets, cmb=2):
        selections, oddses = [], []
        for pair in itertools.permutations(bets, cmb):
            bet = str(pair[0]) + "-" + str(pair[1])
            if cmb == 3:
                bet += "-" + str(pair[2])
            odds = self.odds_d[bet]
            oddses.append(odds)
            selections.append((bet, odds))
        syn_odds = self.calc_syntheic_odds(oddses)

        return syn_odds, selections

    def calc_combination(self, bets, cmb=2, wide=False):
        selections, oddses = [], []
        for pair in itertools.combinations(bets, cmb):
            bet = str(pair[0]) + "=" + str(pair[1])
            if cmb == 3:
                bet += "=" + str(pair[2])
            if wide:
                bet = bet.replace("=", "w")
            odds = self.odds_d[bet]
            oddses.append(odds)
            selections.append((bet, odds))
        syn_odds = self.calc_syntheic_odds(oddses)

        return syn_odds, selections

    def calc(self):
        chk_bets = self.checked_bets()
        bettype = self.radio_var.get()
        self.show_bets.delete("1.0", tk.END)
        self.outputs = []

        if chk_bets[3]: # box
            bets = chk_bets[3]
            win_synodds, win_selections = self.calc_wins(bets)
            exa_synodds, exa_selections = self.calc_permutation(bets)
            qin_synodds, qin_selections = self.calc_combination(bets)
            tie_synodds, tie_selections = self.calc_permutation(bets, cmb=3)    
            tri_synodds, tri_selections = self.calc_combination(bets, cmb=3)
            wid_synodds, wid_selections = self.calc_combination(bets, wide=True)
            if bettype == 0: # all
                win_txt = "win :    " + str(len(win_selections)).rjust(3) + str(round(win_synodds, 1)).rjust(6)
                exa_txt = "exacta : " + str(len(exa_selections)).rjust(3) + str(round(exa_synodds,1)).rjust(6)
                qin_txt = "quinella:" + str(len(qin_selections)).rjust(3) + str(round(qin_synodds,1)).rjust(6)
                tie_txt = "tierce : " + str(len(tie_selections)).rjust(3) + str(round(tie_synodds, 1)).rjust(6)
                tri_txt = "trio :   " + str(len(tri_selections)).rjust(3) + str(round(tri_synodds,1)).rjust(6)
                wid_txt = "wide :   " + str(len(wid_selections)).rjust(3) + str(round(wid_synodds,1)).rjust(6)
                self.outputs = [win_txt, exa_txt, qin_txt, tie_txt, tri_txt, wid_txt]
                for output in self.outputs:
                    self.show_bets.insert(tk.END, output + "\n")
            if bettype == 1: # win
                self.output_for_textbox(win_synodds, win_selections)
            if bettype == 2: # exacta
                self.output_for_textbox(exa_synodds, exa_selections)
            if bettype == 3: # quinella
                self.output_for_textbox(qin_synodds, qin_selections)    
            if bettype == 4: # tierce
                self.output_for_textbox(tie_synodds, tie_selections)     
            if bettype == 5: # trio
                self.output_for_textbox(tri_synodds, tri_selections)     
            if bettype == 6: # wide
                self.output_for_textbox(wid_synodds, wid_selections)

            for output in self.outputs:
                self.show_bets.insert(tk.END, output + "\n")

        elif len(chk_bets[0]) == 1 and chk_bets[1] and not chk_bets[2]:
            if bettype == 2: # exacta
                bets = [str(chk_bets[0][0]) + "-" + str(bet) for bet in chk_bets[1]]
            if bettype == 3: # quinella
                pass
                # bets = [str(chk_bets[0][0]) + "=" + str(bet) for bet in chk_bets[1]]
            oddses = [self.odds_d[bet] for bet in bets]
            syn_odds = self.calc_syntheic_odds(oddses)
            selections = [(str(bet), odds) for bet, odds in zip(bets, oddses)]
            self.output_for_textbox(syn_odds, selections)

    def output_for_textbox(self, synodds, selections):
        self.number_of_bets.set(len(selections))
        self.syntheic_odds.set(round(synodds, 1))
        for bet, odds in selections:
            buy = 3000 * synodds / odds
            txt = " " + str(bet) + str(odds).rjust(7) + str(round(buy)).rjust(7)
            self.outputs.append(txt) 
        for output in self.outputs:
            self.show_bets.insert(tk.END, output + "\n")

    def run(self):
        self.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = Application(master=root)
    app.run()