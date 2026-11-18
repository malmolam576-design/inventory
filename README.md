## Run

```bash
cd inventory
docker compose -f compose.yaml up --build
```

Once it's running, open http://localhost:8000/ to see the products or http://localhost:8000/admin/ to access Django admin (`admin` / `admin`).

The first run seeds the database, loads products, categories and tags, and creates the admin user.

If port 8000 is already in use, change it in `compose.yaml`.

## To stop

```bash
docker compose -f compose.yaml down -v
```

## Run tests

```bash
docker compose exec web python manage.py test catalog
```

## Features

- Product list with 5 items per page
- Search by name or description
- Filter by category and tags
- Combine search and filters
- Filters update automatically

## Notes

FE uses Django templates with some JS for search and filters for debauncing search.

`querysets.py` contains the reusable queries for search, category and tag filtering. `filters.py` handles the URL parameters. This keeps the views simple and the filtering logic easy to reuse.

Products are ordered by name, and related tags and categories are loaded together to avoid extra database queries.

`docker-entrypoint.sh` runs on every container start: it applies migrations, loads sample data, creates the dev admin user if missing, then starts the server.
