import requests
import csv


def get_cities():
    with open("cities.csv") as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        rows = [row for row in reader if len(row) == 2]
        cities = []
        [cities.append(city) for city in rows if city not in cities]
        ok = []
        redirects = []
        error = []
        total = len(cities)
        for (idx, row) in enumerate(cities):
            state, city = row
            print(f"({idx+1} of {total})\tChecking {city}/{state.upper()}...")
            url = (
                f"https://doem.org.br/{state}/{city}/pesquisar?data_inicial=2000-01-01"
            )
            line = f"{state},{city},{url}\n"

            r = requests.get(url)
            has_redirect = len(r.history) > 0

            if r.status_code == 200:
                if has_redirect:
                    redirects.append(line)
                else:
                    ok.append(line)
            else:
                error.append(f"{state},{city}")

        with open(f"cities_ok.csv", "w") as cities_ok:
            cities_ok.writelines(ok)
        with open(f"cities_redirect.csv", "w") as cities_redirect:
            cities_redirect.writelines(redirects)
        if len(error) > 0:
            with open(f"cities_error.csv", "w") as cities_redirect:
                cities_redirect.writelines(error)


if __name__ == "__main__":
    get_cities()
