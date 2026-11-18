from django.shortcuts import render
from django.core.paginator import Paginator

from catalog.filters import ProductFilter
from catalog.models import Category, Product, Tag

PAGE_SIZE = 5

def product_list(request):
  product_filter = ProductFilter(request.GET)
  products = product_filter.apply(Product.objects.all())
  product_page = Paginator(products, PAGE_SIZE).get_page(request.GET.get("page"))
  tags = Tag.objects.all()
  categories = Category.objects.all()

  return render(
    request,
    "catalog/product_list.html",
    {
      "products": product_page,
      "page_obj": product_page,
      "tags": tags,
      "categories": categories,
      "querystring": product_filter.querystring,
      "q": product_filter.q,
      "selected_category": product_filter.category,
      "selected_tags": product_filter.tags,
      "filtered": product_filter.is_active,
    }
  )
