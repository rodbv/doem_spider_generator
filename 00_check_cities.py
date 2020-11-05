import requests
import csv


def get_cities():
    header = "state,city,url,redirect,in_use\n"
    with open("cities.csv") as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        rows = [row for row in reader if len(row) == 2]
        cities = []
        [cities.append(city) for city in rows if city not in cities]
        ok = []
        redirects = []
        for row in cities:
            state, city = row
            url = (
                f"https://doem.org.br/{state}/{city}/pesquisar?data_inicial=2005-01-01"
            )
            line = f"{state},{city},{url},?,?\n"

            r = requests.get(url)
            has_redirect = len(r.history) > 0

            if has_redirect:
                redirects.append(line)
            else:
                ok.append(line)

        with open(f"cities_ok.csv", "w") as cities_ok:
            cities_ok.write(header)
            cities_ok.writelines(ok)
        with open(f"cities_redirect.csv", "w") as cities_redirect:
            cities_redirect.write(header)
            cities_redirect.writelines(redirects)


if __name__ == "__main__":
    get_cities()