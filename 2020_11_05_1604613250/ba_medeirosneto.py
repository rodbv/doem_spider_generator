from gazette.spiders.base import DoemGazetteSpider


class BaMedeirosNetoSpider(DoemGazetteSpider):
    TERRITORY_ID = "2921104"
    name = "ba_medeirosneto"
    state_city_url_part = "ba/medeirosneto"
