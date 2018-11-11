from bs4 import BeautifulSoup
from re import compile
from requests import get
from .CONSTANTS import CHANGES, HEADERS, URL
from .helper import return_int_from_image_url as int_parse
from .models import Entry


class iChart:
    def __init__(self):
        self.entries = []
        self.doc = None
        self.generator = None
        self._post_init()

    def current_top_10(self):
        a = 0
        while a < 10:
            self._add_to_list()
            a += 1
        return self.entries[:10]

    def get_next_entry(self):
        a = 0
        if a < len(self.entries):
            yield self.entries[a]
        else:
            self._add_to_list()
            yield self.entries[a]
        a += 1

    def _add_to_list(self):
        self.entries.append(next(self.generator))

    def _make_request(self):
        request = get(URL, headers=HEADERS)
        self.doc = BeautifulSoup(request.text)

    def _generator_function(self):
        result_set = self.doc.find_all(
            class_=compile("spage_score_item(_1st)*")
        )
        for div in result_set:
            yield self._parse_score(div)

    def _parse_score(self, div):
        title = div.find(class_=compile("ichart_score[0-9]*_song1")).b.text
        artist = div.find(class_=compile("ichart_score[0-9]*_artist1")).b.text
        rank = int_parse(
            div.find(class_=compile("ichart_score[0-9]*_rank")).img["src"]
        )
        change = div.find(class_=compile("ichart_score[0-9]*_change"))
        change_class = CHANGES[change.span["class"][1]]
        change_rank = int(change.text) if change.text != "" else 0
        score_div = div.find(
            class_=compile("ichart_score[0-9]*_score")
        ).find_all("img")
        score = int("".join([int_parse(score["src"]) for score in score_div]))
        return Entry(title, artist, rank, change_class, change_rank, score)

    def _post_init(self):
        self._make_request()
        self.generator = self._generator_function()

