from django.db.models import Q, QuerySet

# Custom queryset for Product

class ProductQuerySet(QuerySet):
    def with_related(self):
        return self.select_related("category").prefetch_related("tags")

    def search(self, text):
        return self.filter(Q(name__icontains=text) | Q(description__icontains=text)) if text else self

    def in_category(self, slug):
        return self.filter(category__slug=slug) if slug else self

    def with_any_tag(self, slugs):
        return self.filter(tags__slug__in=slugs).distinct() if slugs else self

    def filter_by(self, q="", category="", tags=()):
        return self.search(q).in_category(category).with_any_tag(tags)
