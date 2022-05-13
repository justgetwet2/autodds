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
        self.odds  = 0.
        self.selections = []


        self.master.title(f"{self.dt} {self.place_jp}")
        self.frame_upper = tk.Frame(self, padx=10, pady=3)
        self.frame_lower = tk.Frame(self, padx=10, pady=3)
        self.frame_status = tk.Frame(self)

        self.bg_color = self.master.cget("background")
        self.textbox_bg_color = "GhostWhite"
        # self.bg_color = "pink"

        self.grid_propagate(False) # 子フレームのgridに対し親フレームサイズ固定
        self.create_frame_races()
        # self.create_frame_racetitle()
        self.create_frame_buttons()
        self.create_frame_racers()
        self.create_frame_oddses()
        self.create_frame_bettype()
        self.create_frame_wheel()
        self.create_frame_combination()
        self.create_frame_expected_value()
        self.frame_upper.pack()
        
        self.create_frame_textbox()
        self.create_frame_bets()
        self.frame_lower.pack(fill=tk.X)

        self.create_status_bar()
        self.frame_status.pack(fill=tk.X)
        
        self.pack()

    ''' create part '''

    def create_status_bar(self):
        status_bar = tk.Label(self.frame_status, text="status", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(fill=tk.X)

    def create_frame_races(self):
        frame_races = tk.Frame(self.frame_upper, bg=self.bg_color)
        race_numbers = [race[0][2] for race in self.races if race[0]]
        race_numbers += ["-" for _ in range(12-len(race_numbers))]
        buttons = []
        for i, num in enumerate(race_numbers):
            button = tk.Button(frame_races, text=f"{num}", command=self.callback(num))
            buttons.append(button)
            buttons[i].pack(side=tk.LEFT, padx=2)

        frame_races.grid(row=0, column=0, columnspan=3, sticky=tk.W)

    def create_frame_buttons(self):
        frame_buttons = tk.Frame(self.frame_upper, pady=10, bg=self.bg_color)

        btn_update = tk.Button(frame_buttons, text="update", command=lambda: self.update())
        btn_update.pack(side=tk.LEFT, padx=5)

        btn_calc = tk.Button(frame_buttons, text="calc", command=lambda: self.calc())
        btn_calc.pack(side=tk.LEFT, padx=5)     

        btn_add = tk.Button(frame_buttons, text="add", command=lambda: self.add_calc())
        btn_add.pack(side=tk.LEFT, padx=5)     

        frame_buttons.grid(row=0, column=3) #, sticky=tk.NE)

    def create_frame_racers(self):
        self.entry_df = self.races[0][1]
        self.racers = []
        for i, tpl in enumerate(self.entry_df.itertuples()):
            racer_info = tpl._2.split()
            racer = str(i+1) + " " + " ".join(racer_info[:2])
            self.racers.append(racer)
        self.racers += ["" for _ in range(8-len(self.racers))]

        frame_racers = tk.Frame(self.frame_upper, padx=5, pady=5, bg=self.bg_color)
        self.var_racers = []
        label_racers = []
        for i in range(8):
            self.var_racers.append(tk.StringVar())
            self.var_racers[i].set(self.racers[i])
            label_racers.append(tk.Label(frame_racers, textvariable=self.var_racers[i]))
            label_racers[i].pack(anchor=tk.W)
        
        frame_racers.grid(row=1, column=0, rowspan=4, sticky=tk.NW)

    def create_frame_oddses(self):

        frame_oddses = tk.Frame(self.frame_upper, padx=5, pady=5, bg=self.bg_color)

        frame_win_oddses = tk.Frame(frame_oddses)
        self.var_win_oddses = [tk.StringVar() for _ in range(8)]
        win_labels = []
        for i in range(8):
            self.var_win_oddses[i].set(" ")
            win_labels.append(tk.Label(frame_win_oddses, textvariable=self.var_win_oddses[i]))
            win_labels[i].pack(anchor=tk.E)

        frame_place1_oddses = tk.Frame(frame_oddses)
        self.var_place1_oddses = [tk.StringVar() for _ in range(8)]
        place1_labels = []
        for i in range(8):
            self.var_place1_oddses[i].set(" ")
            place1_labels.append(tk.Label(frame_place1_oddses, textvariable=self.var_place1_oddses[i]))
            place1_labels[i].pack(anchor=tk.E)

        frame_place_bars = tk.Frame(frame_oddses)
        self.var_place_bars = [tk.StringVar() for _ in range(8)]
        bar_labels = []
        for i in range(8):
            self.var_place_bars[i].set(" ")
            bar_labels.append(tk.Label(frame_place_bars, textvariable=self.var_place_bars[i]))
            bar_labels[i].pack()

        frame_place2_oddses = tk.Frame(frame_oddses)
        self.var_place2_oddses = [tk.StringVar() for _ in range(8)]
        place2_labels = []
        for i in range(8):
            self.var_place2_oddses[i].set(" ")
            place2_labels.append(tk.Label(frame_place2_oddses, textvariable=self.var_place2_oddses[i]))
            place2_labels[i].pack(anchor=tk.E)

        frame_win_oddses.pack(side="left", padx=10)
        frame_place1_oddses.pack(side="left", padx=5)
        frame_place_bars.pack(side="left")
        frame_place2_oddses.pack(side="left", padx=5)

        frame_oddses.grid(row=1, column=1, rowspan=4, sticky=tk.NW)

    def create_frame_bettype(self):
        frame_bettype = tk.LabelFrame(self.frame_upper, pady=5, text="bet type")
        self.var_bettype = tk.IntVar(value=0)
        bettypes = "all", "win", "exacta", "quinella", "trifecta", "trio", "wide"
        radiobuttons = []
        for i, text in enumerate(bettypes):
            rbn = tk.Radiobutton(frame_bettype, value=i, variable=self.var_bettype, text=text)
            radiobuttons.append(rbn)
            radiobuttons[i].pack(side=tk.LEFT)

        frame_bettype.grid(row=1, column=2, columnspan=3, sticky=tk.NW)

    def create_frame_wheel(self):

        frame_wheel = tk.LabelFrame(self.frame_upper, padx=10, pady=5, text="Wheel", bg=self.bg_color)

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

        frame_wheel.grid(row=2, column=2, columnspan=3, sticky=tk.NW)

    def create_frame_combination(self):

        frame_combination = tk.Frame(self.frame_upper, pady=10, bg=self.bg_color)
        frame_box = tk.LabelFrame(frame_combination, padx=5, pady=5, text="Box")
        self.var_box = []
        chk_box = []
        n = 0.
        for i in range(8):
            self.var_box.append(tk.BooleanVar(value=False))
            chk = tk.Checkbutton(frame_box, variable=self.var_box[i], text=str(i+1).rjust(2))
            chk_box.append(chk)
            chk_box[i].grid(row=math.floor(n), column=i%8)
            n += 1/8
        frame_box.pack(side=tk.LEFT)

        frame_option = tk.LabelFrame(frame_combination, padx=5, pady=5, text="option")
        self.chk_trn = tk.BooleanVar(value=False)
        chk_turnup = tk.Checkbutton(frame_option, variable=self.chk_trn, text="1st<=>2nd")
        chk_turnup.pack()
        frame_option.pack(side=tk.LEFT, padx=10)
        frame_combination.grid(row=3, column=2, columnspan=3, sticky=tk.NW)

    def create_frame_expected_value(self):
        frame_expected_value = tk.Frame(self.frame_upper, padx=3, pady=10, bg=self.bg_color)
        
        self.number_of_bets = tk.StringVar(value="")
        self.syntheic_odds = tk.StringVar(value="")
        self.expected_prob = tk.StringVar(value="")

        tag_number_of_bets = tk.Label(frame_expected_value, text="Number of Bets:")
        label_number_of_bets = tk.Label(frame_expected_value, textvariable=self.number_of_bets)
        tag_syntheic_odds = tk.Label(frame_expected_value, text="Syntheic Odds:")
        label_syntheic_odds = tk.Label(frame_expected_value, textvariable=self.syntheic_odds)
        tag_expected_prob = tk.Label(frame_expected_value, text="Expected Prob:")
        lable_expected_prob = tk.Label(frame_expected_value, textvariable=self.expected_prob)
        
        tag_number_of_bets.pack(side=tk.LEFT)
        label_number_of_bets.pack(side=tk.LEFT, padx=10)
        tag_syntheic_odds.pack(side=tk.LEFT, padx=10)
        label_syntheic_odds.pack(side=tk.LEFT)
        tag_expected_prob.pack(side=tk.LEFT, padx=10)
        lable_expected_prob.pack(side=tk.LEFT)

        frame_expected_value.grid(row=4, column=2, columnspan=3, sticky=tk.NW)

    def create_frame_textbox(self):
        self.textbox = tk.Text(self.frame_lower, width=60, height=20, bg=self.textbox_bg_color)
        scrollbar = tk.Scrollbar(self.frame_lower, orient=tk.VERTICAL, command=self.textbox.yview)
        self.textbox["yscrollcommand"] = scrollbar.set
        
        self.textbox.grid(row=0, column=0, pady=10, sticky=tk.N+tk.S+tk.E+tk.W)
        scrollbar.grid(row=0, column=1, sticky=tk.N+tk.S)

    def create_frame_bets(self):
        frame_bet = tk.LabelFrame(self.frame_lower, text="bet")
        self.var_bet = tk.IntVar(value=1000)
        bets = [1000, 3000, 6000, 10000, 20000, 30000]
        radiobuttons = []
        for i, bet in enumerate(bets):
            rbn = tk.Radiobutton(frame_bet, value=bet, variable=self.var_bet, text=str(bet).rjust(6))
            radiobuttons.append(rbn)
            radiobuttons[i].pack()

        frame_bet.grid(row=0, column=2, padx=10, sticky=tk.NW)

    ''' process part '''

    def callback(self, race_number):
        def func():
            self.clear_checkbox()
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
                self.var_win_oddses[i].set("")
                self.var_place1_oddses[i].set("")
                self.var_place_bars[i].set("")
                self.var_place2_oddses[i].set("")

        return func

    def update(self):
        self.odds_d = odds_dict(self.dt, self.place_jp, self.race)

        win_oddses = [self.odds_d[racer[0]] for racer in self.racers if racer]
        win_oddses += [" " for _ in range(8-len(win_oddses))]
        p1_oddses = [self.odds_d["(" + racer[0]] for racer in self.racers if racer]
        p1_oddses += [" " for _ in range(8-len(p1_oddses))]      
        p2_oddses = [self.odds_d[racer[0] + ")"] for racer in self.racers if racer]
        p2_oddses += [" " for _ in range(8-len(p2_oddses))]
        for i in range(8):
            self.var_win_oddses[i].set(win_oddses[i])
            self.var_place1_oddses[i].set(p1_oddses[i]) 
            self.var_place_bars[i].set("-")
            self.var_place2_oddses[i].set(p2_oddses[i])  

        if self.selections:
            oddses = []
            for ticket, odds in self.selections:
                new_odds = self.odds_d[ticket]
                oddses.append(new_odds)
            self.odds = self.calc_syntheic_odds(oddses)
            self.betting_slip()



    def clear_output(self):
        self.textbox.delete("1.0", tk.END)
        self.number_of_bets.set("")
        self.syntheic_odds.set("")
        self.expected_prob.set("")

    def clear_checkbox(self):
        self.clear_output()
        for w1, w2, w3, box in zip(self.var_wheel1st, self.var_wheel2nd, self.var_wheel3rd, self.var_box):
            w1.set(0)
            w2.set(0)
            w3.set(0)
            box.set(0)

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
        synodds = self.calc_syntheic_odds(oddses)
        sellctions = [(str(bet), odds) for bet, odds in zip(bets, oddses)]

        return synodds, sellctions

    def calc_permutation(self, bets, cmb=2):
        selections, oddses = [], []
        for pair in itertools.permutations(bets, cmb):
            bet = str(pair[0]) + "-" + str(pair[1])
            if cmb == 3:
                bet += "-" + str(pair[2])
            odds = self.odds_d[bet]
            oddses.append(odds)
            selections.append((bet, odds))
        synodds = self.calc_syntheic_odds(oddses)

        return synodds, selections

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
        synodds = self.calc_syntheic_odds(oddses)

        return synodds, selections

    def calculation(self):
        chk_bets = self.checked_bets()
        bettype = self.var_bettype.get()
        synodds = 0.
        selections = []
        
        # self.clear_output()
        self.outputs = []

        if chk_bets[3]: # box
            bets = chk_bets[3]
            win_synodds, win_selections = self.calc_wins(bets)
            exa_synodds, exa_selections = self.calc_permutation(bets)
            qin_synodds, qin_selections = self.calc_combination(bets)
            trf_synodds, trf_selections = self.calc_permutation(bets, cmb=3)    
            tro_synodds, tro_selections = self.calc_combination(bets, cmb=3)
            wid_synodds, wid_selections = self.calc_combination(bets, wide=True)
            if bettype == 0: # all
                win_txt = "win :    " + str(len(win_selections)).rjust(3) + str(round(win_synodds, 1)).rjust(6)
                exa_txt = "exacta : " + str(len(exa_selections)).rjust(3) + str(round(exa_synodds,1)).rjust(6)
                qin_txt = "quinella:" + str(len(qin_selections)).rjust(3) + str(round(qin_synodds,1)).rjust(6)
                trf_txt = "trifecta:" + str(len(trf_selections)).rjust(3) + str(round(trf_synodds, 1)).rjust(6)
                tro_txt = "trio :   " + str(len(tro_selections)).rjust(3) + str(round(tro_synodds,1)).rjust(6)
                wid_txt = "wide :   " + str(len(wid_selections)).rjust(3) + str(round(wid_synodds,1)).rjust(6)
                self.outputs = [win_txt, exa_txt, qin_txt, trf_txt, tro_txt, wid_txt]
                self.textbox.delete("1.0", tk.END)
                self.textbox.insert(tk.END, "*** Combinations ***" + "\n")
                for output in self.outputs:
                    self.textbox.insert(tk.END, output + "\n")

            if bettype == 1: # win
                synodds, selections = win_synodds, win_selections
            if bettype == 2: # exacta
                synodds, selections = exa_synodds, exa_selections
            if bettype == 3: # quinella
                synodds, selections = qin_synodds, qin_selections 
            if bettype == 4: # tierce
                synodds, selections = trf_synodds, trf_selections   
            if bettype == 5: # trio
                synodds, selections = tro_synodds, tro_selections     
            if bettype == 6: # wide
                synodds, selections = wid_synodds, wid_selections
        # Wheel
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
        elif len(chk_bets[0]) == 1 and len(chk_bets[1]) == 1 and chk_bets[2]:
            if bettype == 4: # trifecta
                head = str(chk_bets[0][0]) + "-" + str(chk_bets[1][0]) + "-"
                bets = [head + str(bet) for bet in chk_bets[2]]
                oddses = [self.odds_d[bet] for bet in bets]

            synodds = self.calc_syntheic_odds(oddses)
            selections = [(str(bet), odds) for bet, odds in zip(bets, oddses)]

        #     self.odds, self.selections = synodds, selections
        # self.betting_slip()
        return synodds, selections

    def calc(self):
        self.odds, self.selections = self.calculation()
        self.betting_slip()

    def add_calc(self):
        synodds, selections = self.calculation()
        odds_l = [self.odds, synodds]
        self.odds = self.calc_syntheic_odds(odds_l)
        self.selections += selections
        self.betting_slip()

    def betting_slip(self):

        if not self.odds:
            return
        self.outputs = []
        synodds, selections = self.odds, self.selections

        self.number_of_bets.set(len(selections))
        self.syntheic_odds.set(round(synodds, 1))
        if synodds:
            p = 1.5 * 0.75 / synodds
            self.expected_prob.set(round(p, 2))
        
        self.textbox.delete("1.0", tk.END)
        self.outputs.append("*** Bet distribution ***")

        amount_of_bets = self.var_bet.get()
        amount = 0
        payouts = []
        surplus = ["", "*** Surplus bets ***"]
        for ticket, odds in selections:
            f_bet = amount_of_bets * synodds / odds
            bet = int(round(f_bet, -2))
            if not bet:
                bet = 100
            payout = round(odds * bet)
            payouts.append(payout)
            amount += bet
            txt = " " + str(ticket) + str(odds).rjust(7) + str(bet).rjust(7) + str(payout).rjust(7)
            self.outputs.append(txt) 
            if bet > 100:
                txt = " " + str(ticket).ljust(8) + str(bet-100).rjust(11)
                surplus.append(txt)

        min_payout, max_payout = min(payouts), max(payouts)
        txt = " amount: " + str(amount).rjust(6) + str(min_payout).rjust(10) + " - " + str(max_payout)
        self.outputs.append("")
        self.outputs.append(txt)

        for output in self.outputs:
            self.textbox.insert(tk.END, output + "\n")

        if len(surplus) > 2:
            for output in surplus:
                self.textbox.insert(tk.END, output + "\n")

    def run(self):
        self.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = Application(master=root)
    app.run()