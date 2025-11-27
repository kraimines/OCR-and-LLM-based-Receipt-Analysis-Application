#!/usr/bin/env python3
"""
Test simple pour vérifier la correction du parsing JSON
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ocrapp.views import clean_json_response

def test_problematic_response():
    """Test avec la réponse problématique"""
    
    problematic_response = """<think>
Okay, let's tackle this OCR text. First, I need to identify the store name. The first line is "dURAZIZA" which might be "DURAZIZA" but I'm not sure. Maybe it's a typo or a specific name. I'll go with "DURAZIZA" as the magasin.

Next, the ticket number. The line says "NUM VERT 80102080". "NUM VERT" could be "Numéro Vert" which is a common term for a service number in some countries. But the number here is 80102080. However, the user might consider the ticket number as the numerical part. Wait, but the example in the instructions might have a different approach. Let me check again. The line is "KORBA - NUM VERT 80102080". So "NUM VERT" is probably the service number, and the actual ticket number might be "10042" later on. Wait, there's "10042" under "Caissier". But the user's example might have "NumeroTicket" as the number after "NUM VERT" or maybe the "10042". The instruction says "Numero du ticket ou de caisse". The line "10042" is under "Caissier", so maybe that's the ticket number. But I need to be careful. Let me note both possibilities but go with "80102080" as the ticket number since it's directly mentioned with "NUM VERT".

Date and time: "18/01/2025 16:44" is clearly the date and time. So Date is "18/01/2025" and Heure is "16:44".

Articles: The lines with "a CT NOIS CACAO 1KG VA" and "b BOUTEILLE EAU POUR E" seem like article names. The prices are "13,990", "8.000", "2.010", etc. But need to check for the correct format. Also, "REMISE -28.70% a -4,010" and "REMISE -25.10% a 2.010" – the "a" and "b" might be item identifiers. So first article is "CT NOIS CACAO 1KG" with price "13,990 DT". Second is "BOUTEILLE EAU POUR E" with "8.000 DT". Then "TIMBRE LOI FIN.2022" is the tax stamp, which is separate. The "REMISE" lines are discounts, not articles. So the articles are the two items mentioned.

Total payé: "Total" is mentioned, and the line after is "16.070 =". So the total is "16.070 DT".

Timbre fiscal: The line says "+ TIMBRE LOI FIN.2022 - 0.100". So the tax stamp is "0.100 DT".

Wait, but the user's instruction says to look for amounts like 0.100 DT, 0.200 DT, etc. So "0.100" here is the timbre fiscal. So that's correct.

Now, checking the JSON structure. The store name is "DURAZIZA", number is "80102080", date is "18/01/2025", articles are the two items, total is "16.070 DT", timbre is "0.100 DT".

Wait, but the user's example might have "NumeroTicket" as "10042" if that's the ticket number. The line "10042" is under "Caissier". But the instruction says "Numero du ticket ou de caisse". So maybe "10042" is the ticket number. But the OCR text has "NUM VERT 80102080" which could be a service number. Hmm. The user might have different expectations. Since the example in the problem has "NumeroTicket" as "80102080", I'll use that. But I'm not 100% sure. Alternatively, maybe "10042" is the ticket number. Need to check if there's any other clues. The line "du 1057" at the end – maybe that's the ticket number? But "1057" is after "du". Maybe "du 1057" refers to something else. The user might have intended "NUM VERT" as the ticket number, but I'm not certain. However, the instruction says to extract "NumeroTicket" as per the OCR, so I'll go with "80102080" as the ticket number.

Articles: The first item is "CT NOIS CACAO 1KG" with price "13,990 DT". The second is "BOUTEILLE EAU POUR E" with "8.000 DT". Then there's "REMISE -28.70% a -4,010" and "REMISE -25.10% a 2.010". The "REMISE" lines are discounts, so not articles. Then "Sodexo TR" has "1.200" and "6.000" but those are probably payment methods, not articles. The "Especes" and "Rendu" are also payment details. So only the two items are articles.

Total is "16.070 DT" as per the line "Total 16.070 =".

TimbreFiscal is "0.100 DT" from "+ TIMBRE LOI FIN.2022 - 0.100".

Putting it all together in JSON format as specified.
</think>

{
  "Magasin": "DURAZIZA",
  "Date": "18/01/2025",
  "NumeroTicket": "80102080",
  "Articles": [
    { "nom": "CT NOIS CACAO 1KG", "prix": "13,990 DT" },
    { "nom": "BOUTEILLE EAU POUR E", "prix": "8.000 DT" }
  ],
  "Total": "16.070 DT",
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
    test_problematic_response() 