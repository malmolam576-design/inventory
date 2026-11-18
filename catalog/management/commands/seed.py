from decimal import Decimal

from django.core.management.base import BaseCommand
from django.db import transaction

from catalog.models import Category, Tag, Product

CATEGORIES = [
    ("Audio", "audio"),
    ("Office", "office"),
    ("Kitchen", "kitchen"),
    ("Outdoors", "outdoors"),
    ("Gaming", "gaming"),
]

TAGS = [
    ("Wireless", "wireless"),
    ("Sale", "sale"),
    ("New", "new"),
    ("Eco", "eco"),
    ("Premium", "premium"),
    ("Compact", "compact"),
    ("Portable", "portable"),
    ("Bestseller", "bestseller"),
    ("Gift", "gift"),
    ("Refurbished", "refurbished"),
]

PRODUCTS = [
    ("Studio Headphones", "Over-ear wireless headphones with deep bass.", "129.99", "audio", ["wireless", "premium", "bestseller"]),
    ("Mini Speaker", "Portable wireless speaker with 12 hour battery.", "39.50", "audio", ["wireless", "portable", "sale"]),
    ("Earbuds Pro", "Noise-cancelling wireless earbuds with a charging case.", "89.00", "audio", ["wireless", "compact", "new"]),
    ("Vinyl Turntable", "Belt-drive turntable with a built-in preamp.", "199.00", "audio", ["premium", "gift"]),
    ("Standing Desk", "Adjustable height desk with a bamboo top.", "349.00", "office", ["eco", "premium"]),
    ("Ergonomic Chair", "Mesh back chair with lumbar support.", "259.00", "office", ["bestseller", "sale"]),
    ("Desk Lamp", "Warm LED lamp with a dimmer.", "24.99", "office", ["compact", "eco"]),
    ("Wireless Keyboard", "Slim wireless keyboard, quiet keys.", "49.99", "office", ["wireless", "compact"]),
    ("Notebook Set", "Three recycled paper notebooks.", "12.00", "office", ["eco", "gift"]),
    ("Espresso Machine", "15 bar espresso machine with a milk frother.", "179.00", "kitchen", ["premium", "gift"]),
    ("Chef Knife", "8 inch stainless steel chef knife.", "59.00", "kitchen", ["bestseller"]),
    ("Cast Iron Pan", "Pre-seasoned 10 inch skillet.", "34.95", "kitchen", ["sale"]),
    ("Electric Kettle", "1.7 litre kettle with auto shut-off.", "29.99", "kitchen", ["compact", "new"]),
    ("Camping Tent", "Two-person tent that packs down small.", "149.00", "outdoors", ["portable", "bestseller"]),
    ("Trail Backpack", "35 litre water-resistant backpack.", "79.00", "outdoors", ["portable", "eco", "new"]),
    ("Solar Lantern", "Rechargeable solar lantern, great for camping.", "19.99", "outdoors", ["eco", "portable", "sale"]),
    ("Gaming Mouse", "Wireless gaming mouse with 6 buttons.", "54.00", "gaming", ["wireless", "bestseller"]),
    ("Controller", "Wireless game controller with rumble.", "44.99", "gaming", ["wireless", "refurbished"]),
    ("Headset Stand", "Aluminium stand for headphones and headsets.", "17.50", None, ["compact"]),
    ("Gift Card Holder", "Simple wooden card holder.", "9.00", None, []),
]

class Command(BaseCommand):
    help = "Seed the database with sample data."

    @transaction.atomic
    def handle(self, *args, **options):

        # Create categories
        categories = {}
        for name, slug in CATEGORIES:
            categories[slug], _ = Category.objects.update_or_create(
                slug=slug,
                defaults={"name": name}
            )

        # Create tags
        tags = {}
        for name, slug in TAGS:
            tags[slug], _ = Tag.objects.update_or_create(
                slug=slug,
                defaults={"name": name}
            )

        # Create products and assign tags
        for name, description, price, category_slug, tag_slugs in PRODUCTS:
            product, _ = Product.objects.update_or_create(
                name=name,
                defaults={
                    "description": description,
                    "price": Decimal(price),
                    "category": categories.get(category_slug),
                },
            )

            product.tags.set([
                tags[slug]
                for slug in tag_slugs
            ])
