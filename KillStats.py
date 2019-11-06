import csv, pandas
import re
from collections import Counter
from itertools import zip_longest, product
from operator import attrgetter

from Parser import WORLDS_LIST

date_regex = '([0-9]{2}\_[0-9]{2}\_[0-9]{4})'
global_mobs_list = []
DATES = ("02_11_2019", "03_11_2019", "04_11_2019")

class Monster:
    def __init__(self, name, death_numb, killed_players, date_stats, world):
        self.name = name
        self.death_numb = death_numb
        self.killed_players = killed_players
        self.date_stats = date_stats
        self.world = world
    def __str__(self):
        return self.name
def read_csv_file(filename, world):
    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        date = re.search(date_regex, filename)
        # print(f"DATE : {date.group()} type: {type(date.group())}")
        name, killed, deaths = ['', '', '']
        temp_mobs = []
        for row in csv_reader:
            # print(f"numb : {numb} row : {row}")
            for numb, column in enumerate(row):
                mod_value = numb % 3
                if mod_value == 0:
                    if column.startswith('Total'):
                        # print("DUPA")
                        break
                    name = column
                elif mod_value == 1:
                    killed = column
                elif mod_value == 2:
                    deaths = column
                    mob = Monster(name, int(deaths), int(killed), date.group(), world)
                    temp_mobs.append(mob)
                    # global_mobs_list.append(mob)

    return {date.group() : temp_mobs}

def get_highest_kill_count():
    max_killed_list = []
    for days in global_mobs_list:
        for date, monsters in days.items():
            monsters.sort(key=lambda x: x.death_numb, reverse=True)
            # max_killed_list.append(max(y, key=lambda i: i.death_numb) for x,y in days.items())
            max_nmb_creatre_creatre = max(monsters, key=attrgetter('death_numb'))
            max_killed_list.append(max_nmb_creatre_creatre)
            # print(f"MAX : {max_nmb_creatre_creatre} , {max_nmb_creatre_creatre.death_numb} world : {max_nmb_creatre_creatre.world} date: {max_nmb_creatre_creatre.date_stats}")

    c = Counter()
    for monster in max_killed_list:
        c.update({monster.name: monster.death_numb})
    print(max(c.values()))
    top_5_total_highes_killed_mob = max_killed_list.sort(key=lambda x : x.death_numb, reverse=True)
    return top_5_total_highes_killed_mob

if __name__ == '__main__':
    for world, date in product(WORLDS_LIST, DATES):
        # print(date, world)
        filename = f"worlds/{world}_{date}.csv"
        # print(f"processing : {world}")
        list_from_date = read_csv_file(filename, world)
        global_mobs_list.append(list_from_date)

    top1_killed_mob = get_highest_kill_count()
    #print(top1_killed_mob.death_numb, top1_killed_mob.world)
