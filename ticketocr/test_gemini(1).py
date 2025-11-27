#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import django
from pathlib import Path

# Configuration Django
sys.path.append(str(Path(__file__).parent))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ticketocr.settings')
django.setup()

# Import des fonctions de test
from ocrapp.views import analyze_three_texts_with_llm, gemini_model

def test_gemini_extraction():
    """Test de l'extraction avec Gemini"""
    
    print("=== Test de Gemini pour l'extraction d'informations ===")
    
    # Vérifier si Gemini est configuré
    if gemini_model is None:
        print("❌ Gemini n'est pas configuré correctement")
        return False
    
    print("✅ Gemini est configuré")
    
    # Texte OCR de test (simulation d'un ticket)
    test_ocr_results = {
        "docling": """
        MONOPRIX
        Ticket N°: 12345
        Date: 15/12/2024 14:30
        
        PAIN BAGUETTE    0.800 DT
        LAIT 1L          1.200 DT
        TIMBRE FISCAL    0.100 DT
        
        TOTAL: 2.100 DT
        """,
        "tesseract": """
        MONOPRIX
        Ticket N°: 12345
        Date: 15/12/2024 14:30
        
        PAIN BAGUETTE    0.800 DT
        LAIT 1L          1.200 DT
        TIMBRE FISCAL    0.100 DT
        
        TOTAL: 2.100 DT
        """,
        "doctr": """
        MONOPRIX
        Ticket N°: 12345
        Date: 15/12/2024 14:30
        
        PAIN BAGUETTE    0.800 DT
        LAIT 1L          1.200 DT
        TIMBRE FISCAL    0.100 DT
        
        TOTAL: 2.100 DT
        """
    }
    
    print("\n📝 Test d'extraction avec Gemini...")
    
    try:
        # Test de l'extraction
        result = analyze_three_texts_with_llm(test_ocr_results)
        
        print("\n✅ Extraction réussie !")
        print(f"Magasin: {result.get('Magasin', 'Non détecté')}")
        print(f"Numéro Ticket: {result.get('NumeroTicket', 'Non détecté')}")
        print(f"Date: {result.get('Date', 'Non détecté')}")
        print(f"Total: {result.get('Total', 'Non détecté')}")
        print(f"Nombre d'articles: {len(result.get('Articles', []))}")
        
        if result.get('Articles'):
            print("\nArticles détectés:")
            for i, article in enumerate(result.get('Articles', []), 1):
                print(f"  {i}. {article.get('nom', 'N/A')} - {article.get('prix', 'N/A')}")
        
        print(f"\nCommentaire: {result.get('Commentaire', 'Aucun')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de l'extraction: {e}")
        return False

def test_gemini_api_direct():
    """Test direct de l'API Gemini"""
    
    print("\n=== Test direct de l'API Gemini ===")
    
    try:
        import google.generativeai as genai
        
        # Configuration
        api_key = os.environ.get('GOOGLE_API_KEY')
        if not api_key:
            print("❌ Clé API Gemini non trouvée")
            return False
        
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")
        
        # Test simple
        prompt = "Dis-moi bonjour en français"
        response = model.generate_content(prompt)
        
        print(f"✅ Réponse Gemini: {response.text}")
        return True
        
    except Exception as e:
        print(f"❌ Erreur API Gemini: {e}")
        return False

if __name__ == "__main__":
    print("🔧 Test de configuration Gemini")
    print(f"Clé API: {'✅ Configurée' if os.environ.get('GOOGLE_API_KEY') else '❌ Non configurée'}")
    
    # Test direct de l'API
    api_ok = test_gemini_api_direct()
    
    # Test d'extraction
    extraction_ok = test_gemini_extraction()
    
    print("\n" + "="*50)
    if api_ok and extraction_ok:
        print("🎉 Tous les tests Gemini sont réussis !")
    else:
        print("⚠️ Certains tests ont échoué")
    print("="*50) 