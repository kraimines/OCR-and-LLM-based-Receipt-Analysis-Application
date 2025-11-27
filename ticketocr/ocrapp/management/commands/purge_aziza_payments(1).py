from django.core.management.base import BaseCommand
from ocrapp.models import AccountingEntry
from datetime import date

TARGET_COMPTE = '531200'
TARGET_DESCRIPTION = 'Paiement ticket de caisse'
TARGET_LIBELLE = 'Paiement ticket - AZIZA - 80102080 - 4.090 DT'
TARGET_DATES = [date(2025, 2, 1), date(2025, 8, 8)]

class Command(BaseCommand):
    help = "Supprime définitivement les écritures de paiement AZIZA (4.090 DT) aux dates ciblées"

    def handle(self, *args, **options):
        qs = AccountingEntry.objects.filter(
            compte=TARGET_COMPTE,
            description=TARGET_DESCRIPTION,
            libelle_ecriture=TARGET_LIBELLE,
            date_ecriture__in=TARGET_DATES
        )
        count = qs.count()
        if count == 0:
            self.stdout.write(self.style.WARNING('Aucune écriture à supprimer.'))
            return
        qs.delete()
        self.stdout.write(self.style.SUCCESS(f'{count} écriture(s) supprimée(s).'))
