import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'analisistweets.settings')

import django
django.setup()

from analisis.domain import update_problematics


if __name__ == '__main__':
    update_problematics(debug=True)
