import os
from dotenv import load_dotenv
from django.core.management.base import BaseCommand


class InstallEnv(BaseCommand):

    def handle(self, *args, **options):
        dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
        if os.path.exists(dotenv_path):
            load_dotenv(dotenv_path)
