import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'analisistweets.settings')

import django
django.setup()

from analisis.domain import update_problematics


if __name__ == '__main__':
    print("Starting udpate problematic tweetrelations script...")
    update_problematics(debug=True)
