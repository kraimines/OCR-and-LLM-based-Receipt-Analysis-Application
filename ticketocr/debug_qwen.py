#!/usr/bin/env python3
"""
Script de diagnostic pour tester les APIs Qwen (HuggingFace) et Google Gemini
"""

import os
import json
from openai import OpenAI
from dotenv import load_dotenv
import google.generativeai as genai

# Charger les variables d'environnement
load_dotenv()

def test_huggingface_connection():
    """Test de connexion à l'API HuggingFace"""
    print("🔍 Test de connexion HuggingFace...")
    
    hf_token = os.environ.get("HF_TOKEN", "")
    if not hf_token:
        print("❌ Token HuggingFace manquant dans .env")
        return False
    
    print(f"✅ Token HuggingFace trouvé: {hf_token[:10]}...")
    
    try:
        client = OpenAI(
            base_url="https://router.huggingface.co/v1",
            api_key=hf_token,
        )
        print("✅ Client OpenAI initialisé avec succès")
        return client
    except Exception as e:
        print(f"❌ Erreur initialisation client: {e}")
        return None

def test_qwen_model(client):
    """Test du modèle Qwen"""
    print("\n🤖 Test du modèle Qwen...")
    
    if not client:
        print("❌ Client non disponible")
        return None
    
    # Prompt de test simple
    test_prompt = """Tu es un assistant expert. Réponds UNIQUEMENT avec un objet JSON valide :

{
  "test": "success",
  "message": "Le modèle fonctionne correctement"
}

NE RENVOIE QUE LE JSON, sans commentaires."""
    
    try:
        print("📤 Envoi de la requête de test...")
        completion = client.chat.completions.create(
            model="Qwen/Qwen3-30B-A3B:novita",
            messages=[
                {"role": "user", "content": test_prompt}
            ],
            temperature=0,
            timeout=30
        )
        
        response_text = completion.choices[0].message.content.strip()
        print(f"📥 Réponse reçue: {response_text}")
        
        # Tenter de parser le JSON
        try:
            json_response = json.loads(response_text)
            print("✅ JSON valide reçu")
            print(f"📊 Contenu: {json_response}")
            return True
        except json.JSONDecodeError as e:
            print(f"❌ Erreur parsing JSON: {e}")
            print(f"📝 Réponse brute: {response_text}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur lors de l'appel API: {e}")
        return False

def test_ticket_analysis(client):
    """Test d'analyse de ticket simulé"""
    print("\n🎫 Test d'analyse de ticket...")
    
    if not client:
        print("❌ Client non disponible")
        return None
    
    # Texte OCR simulé
    ocr_text = """CARREFOUR MARKET
123 Avenue de la République
Tunis, Tunisie

Date: 15/01/2024 14:30
Ticket N°: 001234

Articles:
Pain complet      2.500 DT
Lait 1L          3.200 DT
Fromage          8.750 DT
TIMBRE FISCAL    0.100 DT

Total:          14.550 DT

Merci de votre visite"""
    
    prompt = f"""Tu es un assistant expert en analyse de tickets de caisse.

Voici un extrait OCR du ticket de caisse :

--- OCR Doctr ---
{ocr_text}

Ta tâche est d'extraire les éléments suivants et de retourner UNIQUEMENT un objet JSON valide :

{{
  "Magasin": "Nom du magasin",
  "NumeroTicket": "Numéro du ticket",
  "Date": "JJ/MM/AAAA HH:MM",
  "Articles": [
    {{ "nom": "Nom article", "prix": "Prix en DT" }},
    {{ "nom": "TIMBRE FISCAL", "prix": "0.100 DT" }}
  ],
  "Total": "Montant total en DT"
}}

RÈGLES IMPORTANTES :
1. Le timbre fiscal (0.100 DT, 0.200 DT, etc.) doit être inclus dans Articles avec nom "TIMBRE FISCAL"
2. Si tu vois "100 DT", convertis-le en "0.100 DT" pour les timbres fiscaux
3. Retourne UNIQUEMENT le JSON, sans commentaires ni texte supplémentaire
4. Commence par {{ et termine par }}
5. Assure-toi que tous les montants soient des chaînes terminées par 'DT'

NE RENVOIE QUE UN OBJET JSON. PAS DE COMMENTAIRES, PAS DE TEXTE, PAS DE PENSÉES.
Commence DIRECTEMENT par '{{' et termine par '}}'."""
    
    try:
        print("📤 Envoi de l'analyse de ticket...")
        completion = client.chat.completions.create(
            model="Qwen/Qwen3-30B-A3B:novita",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0,
            timeout=60  # Plus de temps pour l'analyse
        )
        
        response_text = completion.choices[0].message.content.strip()
        print(f"📥 Réponse d'analyse reçue ({len(response_text)} caractères)")
        print(f"📝 Réponse brute: {response_text[:500]}...")
        
        # Nettoyer et parser le JSON
        try:
            # Chercher le JSON dans la réponse
            start = response_text.find('{')
            end = response_text.rfind('}') + 1
            
            if start != -1 and end > start:
                json_text = response_text[start:end]
                json_response = json.loads(json_text)
                print("✅ Analyse de ticket réussie")
                print(f"📊 Résultat: {json.dumps(json_response, indent=2, ensure_ascii=False)}")
                return json_response
            else:
                print("❌ Aucun JSON trouvé dans la réponse")
                return None
                
        except json.JSONDecodeError as e:
            print(f"❌ Erreur parsing JSON d'analyse: {e}")
            return None
            
    except Exception as e:
        print(f"❌ Erreur lors de l'analyse de ticket: {e}")
        return None

def test_google_gemini():
    """Test de l'API Google Gemini"""
    print("\n🔍 Test de Google Gemini...")
    
    api_key = os.environ.get("GOOGLE_API_KEY", "")
    if not api_key:
        print("❌ Clé API Google Gemini manquante dans .env")
        return False
    
    print(f"✅ Clé API Google trouvée: {api_key[:10]}...")
    
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Test simple
        test_prompt = "Réponds avec un JSON: {\"test\": \"success\", \"message\": \"Gemini fonctionne\"}"
        response = model.generate_content(test_prompt)
        
        print(f"📥 Réponse Gemini: {response.text}")
        
        # Tenter de parser le JSON
        try:
            json_response = json.loads(response.text)
            print("✅ Gemini fonctionne correctement")
            return True
        except json.JSONDecodeError:
            print("⚠️ Gemini répond mais pas en JSON valide")
            return True
            
    except Exception as e:
        print(f"❌ Erreur Gemini: {e}")
        return False

def main():
    """Fonction principale de diagnostic"""
    print("🚀 Diagnostic des APIs - HuggingFace & Google Gemini")
    print("=" * 60)
    
    # Test 1: Connexion HuggingFace
    print("\n📡 TEST HUGGINGFACE")
    client = test_huggingface_connection()
    
    # Test 2: Modèle Qwen
    if client:
        model_ok = test_qwen_model(client)
        
        # Test 3: Analyse de ticket avec Qwen
        if model_ok:
            test_ticket_analysis(client)
        else:
            print("\n❌ Le modèle Qwen ne fonctionne pas correctement")
    else:
        print("\n❌ Impossible de se connecter à HuggingFace")
    
    # Test 4: Google Gemini
    print("\n📡 TEST GOOGLE GEMINI")
    test_google_gemini()
    
    print("\n" + "=" * 60)
    print("🏁 Diagnostic terminé")

if __name__ == "__main__":
    main()
