from django.core.management.base import BaseCommand
from analisis.domain.populate_db import add_questions, add_tweet_and_tweet_relations
from analisistweets.settings import BASE_DIR
from pathlib import Path

class Command(BaseCommand):
    help = 'Populates the database with initial data'

    def handle(self, *args, **kwargs):
        self.stdout.write(f"Populating db items...")

        path_to_db_json = Path(BASE_DIR) / "data" / "second_run_database.json"
        add_tweet_and_tweet_relations(str(path_to_db_json))
        add_questions()
        
        self.stdout.write(self.style.SUCCESS('Database populated successfully!'))