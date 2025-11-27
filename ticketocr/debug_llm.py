import os
import json
import re
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Initialiser le client OpenAI avec l'URL HuggingFace
client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=os.environ.get("HF_TOKEN", ""),
)

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

# Test avec un exemple simple
test_ocr_text = """
MAGASINS AZIZA
NUM VERT 80102080
3/01/2025 07:38 Caissier 10047 du 1069
LOT 2 SAVON MAIN 1L 3.990
TIMBRE LOI FIN.2022 0.100
Total 4.090
"""

prompt = f"""
Tu es un assistant expert en analyse de tickets de caisse à partir de plusieurs résultats OCR.

Voici un extraits OCR du ticket de caisse :

--- OCR Doctr ---
{test_ocr_text}

Ta tâche est de :
 Extraire les éléments suivants :
- Nom du magasin
- Numéro du ticket ou de caisse
- Date et heure
- Liste des articles avec prix (nom + prix)
- Total payé
- Timbre fiscal (si présent)

**IMPORTANT - RÈGLES DE CLASSIFICATION :**
1. **Timbre fiscal** : Cherche spécifiquement les montants de 0.100 DT, 0.200 DT, etc.
2. **Articles** : Tous les autres produits/services achetés
3. **INCLUSION DU TIMBRE FISCAL** : Le timbre fiscal doit être inclus dans la liste des articles

Retourne un résultat structuré sous forme JSON exactement comme ci-dessous :

{{
  "Magasin": "...",
  "Date": "...",
  "NumeroTicket": "...",
  "Articles": [
    {{ "nom": "...", "prix": "..." }},
    {{ "nom": "TIMBRE FISCAL", "prix": "..." }},
    ...
  ],
  "Total": "..."
}}

**IMPORTANT** : Le timbre fiscal doit apparaître uniquement dans la liste des Articles (avec nom "TIMBRE FISCAL").
**CONVERSION DES MONTANTS** : Si tu vois "100 DT", convertis-le en "0.100 DT" pour les timbres fiscaux.

Assure-toi que tous les montants soient des chaînes terminées par 'DT'. Ne fais aucun commentaire. Retourne uniquement le JSON.
"""

print("=== TEST DE L'API LLM ===")
print(f"HF_TOKEN présent: {bool(os.environ.get('HF_TOKEN'))}")

try:
    print("Appel à l'API HuggingFace avec Qwen...")
    
    completion = client.chat.completions.create(
        model="Qwen/Qwen3-30B-A3B:novita",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    result_text = completion.choices[0].message.content.strip()
    print(f"Réponse brute reçue: {result_text}")
    
    # Test du parsing JSON
    parsed_data = clean_json_response(result_text)
    
    if parsed_data:
        print(f"✅ SUCCÈS: JSON parsé correctement")
        print(f"Résultat: {json.dumps(parsed_data, indent=2, ensure_ascii=False)}")
    else:
        print("❌ ÉCHEC: Impossible de parser le JSON")
        
except Exception as e:
    print(f"❌ Erreur lors de l'appel API: {str(e)}") 