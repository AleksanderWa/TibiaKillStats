import csv
import operator
import re
from collections import Counter
from itertools import zip_longest, product
from operator import attrgetter

from Parser import WORLDS_LIST

date_regex = '([0-9]{2}\_[0-9]{2}\_[0-9]{4})'
global_mobs_list = []
max_killed_list = []
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
                if mod_value==0:
                    if column.startswith('Total'):
                        # print("DUPA")
                        break
                    name = column
                elif mod_value==1:
                    killed = column
                elif mod_value==2:
                    deaths = column
                    mob = Monster(name, int(deaths), int(killed), date.group(), world)
                    temp_mobs.append(mob)

    return {date.group(): temp_mobs}


def get_highest_kill_count():
    """
    :return: dict with top 5 killed mobs on all worlds
    """

    for days in global_mobs_list:
        for date, monsters in days.items():
            max_nmb_creatre_creatre = max(monsters, key=attrgetter('death_numb'))
            max_killed_list.append(max_nmb_creatre_creatre)

    c = Counter()
    for monster in max_killed_list:
        c.update({monster.name: monster.death_numb})

    # mx = max(c, key=lambda key: c[key])

    _sorted = sorted(c, key=lambda key: c[key], reverse=True)

    top_5_killed = {x: c.get(x) for x in _sorted[:5]}



    return top_5_killed


def _get_worlds_for_given_monster(max_killed_list, mob_name):
    monster_world_collection = [i for i in max_killed_list if mob_name==i.name]
    return monster_world_collection


if __name__=='__main__':
    for world, date in product(WORLDS_LIST, DATES):
        # print(date, world)
        filename = f"worlds/{world}_{date}.csv"
        # print(f"processing : {world}")
        list_from_date = read_csv_file(filename, world)
        global_mobs_list.append(list_from_date)

    top5_killed_mob = get_highest_kill_count()
    print(f"MOSTLY KILLED MONSTERS : {list(top5_killed_mob.keys())[0]}")
    temp_list = _get_worlds_for_given_monster(max_killed_list, list(top5_killed_mob.keys())[0])
    temp_list.sort(key=attrgetter('death_numb'), reverse=True)
    for i in temp_list[:5]:
        print(i.name, i.death_numb, i.world)
