from src import KillStats
TEST_WORLD = "Zunera"
TEST_DATE = "04_11_2019"


def test_ehlo():
    global_mobs_list = []
    filename = f"worlds/{TEST_WORLD}_{TEST_DATE}.csv"

    list_from_date = KillStats.read_csv_file(filename, TEST_WORLD)
    global_mobs_list.append(list_from_date)

    temp_list = KillStats.get_top_5_killed_monster()
    for i in temp_list:
        print(i.name, i.death_numb, i.world, i.date_stats)
    # assert response == 250
    assert 0