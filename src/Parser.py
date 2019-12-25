# importing the requests library
import csv
import logging
import os
from datetime import date

import requests
from bs4 import BeautifulSoup

WORLDS_LIST = ("Antica",
               "Assombra",
               "Astera",
               "Belluma",
               "Belobra",
               "Bona",
               "Calmera",
               "Carnera",
               "Celebra",
               "Celesta",
               "Concorda",
               "Cosera",
               "Damora",
               "Descubra",
               "Dibra",
               "Duna",
               "Epoca",
               "Estela",
               "Faluna",
               "Ferobra",
               "Firmera",
               "Funera",
               "Furia",
               "Garnera",
               "Gentebra",
               "Gladera",
               "Harmonia",
               "Helera",
               "Honbra",
               "Impera",
               "Inabra",
               "Jonera",
               "Kalibra",
               "Kenora",
               "Lobera",
               "Luminera",
               "Lutabra",
               "Macabra",
               "Menera",
               "Mitigera",
               "Monza",
               "Nefera",
               "Noctera",
               "Nossobra",
               "Olera",
               "Ombra",
               "Pacera",
               "Peloria",
               "Premia",
               "Pyra",
               "Quelibra",
               "Quintera",
               "Refugia",
               "Relania",
               "Relembra",
               "Secura",
               "Serdebra",
               "Serenebra",
               "Solidera",
               "Talera",
               "Torpera",
               "Tortura",
               "Venebra",
               "Vita",
               "Vunira",
               "Wintera",
               "Zuna",
               "Zunera",
               )

DIRECTORY_PATH = "worlds/"
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Parser:
    # api-endpoint
    URL = "https://www.tibia.com/community/?subtopic=killstatistics"

    def send_url_request(self, world):
        # defining a params dict for the parameters to be sent to the API
        post_data = {'world': world, 'Submit.x': '85', 'Submit.y': '16'}
        # sending get request and saving the response as response object
        r = requests.post(url=self.URL, data=post_data)
        logger.info(f"Parsing : {world}")
        return r.content

    def parse_url(self, data):
        soup = BeautifulSoup(data, features="html.parser")
        table = soup.find('table', cellspacing=1, cellpadding=3)
        dict_results = [y.get_text().replace("\xa0", '') for (row, y) in enumerate(table.find_all('td')[8:]) if
                        row % 5 <= 2]

        return dict_results


def save_to_csv(dict_data, file_name, date):
    csv_columns = ['No', 'Kills']
    file_name = f'{file_name}_{date}.csv'
    full_path = os.path.join(DIRECTORY_PATH, file_name)
    print(f"{full_path}")
    try:
        with open(full_path, 'w') as f:
            writer = csv.DictWriter(f, fieldnames=csv_columns)
            writer.writeheader()
            data = [dict(zip(csv_columns, [k, v])) for k, v in dict_data.items()]
            writer.writerows(data)
    except IOError:
        logger.error("I/O error")


def save_list_to_csv(list_data, file_name, date):
    file_name = f'{file_name}_{date}.csv'
    full_path = os.path.join(DIRECTORY_PATH, file_name)
    print(f"{full_path}")
    try:
        with open(full_path, 'w', newline='') as myfile:
            wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
            wr.writerow(list_data)
    except IOError:
        logger.error("I/O error")


if __name__ == '__main__':
    parser = Parser()
    # data = parser.send_url_request('Antica')
    today = date.today()
    date = today.strftime("%d_%m_%Y")
    for world in WORLDS_LIST:
        data = parser.send_url_request(world)
        parsed_data = parser.parse_url(data)
        save_list_to_csv(parsed_data, world, date)
    # data_website = parser.parse_url(data)
    # save_list_to_csv(data_website, "test")
    # logging.info(data_website)
