
#!/bin/sh
set -e

# Update database
python manage.py migrate --noinput

# Load initial data
python manage.py seed

# Create admin user if credentials are provided
if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ]; then
    python manage.py shell -c "
import os
from django.contrib.auth import get_user_model

User = get_user_model()
username = os.environ['DJANGO_SUPERUSER_USERNAME']

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(
        username,
        os.environ.get('DJANGO_SUPERUSER_EMAIL', ''),
        os.environ['DJANGO_SUPERUSER_PASSWORD']
    )
    print('Admin user created.')
"
fi

# Start Django
exec python manage.py runserver 0.0.0.0:8000
