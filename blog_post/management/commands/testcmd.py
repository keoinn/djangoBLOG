from typing import Any
from django.core.management.base import BaseCommand, CommandError, CommandParser


class Command(BaseCommand):
    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            "--gen-cert",
            action='store_true'
        )
    
    def handle(self, *args: Any, **options: Any) -> str | None:
        
        if options['gen_cert']:
            print('Delete Option Start.')
        else: 
            print("Default Action")