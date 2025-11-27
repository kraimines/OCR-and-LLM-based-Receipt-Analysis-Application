#!/usr/bin/env python3
"""
Script de test pour vérifier le nettoyage des réponses JSON du LLM
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ocrapp.views import clean_json_response
import json

def test_json_cleaning():
    """Test du nettoyage des réponses JSON"""
    
    # Test 1: Réponse avec balises <think>
    test_response_1 = """<think>
Okay, let me try to figure this out. The user provided an OCR text from a receipt and wants me to extract specific elements into a JSON format. First, I need to parse the OCR text carefully.

Starting with the "Magasin" (Store name). The first line after "OCR Doctr" is "aHirAZIZA" which might be "AZIZA" since "aHir" could be a typo or misread. Then there's "MONASTIR2 - NUM VERT 80102080". The store name is probably "AZIZA" as mentioned in the code and the site URL later. So Magasin would be "AZIZA".

Next, the "NumeroTicket" (Receipt Number). The line "NUM VERT 80102080" suggests that the number is 80102080. But sometimes "NUM VERT" might be "Numéro de ticket" or something similar. So I'll take 80102080 as the ticket number.

For the "Date" and "Heure" (Date and Time). There's "3/01/2025 07:38" and another date "2025.1.23 15:56". Wait, the first date is 3/01/2025, which is day/month/year, so March 1, 2025, and the time is 07:38. The second date is 2025.1.23, which is January 23, 2025, at 15:56. But which one is the actual date of the receipt? The first one might be the date when the receipt was printed, and the second could be a different date. However, since the user wants the date and time, maybe the first one is the correct one. But I need to check. The line "3/01/2025 07:38 Caissier 10047 du 1069" seems like the date and time of the transaction. The second date "2025.1.23 15:56" might be a different date, maybe a later date or a mistake. I'll go with "3/01/2025 07:38" as the date and time.

Articles: The line "LOT 2 SAVON MAIN 1L" with "3.990" next to it. So that's an article named "SAVON MAIN 1L" with a price of 3.990 DT. Then there's "TIMBRE LOI FIN.2022" with "0.100" which is the timbre fiscal. The total is 4.090 DT. The "speces" line has 6.000 and "endu" 1.910, which might be the amount paid and change, but the user didn't ask for that. So the articles list should have "SAVON MAIN 1L" at 3.990 DT.

Total payé is "Total 4.090" so that's 4.090 DT.

Timbre Fiscal is 0.100 DT as per the rule, since it's a specific amount. Even though "TIMBRE LOI FIN.2022" is mentioned, the amount is 0.100, so that's the timbre fiscal.

Wait, but the user says to look for amounts like 0.100 DT, 0.200 DT, etc. So "0.100" is the timbre fiscal. The other amounts are for the article and total. So the timbre fiscal is 0.100 DT.

Putting it all together:

Magasin: AZIZA
NumeroTicket: 80102080
Date: "3/01/2025 07:38"
Articles: [{"nom": "SAVON MAIN 1L", "prix": "3.990 DT"}]
Total: "4.090 DT"
TimbreFiscal: "0.100 DT"

I need to make sure that the JSON structure matches exactly. Also, check that all amounts are strings ending with DT. The dates should be in the format as they appear, but maybe the user expects a specific format. The first date is "3/01/2025 07:38" and the second is "2025.1.23 15:56". But the first one is probably the correct transaction date. The second might be a different date, like a later date or a mistake. Since the user didn't specify which one, I'll use the first date mentioned.

Also, check if "speces" and "endu" are part of the payment details, but the user didn't ask for those. So ignore them.

So the final JSON should have all these elements.
</think>

{
  "Magasin": "AZIZA",
  "Date": "3/01/2025 07:38",
  "NumeroTicket": "80102080",
  "Articles": [
    { "nom": "LOT 2 SAVON MAIN 1L", "prix": "3.990 DT" }
  ],
  "Total": "4.090 DT",
  "TimbreFiscal": "0.100 DT"
}"""
    
    print("=== Test 1: Réponse avec balises <think> ===")
    result_1 = clean_json_response(test_response_1)
    print("Résultat:", result_1)
    print("Succès:", result_1 is not None)
    print()
    
    # Test 2: Réponse JSON simple
    test_response_2 = """{
  "Magasin": "Carrefour",
  "Date": "25/01/2025 14:30",
  "NumeroTicket": "12345",
  "Articles": [
    {"nom": "Pain", "prix": "1.200 DT"},
    {"nom": "Lait", "prix": "0.900 DT"}
  ],
  "Total": "2.100 DT",
  "TimbreFiscal": "0.100 DT"
}"""
    
    print("=== Test 2: Réponse JSON simple ===")
    result_2 = clean_json_response(test_response_2)
    print("Résultat:", result_2)
    print("Succès:", result_2 is not None)
    print()
    
    # Test 3: Réponse avec texte avant et après JSON
    test_response_3 = """Voici l'analyse du ticket :

{
  "Magasin": "Monoprix",
  "Date": "20/01/2025 10:15",
  "NumeroTicket": "67890",
  "Articles": [
    {"nom": "Yaourt", "prix": "2.500 DT"}
  ],
  "Total": "2.500 DT",
  "TimbreFiscal": ""
}

J'espère que cette analyse vous convient."""
    
    print("=== Test 3: Réponse avec texte avant et après ===")
    result_3 = clean_json_response(test_response_3)
    print("Résultat:", result_3)
    print("Succès:", result_3 is not None)
    print()
    
    # Test 4: Réponse invalide (pas de JSON)
    test_response_4 = """Je ne peux pas analyser ce ticket car l'image est trop floue."""
    
    print("=== Test 4: Réponse sans JSON ===")
    result_4 = clean_json_response(test_response_4)
    print("Résultat:", result_4)
    print("Succès:", result_4 is None)
    print()

    # Test 4: Réponse problématique qui causait l'erreur "No valid JSON found"
    test_response_4 = """<think>
Okay, let's tackle this OCR text. First, I need to extract the store name. The first line says "MONOPRIX", so that's straightforward.

Next, the ticket number. Looking through the text, there's "C36224 X" which might be the ticket number. The "C" could stand for "caisse" or "ticket", so I'll take "C36224" as the NumeroTicket.

Date and time are given as "21/05/2025 13:02:42". I'll format that as "Date": "21/05/2025 13:02:42".

For the articles, the first line after the store name is "PROTEGES SLIP NANA" with "1 X 3690". So that's an article named "PROTEGES SLIP NANA" priced at 3690 DT. Then there's "D.Timbre LF 2022" with "1 X 100". According to the rules, the timbre fiscal should be included in the Articles list. The note says if there's "100 DT", convert to "0.100 DT". So the second article is "TIMBRE FISCAL" with price "0.100 DT".

Total payé is "ESPECES : 5000" which is 5000 DT. The "TOTAL ACHAT" is 3790, but the total paid is 5000. The "RENDU" is 1210, but there's also "TOTAL RENDU 1250". However, the user asked for "Total payé" which is the amount paid, so that's 5000 DT.

Wait, but the "RENDU EN VOTRE FAVEUR - 40" and "TOTAL RENDU 1250". Maybe the total paid is 5000, and the total refund is 1250? But the instruction says to extract "Total payé" which is "ESPECES : 5000", so that's correct.

I need to make sure the timbre fiscal is included as an article. The original text has "D.Timbre LF 2022" with 1 X 100. So converting 100 to 0.100 DT and naming it "TIMBRE FISCAL".

Check if all prices end with 'DT'. The first article is 3690 DT, the second is 0.100 DT. The total payé is 5000 DT. The other totals like 3790 and 1210 are mentioned, but the user specified "Total payé" which is 5000.

So the JSON should have Magasin as "MONOPRIX", NumeroTicket as "C36224", Date as "21/05/2025 13:02:42", Articles with the two items, and Total as "5000 DT".
</think>

{
  "Magasin": "MONOPRIX",
  "Date": "21/05/2025 13:02:42",
  "NumeroTicket": "C36224",
  "Articles": [
    { "nom": "PROTEGES SLIP NANA", "prix": "3690 DT" },
    { "nom": "TIMBRE FISCAL", "prix": "0.100 DT" }
  ],
  "Total": "5000 DT"
}"""

    print("\n=== TEST 4: Réponse problématique ===")
    result_4 = clean_json_response(test_response_4)
    print(f"Résultat: {json.dumps(result_4, indent=2, ensure_ascii=False) if result_4 else 'None'}")

if __name__ == "__main__":
    test_json_cleaning() 