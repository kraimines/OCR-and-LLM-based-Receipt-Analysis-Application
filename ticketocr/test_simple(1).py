#!/usr/bin/env python3
"""
Test simple pour vérifier la correction du parsing JSON
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ocrapp.views import clean_json_response

def test_simple():
    """Test simple avec la réponse problématique"""
    
    problematic_response = """<think>
Okay, let's tackle this OCR text. First, I need to extract the store name. The line says "MAGASINS AZIZA" so that's the magasin.

Next, the ticket number. There's "NUM VERT 80102080" which might be the number. The date and time are on the line "3/01/2025 07:38 Caissier 10047 du 1069". The date is 3/01/2025 and time is 07:38. But wait, there's another date "2025.1.23 15:56". Hmm, which one is correct? The first one is "3/01/2025" and the second is "2025.1.23". Probably the first one is the date of the transaction, and the second might be a different date, maybe the expiration or something else. But the user asked for date and time, so I'll go with the first occurrence: "3/01/2025 07:38".

For the articles, there's "LOT 2 SAVON MAIN 1L" with the price "3.990". So that's one article. Then "TIMBRE LOI FIN.2022" with "0.100". But according to the rules, timbre fiscal is separate from articles. So the article is "SAVON MAIN 1L" and the price is "3.990 DT". The timbre fiscal is "0.100 DT".

Total is "Total 4.090" so that's "4.090 DT". 

The "speces : 6.000" and "endu : 1.910" might be the amount paid and change, but the user didn't ask for that. Just the total payé is 4.090 DT.

So putting it all together, the JSON should have Magasin as "AZIZA", NumeroTicket as "80102080", Date as "3/01/2025 07:38", Articles with the soap, Total as "4.090 DT", and TimbreFiscal as "0.100 DT".
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

    print("=== Test de la réponse problématique ===")
    result = clean_json_response(problematic_response)
    
    if result:
        print("✅ SUCCÈS: JSON parsé correctement")
        print("Résultat:", result)
        print(f"Magasin: {result.get('Magasin', 'Non trouvé')}")
        print(f"Date: {result.get('Date', 'Non trouvé')}")
        print(f"NumeroTicket: {result.get('NumeroTicket', 'Non trouvé')}")
        print(f"Total: {result.get('Total', 'Non trouvé')}")
        print(f"TimbreFiscal: {result.get('TimbreFiscal', 'Non trouvé')}")
        print(f"Articles: {len(result.get('Articles', []))} articles")
    else:
        print("❌ ÉCHEC: Impossible de parser le JSON")
    
    print()

if __name__ == "__main__":
    test_simple() 