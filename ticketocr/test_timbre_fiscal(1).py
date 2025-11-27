#!/usr/bin/env python3
"""
Script de test pour vérifier la détection du timbre fiscal
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ocrapp.views import post_process_timbre_fiscal

def test_timbre_fiscal_detection():
    """Test de la détection du timbre fiscal"""
    
    # Test 1: Timbre fiscal dans les articles
    test_data_1 = {
        "Date": "25/01/2025 14:30",
        "Magasin": "Carrefour",
        "NumeroTicket": "12345",
        "Total": "15.100 DT",
        "TimbreFiscal": "",
        "Articles": [
            {"nom": "Pain", "prix": "1.200 DT"},
            {"nom": "Lait", "prix": "0.900 DT"},
            {"nom": "Timbre fiscal", "prix": "0.100 DT"},  # Doit être détecté
            {"nom": "Yaourt", "prix": "2.500 DT"}
        ]
    }
    
    print("=== Test 1: Timbre fiscal dans les articles ===")
    print("Avant:", test_data_1)
    result_1 = post_process_timbre_fiscal(test_data_1)
    print("Après:", result_1)
    print(f"Timbre fiscal détecté: {result_1['TimbreFiscal']}")
    print(f"Nombre d'articles après filtrage: {len(result_1['Articles'])}")
    print()
    
    # Test 2: Timbre fiscal déjà détecté
    test_data_2 = {
        "Date": "25/01/2025 14:30",
        "Magasin": "Carrefour",
        "NumeroTicket": "12345",
        "Total": "15.100 DT",
        "TimbreFiscal": "0.100 DT",  # Déjà détecté
        "Articles": [
            {"nom": "Pain", "prix": "1.200 DT"},
            {"nom": "Lait", "prix": "0.900 DT"},
            {"nom": "Timbre fiscal", "prix": "0.100 DT"},  # Ne doit pas être dupliqué
            {"nom": "Yaourt", "prix": "2.500 DT"}
        ]
    }
    
    print("=== Test 2: Timbre fiscal déjà détecté ===")
    print("Avant:", test_data_2)
    result_2 = post_process_timbre_fiscal(test_data_2)
    print("Après:", result_2)
    print(f"Timbre fiscal détecté: {result_2['TimbreFiscal']}")
    print(f"Nombre d'articles après filtrage: {len(result_2['Articles'])}")
    print()
    
    # Test 3: Pas de timbre fiscal
    test_data_3 = {
        "Date": "25/01/2025 14:30",
        "Magasin": "Carrefour",
        "NumeroTicket": "12345",
        "Total": "15.000 DT",
        "TimbreFiscal": "",
        "Articles": [
            {"nom": "Pain", "prix": "1.200 DT"},
            {"nom": "Lait", "prix": "0.900 DT"},
            {"nom": "Yaourt", "prix": "2.500 DT"}
        ]
    }
    
    print("=== Test 3: Pas de timbre fiscal ===")
    print("Avant:", test_data_3)
    result_3 = post_process_timbre_fiscal(test_data_3)
    print("Après:", result_3)
    print(f"Timbre fiscal détecté: {result_3['TimbreFiscal']}")
    print(f"Nombre d'articles après filtrage: {len(result_3['Articles'])}")
    print()
    
    # Test 4: Différents montants de timbre fiscal
    test_data_4 = {
        "Date": "25/01/2025 14:30",
        "Magasin": "Carrefour",
        "NumeroTicket": "12345",
        "Total": "25.200 DT",
        "TimbreFiscal": "",
        "Articles": [
            {"nom": "Pain", "prix": "1.200 DT"},
            {"nom": "Lait", "prix": "0.900 DT"},
            {"nom": "Timbre fiscal", "prix": "0.200 DT"},  # Timbre 0.200 DT
            {"nom": "Yaourt", "prix": "2.500 DT"}
        ]
    }
    
    print("=== Test 4: Timbre fiscal 0.200 DT ===")
    print("Avant:", test_data_4)
    result_4 = post_process_timbre_fiscal(test_data_4)
    print("Après:", result_4)
    print(f"Timbre fiscal détecté: {result_4['TimbreFiscal']}")
    print(f"Nombre d'articles après filtrage: {len(result_4['Articles'])}")
    print()

if __name__ == "__main__":
    test_timbre_fiscal_detection() 