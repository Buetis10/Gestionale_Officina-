#!/usr/bin/env python
"""Utility da riga di comando per amministrare il progetto Django.

Questo script è il punto di ingresso per comandi come `migrate`, `runserver` e `createsuperuser`.
Viene normalmente eseguito con il virtual environment attivato.
"""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
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
