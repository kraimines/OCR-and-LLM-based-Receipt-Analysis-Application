#!/usr/bin/env python3
"""
Script de test pour vérifier que les erreurs de formatage sont corrigées
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ocrapp.views import extraire_elements_avec_regex, valider_et_corriger_avec_regex

def test_error_fix():
    """Test de correction des erreurs de formatage"""
    
    print("=== Test 1: Texte vide ===")
    result_1 = extraire_elements_avec_regex("")
    print("Résultat:", result_1)
    print()
    
    print("=== Test 2: Texte None ===")
    result_2 = extraire_elements_avec_regex(None)
    print("Résultat:", result_2)
    print()
    
    print("=== Test 3: Texte sans total ===")
    texte_3 = """
    Boulangerie du Coin
    Date: 19/07/2024
    Pain 1.200 DT
    Lait 0.900 DT
    Timbre Fiscal 0.100 DT
    """
    result_3 = extraire_elements_avec_regex(texte_3)
    print("Résultat:", result_3)
    print()
    
    print("=== Test 4: Validation avec données LLM ===")
    result_data_llm = {
        "Date": "",
        "Magasin": "Boulangerie du Coin",
        "NumeroTicket": "12345",
        "Total": "",
        "TimbreFiscal": "",
        "Articles": [
            {"nom": "Pain", "prix": "1.200 DT"},
            {"nom": "Lait", "prix": "0.900 DT"},
        ]
    }
    
    result_4 = valider_et_corriger_avec_regex(result_data_llm, texte_3)
    print("Résultat validation:", result_4)
    print()
    
    print("=== Test 5: Texte avec caractères spéciaux ===")
    texte_5 = """
    Restaurant XYZ
    Date: 25-01-2025
    Pizza 8.500 DT
    Boisson 2.000 DT
    Timbre Fiscal 0.200 DT
    Total : 10.700 DT
    """
    result_5 = extraire_elements_avec_regex(texte_5)
    print("Résultat:", result_5)
    print()

if __name__ == "__main__":
    test_error_fix() 