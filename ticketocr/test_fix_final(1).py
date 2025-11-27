import json
import re

def clean_json_response(text):
    """
    Nettoie une réponse JSON malformée de manière plus robuste
    """
    import re
    
    if not text or not isinstance(text, str):
        return None
    
    print(f"Texte original reçu: {text[:200]}...")
    
    # Supprimer les balises <think> et leur contenu
    text = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL)
    print(f"Après suppression <think>: {text[:200]}...")
    
    # Méthode simple et robuste : chercher le dernier JSON valide
    # Chercher toutes les occurrences de { et }
    start_positions = [i for i, char in enumerate(text) if char == '{']
    end_positions = [i for i, char in enumerate(text) if char == '}']
    
    if not start_positions or not end_positions:
        print("Aucun JSON trouvé")
        return None
    
    # Essayer de trouver le JSON le plus long possible
    best_json = None
    best_length = 0
    
    for start in start_positions:
        for end in end_positions:
            if end > start:
                json_candidate = text[start:end+1]
                # Vérifier si c'est un JSON valide
                try:
                    # Nettoyer le JSON candidat
                    cleaned_json = json_candidate.strip()
                    # Supprimer les virgules en trop
                    cleaned_json = re.sub(r',(\s*[}\]])', r'\1', cleaned_json)
                    # Corriger les guillemets simples
                    cleaned_json = re.sub(r"'([^']*)'", r'"\1"', cleaned_json)
                    # S'assurer que les clés ont des guillemets doubles
                    cleaned_json = re.sub(r'(\s*)(\w+)(\s*):', r'\1"\2"\3:', cleaned_json)
                    
                    # Tenter de parser
                    result = json.loads(cleaned_json)
                    if len(cleaned_json) > best_length:
                        best_json = result
                        best_length = len(cleaned_json)
                        print(f"✅ JSON valide trouvé (longueur {best_length}): {cleaned_json[:200]}...")
                except:
                    continue
    
    if best_json:
        print(f"✅ JSON final sélectionné: {best_json}")
        return best_json
    
    # Fallback : essayer la méthode regex
    json_pattern = r'\{(?:[^{}]|(?:\{[^{}]*\}))*\}'
    json_matches = re.findall(json_pattern, text, re.DOTALL)
    
    if json_matches:
        json_text = max(json_matches, key=len)
        try:
            # Nettoyer le JSON
            json_text = re.sub(r',(\s*[}\]])', r'\1', json_text)
            json_text = re.sub(r"'([^']*)'", r'"\1"', json_text)
            json_text = re.sub(r'(\s*)(\w+)(\s*):', r'\1"\2"\3:', json_text)
            
            result = json.loads(json_text)
            print(f"✅ JSON parsé via regex: {result}")
            return result
        except:
            pass
    
    print("❌ Aucun JSON valide trouvé")
    return None

# Test avec la réponse LLM problématique
test_response = """<think> Okay, let's tackle this OCR text. First, I need to extract the store name. The line says "MAGASINS AZIZA" so that's the magasin. Next, the ticket number. There's "NUM VERT 80102080" which might be the number. The date and time are on the line "3/01/2025 07:38 Caissier 10047 du 1069". The date is 3/01/2025 and time is 07:38. But wait, there's another date "2025.1.23 15:56". Hmm, which one is correct? The first one is "3/01/2025" and the second is "2025.1.23". Probably the first one is the date of the transaction, and the second might be a different date, maybe the expiration or something else. But the user asked for date and time, so I'll go with the first occurrence: "3/01/2025 07:38". For the articles, there's "LOT 2 SAVON MAIN 1L" with the price "3.990". So that's one article. Then "TIMBRE LOI FIN.2022" with "0.100". But according to the rules, timbre fiscal is separate from articles. So the article is "SAVON MAIN 1L" and the price is "3.990 DT". The timbre fiscal is "0.100 DT". Total is "Total 4.090" so that's "4.090 DT". The "speces : 6.000" and "endu : 1.910" might be the amount paid and change, but the user didn't ask for that. Just the total payé is 4.090 DT. So putting it all together, the JSON should have Magasin as "AZIZA", NumeroTicket as "80102080", Date as "3/01/2025 07:38", Articles with the soap, Total as "4.090 DT", and TimbreFiscal as "0.100 DT". </think> { "Magasin": "AZIZA", "Date": "3/01/2025 07:38", "NumeroTicket": "80102080", "Articles": [ { "nom": "LOT 2 SAVON MAIN 1L", "prix": "3.990 DT" } ], "Total": "4.090 DT", "TimbreFiscal": "0.100 DT" }"""

print("=== TEST DE LA FONCTION AMÉLIORÉE ===")
result = clean_json_response(test_response)

if result:
    print("\n✅ SUCCÈS: JSON parsé correctement")
    print(f"Résultat: {json.dumps(result, indent=2, ensure_ascii=False)}")
else:
    print("\n❌ ÉCHEC: Impossible de parser le JSON") 