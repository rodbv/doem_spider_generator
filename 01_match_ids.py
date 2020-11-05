import csv
from unidecode import unidecode
from string import capwords

# cities which didn't redirect, from check_cities.py
cities = [
    ("al", "jaramataia"),
    ("al", "satuba"),
    ("ba", "acajutiba"),
    ("ba", "alagoinhas"),
    ("ba", "alcobaca"),
    ("ba", "antoniocardoso"),
    ("ba", "baianopolis"),
    ("ba", "baixagrande"),
    ("ba", "banzae"),
    ("ba", "barradochoca"),
    ("ba", "barradomendes"),
    ("ba", "barreiras"),
    ("ba", "barrocas"),
    ("ba", "belmonte"),
    ("ba", "biritinga"),
    ("ba", "boanova"),
    ("ba", "brotasdemacaubas"),
    ("ba", "cachoeira"),
    ("ba", "cacule"),
    ("ba", "caetanos"),
    ("ba", "camamu"),
    ("ba", "campoalegredelourdes"),
    ("ba", "campoformoso"),
    ("ba", "canapolis"),
    ("ba", "canavieiras"),
    ("ba", "cansancao"),
    ("ba", "canudos"),
    ("ba", "capsej"),
    ("ba", "catolandia"),
    ("ba", "catu"),
    ("ba", "cdsterritoriolitoralnorteeagrestebaiano"),
    ("ba", "cdstlnab"),
    ("ba", "cdstpni"),
    ("ba", "cicerodantas"),
    ("ba", "cipo"),
    ("ba", "cisan"),
    ("ba", "coisan"),
    ("ba", "conceicaodafeira"),
    ("ba", "consan"),
    ("ba", "consorcioconsisal"),
    ("ba", "consorcioportaldosertao"),
    ("ba", "correntina"),
    ("ba", "dariomeira"),
    ("ba", "diasdavila"),
    ("ba", "ericocardoso"),
    ("ba", "florestaazul"),
    ("ba", "gentiodoouro"),
    ("ba", "gongogi"),
    ("ba", "governadormangabeira"),
    ("ba", "guaratinga"),
    ("ba", "heliopolis"),
    ("ba", "ibiquera"),
    ("ba", "idesba"),
    ("ba", "inhambupe"),
    ("ba", "ipcf"),
    ("ba", "insv"),
    ("ba", "ipiau"),
    ("ba", "ipira"),
    ("ba", "irara"),
    ("ba", "irece"),
    ("ba", "itabela"),
    ("ba", "itambe"),
    ("ba", "itanagra"),
    ("ba", "itapetinga"),
    ("ba", "ituacu"),
    ("ba", "jaguarari"),
    ("ba", "joaodourado"),
    ("ba", "juazeiro"),
    ("ba", "jussara"),
    ("ba", "laje"),
    ("ba", "luiseduardomagalhaes"),
    ("ba", "macajuba"),
    ("ba", "mascote"),
    ("ba", "medeirosneto"),
    ("ba", "modelo"),
    ("ba", "montesanto"),
    ("ba", "morrodochapeu"),
    ("ba", "mucuri"),
    ("ba", "mundonovo"),
    ("ba", "muritiba"),
    ("ba", "oliveiradosbrejinhos"),
    ("ba", "pedeserra"),
    ("ba", "pedrao"),
    ("ba", "pedroalexandre"),
    ("ba", "pindobacu"),
    ("ba", "pontonovo"),
    ("ba", "prado"),
    ("ba", "queimadas"),
    ("ba", "ribeiradoamparo"),
    ("ba", "ribeiradopombal"),
    ("ba", "rodelas"),
    ("ba", "santacruzcabralia"),
    ("ba", "santoamaro"),
    ("ba", "santoestevao"),
    ("ba", "saofranciscodoconde"),
    ("ba", "saogoncalodoscampos"),
    ("ba", "saojosedojacuipe"),
    ("ba", "saude"),
    ("ba", "senhordobonfim"),
    ("ba", "sentose"),
    ("ba", "serrapreta"),
    ("ba", "serrinha"),
    ("ba", "sitiodomato"),
    ("ba", "sitiodoquinto"),
    ("ba", "tabocasdobrejovelho"),
    ("ba", "teixeiradefreitas"),
    ("ba", "teolandia"),
    ("ba", "tucano"),
    ("ba", "uaua"),
    ("ba", "varzeadaroca"),
    ("ba", "xiquexique"),
    ("ba", "saaealagoinhas"),
    ("pe", "petrolina"),
    ("se", "indiaroba"),
]


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


def save_spider_file(filename, spider_code):
    with open(filename, "w") as spider_file:
        spider_file.write(spider_code)


def save_spiders(matched_cities):
    template_file = open("spider_template.py", mode="r")
    template = template_file.read()
    for (territory_id, state, city, city_full) in matched_cities:
        filename = f"{state}_{city}.py"
        class_name = get_class_name(state, city_full)
        # print('Spawning', class_name, '...')
        spider_code = (
            template.replace("{className}", class_name)
            .replace("{territory_id}", territory_id)
            .replace("{state}", state)
            .replace("{city}", city)
        )
        # save_spider_file(filename, spider_code)


def main():
    territories = load_territories()
    matched = []
    not_matched = []
    for (state, city) in cities:
        for (territory_id, t_city, t_city_name, t_state) in territories:
            if t_city == city and t_state == state:
                print(
                    f"https://doem.org.br/{state}/{city}/pesquisar?data_inicial=2010-01-01"
                )
                matched.append((territory_id, state, city, t_city_name))
                break
        else:
            not_matched.append((state, city))
    save_spiders(matched)


if __name__ == "__main__":
    main()
