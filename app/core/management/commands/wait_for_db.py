"""
Django command to wait for database to be available
"""

import time
# Error That Postgres Throws
from psycopg2 import OperationalError as Psycopg2OpError
# Error That Django Throws when DB is not ready
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Django command to wait for database to be available"""

    def handle(self, *args, **options):
        """Entry Point for Command"""
        self.stdout.write("Waiting for Database...")
        db_up = False
        while db_up is False:
            try:
                self.check(databases=["default"])
                db_up = True
            except (Psycopg2OpError, OperationalError):
                self.stdout.write("Database Unavailable, Waiting 1 second ...")
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS("DATABASE AVAILABLE !!!"))
