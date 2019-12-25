import csv
import re
from collections import Counter
from itertools import product
from operator import attrgetter

from src.Parser import WORLDS_LIST

date_regex = '([0-9]{2}\_[0-9]{2}\_[0-9]{4})'
DATES = ("23_12_2019", "24_12_2019", "25_12_2019", "26_12_2019", "27_12_2019")


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
                        break
                    name = column
                elif mod_value == 1:
                    killed = column
                elif mod_value == 2:
                    deaths = column
                    mob = Monster(name, int(deaths), int(killed), date.group(), world)
                    temp_mobs.append(mob)

    return {date.group(): temp_mobs}


def get_highest_kill_count(max_count_list, count_for):
    """
    :return: dict with top 5 killed mobs on all worlds
    """

    for days in global_mobs_list:
        for date, monsters in days.items():
            max_nmb_creatre_creatre = max(monsters, key=attrgetter(count_for))
            max_count_list.append(max_nmb_creatre_creatre)

    c = Counter()

    if count_for == "death_numb":
        for monster in max_count_list:
            c.update({monster.name: monster.death_numb})
    elif count_for == "killed_players":
        for monster in max_count_list:
            c.update({monster.name: monster.killed_players})

    # mx = max(c, key=lambda key: c[key])

    _sorted = sorted(c, key=lambda key: c[key], reverse=True)

    top_5_killed = {x: c.get(x) for x in _sorted[:10]}
    return top_5_killed


def _get_worlds_for_given_monster(max_killed_list, mob_name):
    monster_world_collection = [monster for monster in max_killed_list if mob_name == i.name]
    return monster_world_collection


def get_top_5_killed_monster():
    max_killed_list = []
    top5_killed_mob = get_highest_kill_count(max_killed_list, "death_numb")
    mostly_killed_monster = list(top5_killed_mob.items())[4]
    print(f"MOSTLY KILLED MONSTERS : {mostly_killed_monster}")
    temp_list = _get_worlds_for_given_monster(max_killed_list, list(top5_killed_mob.keys())[0])
    temp_list.sort(key=attrgetter('death_numb'), reverse=True)
    return temp_list[:5]

if __name__ == '__main__':
    global_mobs_list = []
    for world, date in product(WORLDS_LIST, DATES):
        filename = f"worlds/{world}_{date}.csv"

        list_from_date = read_csv_file(filename, world)
        global_mobs_list.append(list_from_date)

    for i in get_top_5_killed_monster():
        print(i.name, i.death_numb, i.world, i.date_stats)

    # max_killed_players = []
    # top5_mob_killers = get_highest_kill_count(max_killed_players, "killed_players")
    # mostly_deadly_monsters = list(top5_mob_killers.items())[0]
    # print(f"THE MOST DEADLY  MONSTERS : {mostly_deadly_monsters}")
    # temp_list = _get_worlds_for_given_monster(max_killed_players, list(top5_mob_killers.keys())[1])
    # temp_list.sort(key=attrgetter('killed_players'), reverse=True)
    # for i in temp_list[:5]:
    #     print(i.name, i.killed_players, i.world, i.date_stats)

    death_sum = 0
    killed_players = 0
    for days in global_mobs_list:
        for date, monsters in days.items():
            death_sum += sum(m.death_numb for m in monsters)
            killed_players += sum(m.killed_players for m in monsters)

    print(f"ALL MONSTERS KILLED : {death_sum} KILLED PLAYERS : {killed_players}")
