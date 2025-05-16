"""Count URI segments."""
import argparse
from urllib.parse import urlparse
from rdflib import URIRef




class URICounter():
    """URICounter class."""

    STOPS = [
        "https://doi.org",
        "https://isni.org/isni",
        "https://id.worldcat.org/fast",
        "https://id.nlm.nih.gov/mesh",
        "https://hdl.loc.gov/loc.afc",
        "https://hdl.loc.gov/loc.asian",
        "https://hdl.loc.gov/loc.pnp",
        "https://hdl.loc.gov/loc.law",
        "https://hdl.loc.gov/loc.gdc",
        "https://hdl.loc.gov/loc.music",
        "https://d-nb.info/gnd",
        "http://www.nber.org/papers",
        "http://id.worldcat.org/fast"
    ]

    def __init__(self, levels=3, ignore_scheme=True, stops=None):
        """Initialize URICounter object.

        Arguments:
            levels (int): Number of levels to include, starting from
                1 as the hostname. Default 3.
            ignore_scheme (bool): Set True to ignore the URI scheme,
                intended as a way to merge http and https URIs. Default
                True.
            stops (list): If not None, a set of stop URIs to replace the
                defaults that are in self.STOPS.
        """
        self.levels = levels
        self.ignore_scheme = ignore_scheme
        # Initialize stops for each level
        if stops is None:
            stops = self.STOPS
        self.stops = []
        for uri in stops:
            for root in self.split_stop_uri(uri):
                self.stops.append(root)
        # Initialize counters for each level
        self.counter = []
        for level in range(0, self.levels):
            self.counter.append({})

    def split_stop_uri(self, uri):
        """Split a URI into parts."""
        up = urlparse(uri)
        root = ""
        if not self.ignore_scheme:
            root = up.scheme + "://"
        root += up.netloc
        roots = [root]
        elements = up.path.split("/")
        try:
            elements.pop(0)
            for level in range(1, self.levels):
                root += "/" + elements.pop(0)
                roots.append(root)
        except:
            pass
        #print(f"{uri} -> {roots}")
        return roots

    def add(self, uri):
        #https://docs.python.org/3/library/urllib.parse.html
        up = urlparse(uri)
        base = ""
        if not self.ignore_scheme:
            base = up.scheme + "://"
        base += up.netloc
        if base not in self.counter[0]:
            self.counter[0][base] = 0
        self.counter[0][base] += 1
        if base in self.stops:
            return
        elements = up.path.split("/")
        try:
            elements.pop(0)  # get rid of empty before first path element
            for level in range(1, self.levels):
                base += "/" + elements.pop(0)
                if base not in self.counter[level]:
                    self.counter[level][base] = 0
                self.counter[level][base] += 1
                if base in self.stops:
                    break
        except:
            pass

    def __str__(self):
        s = ""
        for level in range(0, self.levels):
            s += "\nLevel %s:" % (level) + "\n"
            for path, count in sorted(self.counter[level].items(), key=lambda item: item[1], reverse=True):
                s += "%8d %s" % (count, path) + "\n"
        return s


class TripleURICounter():
    """Class to implement counters for all elements of triples."""

    def __init__(self, levels=3, ignore_scheme=True):
        """Initialize including setting levels and whether to ignore
        the URI scheme or not.

        Arguments:
            levels (int): number of elements within the URI to look at.
                The hostname is 1, default is 3.
            ignore_scheme (bool):
        """
        self.s_counter = URICounter(levels, ignore_scheme)
        self.p_counter = URICounter(levels, ignore_scheme)
        self.o_counter = URICounter(levels, ignore_scheme)

    def add(self, s, p, o):
        """Add all the URIs to the respective counters."""
        if isinstance(s, URIRef):
            self.s_counter.add(s)
        if isinstance(p, URIRef):
            self.p_counter.add(p)
        if isinstance(o, URIRef):
            self.o_counter.add(o)

    def __str__(self):
        s = "SUBJECTS\n\n" + str(self.s_counter)
        s += "PREDICATES\n\n" + str(self.p_counter)
        s += "OBJECTS\n\n" + str(self.o_counter)
        return s


if __name__ == "__main__":
    uc = URICounter()
    uc.add("http://id.loc.gov/vocabulary/organizations/dlc")
    uc.add("http://id.loc.gov/vocabulary/pres/ff")
    uc.add("https://id.loc.gov/vocabulary/organizations/dlf")
    uc.add("https://isni.org/isni/123")
    uc.add("https://isni.org/isni/1234")
    uc.add("https://isni.org/isni/12345")
    print(uc)
