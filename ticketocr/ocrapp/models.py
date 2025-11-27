from django.db import models
from django.utils import timezone

class ExtractionHistory(models.Model):
    image = models.ImageField(upload_to='tickets/')
    extracted_text = models.TextField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Ticket du {self.uploaded_at.strftime('%Y-%m-%d %H:%M:%S')}"

class TicketHistory(models.Model):
    """Historique des tickets analysés"""
    date_ticket = models.DateField()
    magasin = models.CharField(max_length=200)
    total = models.DecimalField(max_digits=10, decimal_places=3)
    numero_ticket = models.CharField(max_length=100, blank=True, null=True)
    articles_data = models.JSONField(default=list)  # Stocke les articles en JSON
    llm_analysis = models.JSONField(default=dict)  # Stocke l'analyse LLM complète
    tva_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)  # Taux de TVA en %
    tva_amount = models.DecimalField(max_digits=10, decimal_places=3, default=0)  # Montant TVA
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.magasin} - {self.date_ticket} - {self.total} DT"

class AccountingEntry(models.Model):
    """Entrées comptables générées"""
    ticket = models.ForeignKey(TicketHistory, on_delete=models.CASCADE, related_name='accounting_entries')
    date_ecriture = models.DateField()
    compte = models.CharField(max_length=20, default='606100')
    description = models.CharField(max_length=200, default='Achat divers')
    libelle_ecriture = models.CharField(max_length=200)
    debit = models.DecimalField(max_digits=10, decimal_places=3)
    credit = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.libelle_ecriture} - {self.debit} DT"

class Budget(models.Model):
    """Modèle pour gérer les budgets mensuels et annuels"""
    BUDGET_TYPES = [
        ('monthly', 'Mensuel'),
        ('yearly', 'Annuel'),
    ]
    
    type_budget = models.CharField(max_length=10, choices=BUDGET_TYPES, default='monthly')
    montant = models.DecimalField(max_digits=12, decimal_places=3)
    annee = models.IntegerField()
    mois = models.IntegerField(null=True, blank=True)  # Null pour budget annuel
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['type_budget', 'annee', 'mois']
        ordering = ['-created_at']
    
    def __str__(self):
        if self.type_budget == 'monthly':
            return f"Budget {self.get_type_budget_display()} {self.mois:02d}/{self.annee} - {self.montant} DT"
        else:
            return f"Budget {self.get_type_budget_display()} {self.annee} - {self.montant} DT"
    
    @classmethod
    def get_current_budget(cls, budget_type='monthly'):
        """Récupère le budget actuel selon le type"""
        from datetime import datetime
        now = datetime.now()
        
        if budget_type == 'monthly':
            try:
                return cls.objects.get(
                    type_budget='monthly',
                    annee=now.year,
                    mois=now.month
                )
            except cls.DoesNotExist:
                return None
        else:  # yearly
            try:
                return cls.objects.get(
                    type_budget='yearly',
                    annee=now.year
                )
            except cls.DoesNotExist:
                return None
