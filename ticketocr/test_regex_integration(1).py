#!/usr/bin/env python3
"""
Script de test pour vérifier l'intégration de la fonction regex
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ocrapp.views import extraire_elements_avec_regex, valider_et_corriger_avec_regex

def test_regex_extraction():
    """Test de l'extraction avec regex"""
    
    # Test 1: Ticket avec timbre fiscal
    texte_ocr_1 = """
    Boulangerie du Coin
    Date: 19/07/2024
    Pain 1.200 DT
    Lait 0.900 DT
    Timbre Fiscal 0.100 DT
    Espece 2.200 DT
    Total : 2.200 DT
    """
    
    print("=== Test 1: Extraction regex avec timbre fiscal ===")
    result_1 = extraire_elements_avec_regex(texte_ocr_1)
    print("Résultat regex:", result_1)
    print()
    
    # Test 2: Ticket sans timbre fiscal
    texte_ocr_2 = """
    Supermarché ABC
    Date: 25/01/2025
    Pain 1.200 DT
    Lait 0.900 DT
    Yaourt 2.500 DT
    Total : 4.600 DT
    """
    
    print("=== Test 2: Extraction regex sans timbre fiscal ===")
    result_2 = extraire_elements_avec_regex(texte_ocr_2)
    print("Résultat regex:", result_2)
    print()
    
    # Test 3: Validation et correction avec regex
    result_data_llm = {
        "Date": "",
        "Magasin": "Boulangerie du Coin",
        "NumeroTicket": "12345",
        "Total": "",
        "TimbreFiscal": "",
        "Articles": [
            {"nom": "Pain", "prix": "1.200 DT"},
            {"nom": "Lait", "prix": "0.900 DT"},
            {"nom": "Timbre fiscal", "prix": "0.100 DT"},  # Doit être détecté et déplacé
        ]
    }
    
    print("=== Test 3: Validation et correction LLM avec regex ===")
    print("Avant correction:", result_data_llm)
    result_3 = valider_et_corriger_avec_regex(result_data_llm, texte_ocr_1)
    print("Après correction:", result_3)
    print()
    
    # Test 4: Différents formats de dates
    texte_ocr_3 = """
    Restaurant XYZ
    Date: 25-01-2025
    Pizza 8.500 DT
    Boisson 2.000 DT
    Timbre Fiscal 0.200 DT
    Total : 10.700 DT
    """
    
    print("=== Test 4: Format de date avec tirets ===")
    result_4 = extraire_elements_avec_regex(texte_ocr_3)
    print("Résultat regex:", result_4)
    print()

if __name__ == "__main__":
    test_regex_extraction() 