import csv
import os
from string import capwords
from unidecode import unidecode
from datetime import datetime


def normalize(city):
    return unidecode(city).lower().replace(" ", "")


def get_class_name(state, city):
    city_name = capwords(city).replace(" ", "")
    return f"{state.capitalize()}{city_name}Spider"


def load_territories():
    with open("territories.csv") as csvfile:
        rows = csv.reader(csvfile, delimiter=",")
        return [
            [id, normalize(city), capwords(unidecode(city)), normalize(state)]
            for [id, city, state, _] in rows
        ]


def load_cities():
    with open("cities_ok.csv") as csvfile:
        rows = csv.reader(csvfile, delimiter=",")
        return [[state, city] for [state, city, _] in rows]


def save_spiders(directory, matched_cities):
    template_file = open("spider_template", mode="r")
    template = template_file.read()
    for (territory_id, state, city, city_full) in matched_cities:
        filename = f"{state}_{city}.py"
        class_name = get_class_name(state, city_full)
        print("Spawning", class_name, "...")
        spider_code = (
            template.replace("{className}", class_name)
            .replace("{territory_id}", territory_id)
            .replace("{state}", state)
            .replace("{city}", city)
        )
        with open(os.path.join(directory, filename), "w") as spider_file:
            spider_file.write(spider_code)


def main():
    territories = load_territories()
    matched = []
    not_matched = []
    cities = load_cities()
    directory = os.path.join("spiders", datetime.now().strftime("%Y_%m_%d_%s"))
    os.makedirs(directory)

    for (state, city) in cities:
        for (territory_id, t_city, t_city_name, t_state) in territories:
            if t_city == city and t_state == state:
                matched.append((territory_id, state, city, t_city_name))
                break
        else:
            not_matched.append([state, city])
    save_spiders(directory, matched)
    # print(not_matched)
    # with open(os.path.join(directory, "not_matched.csv"), "w") as not_matched_file:
    x = [f"{state},{city}\n" for [state, city] in not_matched]
    with open(os.path.join(directory, "0_not_matched.csv"), "w") as not_matched_file:
        not_matched_file.writelines(x)


if __name__ == "__main__":
    main()
