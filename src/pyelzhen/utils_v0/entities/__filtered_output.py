class FilteredOutput():
    def __init__(self, results=[], count=None, page_size=None):
        self._results = results
        self._count = count
        self._page_size = page_size

    @property
    def results(self):
        return self._results

    @results.setter
    def results(self, value):
        self._results = value

    @property
    def count(self):
        return self._count

    @count.setter
    def count(self, value):
        self._count = value

    @property
    def page_size(self):
        return self._page_size

    @page_size.setter
    def page_size(self, value):
        self._page_size = value
