import itertools
import numpy as np
import math
import os
import pickle
import sys
import tkinter as tk
from scrape_odds import odds_dict

place_d = {"kawaguchi": "川口", "isesaki": "伊勢崎", "hamamatsu": "浜松", "iizuka": "飯塚", "sanyo": "山陽"}

class Application(tk.Frame):
    def __init__(self, master):
        super().__init__(master) #,  width=800, height=400)

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
        # self.create_frame_racetitle()
        self.create_frame_buttons()
        self.create_frame_racer()
        self.create_frame_odds()
        self.create_frame_bettype()
        self.create_frame_wheel()
        self.create_frame_box()
        self.create_frame_output()
        self.frame_main.pack()
        
        self.create_frame_textbox()
        self.create_frame_bets()
        self.frame_bets.pack(fill=tk.X)

        self.create_status_bar()
        self.frame_status.pack(fill=tk.X)
        
        self.pack()

    ''' create part '''

    def create_status_bar(self):
        status_bar = tk.Label(self.frame_status, text="status bar", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(fill=tk.X)

    def create_frame_races(self):
        frame_races = tk.Frame(self.frame_main, bg=self.bg_color)
        race_numbers = [race[0][2] for race in self.races if race[0]]
        race_numbers += ["-" for _ in range(12-len(race_numbers))]
        buttons = []
        for i, num in enumerate(race_numbers):
            button = tk.Button(frame_races, text=f"{num}", command=self.callback(num))
            buttons.append(button)
            buttons[i].pack(side=tk.LEFT, padx=2)

        frame_races.grid(row=0, column=0, columnspan=3, sticky=tk.W)

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

        frame_buttons.grid(row=0, column=3, sticky=tk.NE)

    def create_frame_racer(self):
        self.entry_df = self.races[0][1]
        self.racers = []
        for i, tpl in enumerate(self.entry_df.itertuples()):
            racer_info = tpl._2.split()
            racer = str(i+1) + " " + " ".join(racer_info[:2])
            self.racers.append(racer)
        self.racers += ["" for _ in range(8-len(self.racers))]

        frame_racers = tk.Frame(self.frame_main, padx=5, pady=5, bg=self.bg_color)
        self.var_racers = []
        label_racers = []
        for i in range(8):
            self.var_racers.append(tk.StringVar())
            self.var_racers[i].set(self.racers[i])
            label_racers.append(tk.Label(frame_racers, textvariable=self.var_racers[i]))
            label_racers[i].pack(anchor=tk.W)
        
        frame_racers.grid(row=1, column=0, rowspan=3, sticky=tk.EW)

    def create_frame_odds(self):
        frame_odds = tk.Frame(self.frame_main, padx=5, pady=5, bg=self.bg_color)
        self.var_oddses = []
        label_oddses = []
        for i in range(8):
            self.var_oddses.append(tk.StringVar())
            self.var_oddses[i].set("")
            label_oddses.append(tk.Label(frame_odds, textvariable=self.var_oddses[i]))
            label_oddses[i].pack(anchor=tk.E)

        frame_odds.grid(row=1, column=1, rowspan=3, sticky=tk.NW)

    def create_frame_bettype(self):
        frame_bettype = tk.LabelFrame(self.frame_main, text="bet type")
        self.var_radio = tk.IntVar(value=0)
        bettypes = "all", "win", "exacta", "quinella", "trifecta", "trio", "wide"
        radiobuttons = []
        for i, text in enumerate(bettypes):
            rbn = tk.Radiobutton(frame_bettype, value=i, variable=self.var_radio, text=text)
            radiobuttons.append(rbn)
            radiobuttons[i].pack(side=tk.LEFT)

        frame_bettype.grid(row=1, column=2, columnspan=3, padx=5, sticky=tk.NW)

    def create_frame_wheel(self):
        frame_wheel = tk.Frame(self.frame_main, padx=5, bg=self.bg_color)

        frame_wheel1st = tk.LabelFrame(frame_wheel, text="1st")
        self.var_wheel1st = []
        chk_wheel1st = []
        n = 0.
        for i in range(8):
            self.var_wheel1st.append(tk.BooleanVar(value=False))
            chk = tk.Checkbutton(frame_wheel1st, variable=self.var_wheel1st[i], text=str(i+1).rjust(2))
            chk_wheel1st.append(chk)
            chk_wheel1st[i].grid(row=math.floor(n), column=i%4)
            n += 1/4
        frame_wheel1st.pack(side=tk.LEFT)

        frame_wheel2nd = tk.LabelFrame(frame_wheel, text="2nd")
        self.var_wheel2nd = []
        chk_wheel2nd = []
        n = 0.
        for i in range(8):
            self.var_wheel2nd.append(tk.BooleanVar(value=False))
            chk = tk.Checkbutton(frame_wheel2nd, variable=self.var_wheel2nd[i], text=str(i+1).rjust(2))
            chk_wheel2nd.append(chk)
            chk_wheel2nd[i].grid(row=math.floor(n), column=i%4)
            n += 1/4
        frame_wheel2nd.pack(side=tk.LEFT, padx=10)

        frame_wheel3rd = tk.LabelFrame(frame_wheel, text="3rd")
        self.var_wheel3rd = []
        chk_wheel3rd = []
        n = 0.
        for i in range(8):
            self.var_wheel3rd.append(tk.BooleanVar(value=False))
            chk = tk.Checkbutton(frame_wheel3rd, variable=self.var_wheel3rd[i], text=str(i+1).rjust(2))
            chk_wheel3rd.append(chk)
            chk_wheel3rd[i].grid(row=math.floor(n), column=i%4)
            n += 1/4
        frame_wheel3rd.pack(side=tk.LEFT)

        frame_wheel.grid(row=2, column=2, sticky=tk.NS)

    def create_frame_box(self):

        frame_box = tk.LabelFrame(self.frame_main, padx=10, pady=10, text="Box", bg=self.bg_color)
        self.var_box = []
        chk_box = []
        n = 0.
        for i in range(8):
            self.var_box.append(tk.BooleanVar(value=False))
            chk = tk.Checkbutton(frame_box, variable=self.var_box[i], text=str(i+1).rjust(2))
            chk_box.append(chk)
            chk_box[i].grid(row=math.floor(n), column=i%8)
            n += 1/8
        frame_box.grid(row=3, column=2, columnspan=2, sticky=tk.NW)

        # frame_box_etc = tk.Frame(self.frame_main, padx=5, bg=self.bg_color)

        # frame_options = tk.LabelFrame(frame_box_etc, text="option")
        # self.chk_trn = tk.BooleanVar(value=False)
        # chk_turnup = tk.Checkbutton(frame_options, variable=self.chk_trn, text="1st<=>2nd")
        # chk_turnup.pack()
        # frame_options.pack(side="left", padx=10)

        # btn_clear = tk.Button(frame_box_etc, text="clear", command=lambda: self.check_clear())
        # btn_clear.pack(side="left", pady=6, anchor=tk.S)

        # frame_box_etc.grid(row=3, column=2, sticky=tk.NS+tk.W)

    def create_frame_output(self):
        frame_output = tk.Frame(self.frame_main, padx=3, pady=10, bg=self.bg_color)
        
        self.number_of_bets = tk.StringVar(value="")
        self.syntheic_odds = tk.StringVar(value="")
        self.expected_prob = tk.StringVar(value="")

        tag_number_of_bets = tk.Label(frame_output, text="Number of Bets:")
        label_number_of_bets = tk.Label(frame_output, textvariable=self.number_of_bets)
        tag_syntheic_odds = tk.Label(frame_output, text="Syntheic Odds:")
        label_syntheic_odds = tk.Label(frame_output, textvariable=self.syntheic_odds)
        tag_expected_prob = tk.Label(frame_output, text="Expected Prob:")
        lable_expected_prob = tk.Label(frame_output, textvariable=self.expected_prob)
        
        tag_number_of_bets.pack(side="left")
        label_number_of_bets.pack(side="left", padx=10)
        tag_syntheic_odds.pack(side="left", padx=10)
        label_syntheic_odds.pack(side="left")
        tag_expected_prob.pack(side="left", padx=10)
        lable_expected_prob.pack(side="left")

        frame_output.grid(row=4, column=0, columnspan=5, sticky=tk.NW)

    def create_frame_textbox(self):
        self.show_bets = tk.Text(self.frame_bets, width=60, height=20)
        scrollbar = tk.Scrollbar(self.frame_bets, orient=tk.VERTICAL, command=self.show_bets.yview)
        self.show_bets["yscrollcommand"] = scrollbar.set
        
        self.show_bets.grid(row=0, column=0, pady=10, sticky=tk.N+tk.S+tk.E+tk.W)
        scrollbar.grid(row=0, column=1, sticky=tk.N+tk.S)

    def create_frame_bets(self):
        frame_bet = tk.LabelFrame(self.frame_bets, text="bet")
        self.bet_var = tk.IntVar(value=1000)
        rbn_1k = tk.Radiobutton(frame_bet, value=1000, variable=self.bet_var, text=" 1000")
        rbn_3k = tk.Radiobutton(frame_bet, value=3000, variable=self.bet_var, text=" 3000")
        rbn_5k = tk.Radiobutton(frame_bet, value=5000, variable=self.bet_var, text=" 5000")
        rbn_10k = tk.Radiobutton(frame_bet, value=10000, variable=self.bet_var, text="10000")
        rbn_20k = tk.Radiobutton(frame_bet, value=20000, variable=self.bet_var, text="20000")
        rbn_30k = tk.Radiobutton(frame_bet, value=30000, variable=self.bet_var, text="30000")
        rbn_1k.pack()
        rbn_3k.pack()
        rbn_5k.pack()
        rbn_10k.pack()
        rbn_20k.pack()
        rbn_30k.pack()
        frame_bet.grid(row=0, column=2, padx=10, sticky=tk.NW)

    ''' process part '''

    def callback(self, race_number):
        def func():
            self.check_clear()
            racetitle_text = "no race"
            if race_number.isdigit():
                racetitle_text = race_number + "R " + self.races[int(race_number)-1][0][3]    
                self.race = int(race_number)
                self.entry_df = self.races[self.race-1][1]
                self.racers = []
                for i, tpl in enumerate(self.entry_df.itertuples()):
                    racer_info = tpl._2.split()
                    racer = str(i+1) + " " + " ".join(racer_info[:2])
                    self.racers.append(racer)
                self.racers += ["" for _ in range(8-len(self.racers))]
            else:
                self.racers = ["" for _ in range(8)]

            self.master.title(f"{self.dt} {self.place_jp} " + racetitle_text)
            for i in range(8):
                self.var_racers[i].set(self.racers[i])
                self.var_oddses[i].set("")

        return func

    def update(self):
        self.odds_d = odds_dict(self.dt, self.place_jp, self.race)
        win_odds = []
        for racer in self.racers:
            if racer:
                win_odds.append(self.odds_d[racer[0]])
            else:
                win_odds.append(" ")
        for i in range(8):
            self.var_oddses[i].set(win_odds[i])

    def clear_output(self):
        self.number_of_bets.set("")
        self.syntheic_odds.set("")
        self.expected_prob.set("")

    def check_clear(self):

        for w1, w2, w3, box in zip(self.var_wheel1st, self.var_wheel2nd, self.var_wheel3rd, self.var_box):
            w1.set(0)
            w2.set(0)
            w3.set(0)
            box.set(0)
            
        self.clear_output()
        self.show_bets.delete("1.0", tk.END)

    def checked_bets(self):

        wheel1st = [chk.get() for chk in self.var_wheel1st]
        w1_indexes = [i+1 for i, chk in enumerate(wheel1st) if chk]
        
        wheel2nd = [chk.get() for chk in self.var_wheel2nd]
        w2_indexes = [i+1 for i, chk in enumerate(wheel2nd) if chk]

        wheel3rd = [chk.get() for chk in self.var_wheel3rd]
        w3_indexes = [i+1 for i, chk in enumerate(wheel3rd) if chk]

        box = [chk.get() for chk in self.var_box]
        box_indexes = [i+1 for i, chk in enumerate(box) if chk]

        return w1_indexes, w2_indexes, w3_indexes, box_indexes

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
        bettype = self.var_radio.get()
        self.clear_output()
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
        elif len(chk_bets[0]) == 1 and chk_bets[1] and not chk_bets[2]:
            if bettype == 2: # exacta
                bets = [str(chk_bets[0][0]) + "-" + str(bet) for bet in chk_bets[1]]
                oddses = [self.odds_d[bet] for bet in bets]
            if bettype == 3: # quinella
                bets = [str(chk_bets[0][0]) + "=" + str(bet) for bet in chk_bets[1]]
                oddses = []
                for bet in bets:
                    try:
                        odds = self.odds_d[bet]
                    except:
                        bet = bet[2] + "=" + bet[0]
                        odds = self.odds_d[bet]
                    oddses.append(odds)

            syn_odds = self.calc_syntheic_odds(oddses)
            selections = [(str(bet), odds) for bet, odds in zip(bets, oddses)]
            self.output_for_textbox(syn_odds, selections)

    def output_for_textbox(self, synodds, selections):
        self.show_bets.delete("1.0", tk.END)
        self.number_of_bets.set(len(selections))
        self.syntheic_odds.set(round(synodds, 1))
        p = 1.5 * 0.75 / synodds
        self.expected_prob.set(round(p, 2))
        
        amount_of_coins = self.bet_var.get()
        amount = 0
        for bet, odds in selections:
            coins = amount_of_coins * synodds / odds
            each_coins = int(round(coins, -2))
            if not each_coins:
                each_coins = 100
            each_payout = round(odds * each_coins)
            amount += each_coins
            txt = " " + str(bet) + str(odds).rjust(7) + str(each_coins).rjust(7) + str(each_payout).rjust(7)
            self.outputs.append(txt) 
        txt = " amount: " + str(amount).rjust(6)
        self.outputs.append(txt)
        for output in self.outputs:
            self.show_bets.insert(tk.END, output + "\n")

    def run(self):
        self.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = Application(master=root)
    app.run()