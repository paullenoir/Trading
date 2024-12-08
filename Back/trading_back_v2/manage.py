#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

# python manage.py run_back "1d"
# python manage.py run_back "1h"
# python manage.py run_back "30min"
# python manage.py run_back "15min"
#la commande run_back se trouve dans Trading\Back\trading_back_v2\trading_back_app_v2\management\commands\run_back.py

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'trading_back_v2.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
