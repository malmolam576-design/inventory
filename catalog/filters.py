
# Read search/category/tag filters from request query params.
# Current params minus page for building pagination.

class ProductFilter:
    def __init__(self, data):
        self.data = data
        self.q = data.get("q", "").strip()
        self.category = data.get("category", "").strip()
        self.tags = list(filter(None, data.getlist("tag")))

    @property
    def is_active(self):
        return any((self.q, self.category, self.tags))

    @property
    def querystring(self):
        params = self.data.copy()
        params.pop("page", None)
        return params.urlencode()

    def apply(self, queryset):
        return queryset.with_related().filter_by(self.q, self.category, self.tags)
