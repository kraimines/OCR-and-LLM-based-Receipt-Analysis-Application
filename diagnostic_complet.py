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

from ocrapp.views import (
    analyze_three_texts_with_llm, 
    gemini_model, 
    extract_text_doctr, 
    extract_text_docling, 
    extract_text_tesseract,
    diagnose_system
)

def test_ocr_engines():
    """Test des moteurs OCR"""
    print("=== Test des moteurs OCR ===")
    
    # Créer une image de test simple
    try:
        from PIL import Image, ImageDraw, ImageFont
        import tempfile
        
        # Créer une image de test
        img = Image.new('RGB', (400, 200), color='white')
        draw = ImageDraw.Draw(img)
        
        # Ajouter du texte
        try:
            font = ImageFont.truetype("arial.ttf", 16)
        except:
            font = ImageFont.load_default()
        
        text = """MONOPRIX
Ticket N°: 12345
Date: 15/12/2024 14:30
PAIN BAGUETTE    0.800 DT
LAIT 1L          1.200 DT
TIMBRE FISCAL    0.100 DT
TOTAL: 2.100 DT"""
        
        draw.text((10, 10), text, fill='black', font=font)
        
        # Sauvegarder temporairement
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
            img.save(tmp.name)
            test_image_path = tmp.name
        
        print(f"✅ Image de test créée: {test_image_path}")
        
        # Test DocLing
        try:
            docling_text = extract_text_docling(test_image_path)
            print(f"✅ DocLing: {len(docling_text)} caractères extraits")
            print(f"   Texte: {docling_text[:100]}...")
        except Exception as e:
            print(f"❌ DocLing échoué: {e}")
            docling_text = ""
        
        # Test Tesseract
        try:
            tesseract_text = extract_text_tesseract(test_image_path)
            print(f"✅ Tesseract: {len(tesseract_text)} caractères extraits")
            print(f"   Texte: {tesseract_text[:100]}...")
        except Exception as e:
            print(f"❌ Tesseract échoué: {e}")
            tesseract_text = ""
        
        # Test Doctr
        try:
            doctr_text = extract_text_doctr(test_image_path)
            print(f"✅ Doctr: {len(doctr_text)} caractères extraits")
            print(f"   Texte: {doctr_text[:100]}...")
        except Exception as e:
            print(f"❌ Doctr échoué: {e}")
            doctr_text = ""
        
        # Nettoyer
        os.unlink(test_image_path)
        
        return {
            "docling": docling_text,
            "tesseract": tesseract_text,
            "doctr": doctr_text
        }
        
    except Exception as e:
        print(f"❌ Erreur lors de la création de l'image de test: {e}")
        return {"docling": "", "tesseract": "", "doctr": ""}

def test_gemini_detailed():
    """Test détaillé de Gemini"""
    print("\n=== Test détaillé de Gemini ===")
    
    if gemini_model is None:
        print("❌ Gemini n'est pas configuré")
        return False
    
    print("✅ Gemini est configuré")
    
    # Test avec texte simple
    try:
        import google.generativeai as genai
        
        prompt = """Analyse ce ticket et extrait les informations :

MONOPRIX
Ticket N°: 12345
Date: 15/12/2024 14:30
PAIN BAGUETTE    0.800 DT
LAIT 1L          1.200 DT
TIMBRE FISCAL    0.100 DT
TOTAL: 2.100 DT

Retourne UNIQUEMENT un JSON valide avec cette structure :
{
  "Magasin": "Nom du magasin",
  "NumeroTicket": "Numero du ticket", 
  "Date": "JJ/MM/AAAA HH:MM",
  "Articles": [
    {"nom": "Nom article", "prix": "Prix en DT"}
  ],
  "Total": "Montant total en DT"
}"""

        print("📝 Test d'appel Gemini...")
        response = gemini_model.generate_content(prompt)
        result_text = response.text.strip()
        
        print(f"✅ Réponse Gemini reçue ({len(result_text)} caractères)")
        print(f"   Texte: {result_text[:200]}...")
        
        # Essayer de parser le JSON
        import json
        try:
            parsed = json.loads(result_text)
            print("✅ JSON valide parsé")
            print(f"   Magasin: {parsed.get('Magasin', 'Non trouvé')}")
            print(f"   Articles: {len(parsed.get('Articles', []))}")
            return True
        except json.JSONDecodeError as e:
            print(f"❌ JSON invalide: {e}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur Gemini: {e}")
        return False

def test_complete_workflow():
    """Test du workflow complet"""
    print("\n=== Test du workflow complet ===")
    
    # Test OCR
    ocr_results = test_ocr_engines()
    
    # Vérifier si on a du texte
    total_text = sum(len(text) for text in ocr_results.values())
    if total_text == 0:
        print("❌ Aucun texte OCR extrait - problème avec les moteurs OCR")
        return False
    
    print(f"✅ {total_text} caractères extraits au total")
    
    # Test Gemini
    if not test_gemini_detailed():
        print("❌ Problème avec Gemini")
        return False
    
    # Test workflow complet
    try:
        print("\n📝 Test du workflow complet...")
        result = analyze_three_texts_with_llm(ocr_results)
        
        print("✅ Workflow complet réussi !")
        print(f"   Magasin: {result.get('Magasin', 'Non détecté')}")
        print(f"   Articles: {len(result.get('Articles', []))}")
        print(f"   Commentaire: {result.get('Commentaire', 'Aucun')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur workflow complet: {e}")
        return False

def check_database():
    """Vérifier la base de données"""
    print("\n=== Vérification de la base de données ===")
    
    try:
        from ocrapp.models import TicketHistory, AccountingEntry
        
        tickets = TicketHistory.objects.all()
        entries = AccountingEntry.objects.all()
        
        print(f"✅ Base de données accessible")
        print(f"   Tickets enregistrés: {tickets.count()}")
        print(f"   Entrées comptables: {entries.count()}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur base de données: {e}")
        return False

if __name__ == "__main__":
    print("🔧 Diagnostic complet du système")
    print("="*50)
    
    # Diagnostic système
    print("\n1. Diagnostic système:")
    issues = diagnose_system()
    if not issues:
        print("✅ Aucun problème système détecté")
    
    # Test base de données
    print("\n2. Test base de données:")
    db_ok = check_database()
    
    # Test OCR
    print("\n3. Test OCR:")
    ocr_ok = test_ocr_engines()
    
    # Test Gemini
    print("\n4. Test Gemini:")
    gemini_ok = test_gemini_detailed()
    
    # Test workflow complet
    print("\n5. Test workflow complet:")
    workflow_ok = test_complete_workflow()
    
    # Résumé
    print("\n" + "="*50)
    print("📊 RÉSUMÉ DU DIAGNOSTIC:")
    print(f"   Base de données: {'✅' if db_ok else '❌'}")
    print(f"   OCR: {'✅' if ocr_ok else '❌'}")
    print(f"   Gemini: {'✅' if gemini_ok else '❌'}")
    print(f"   Workflow complet: {'✅' if workflow_ok else '❌'}")
    
    if all([db_ok, ocr_ok, gemini_ok, workflow_ok]):
        print("\n🎉 Tous les tests sont réussis !")
        print("💡 Si rien n'est détecté, le problème vient de l'interface web ou des données uploadées")
    else:
        print("\n⚠️ Certains tests ont échoué")
        print("🔧 Vérifiez les erreurs ci-dessus")
    
    print("="*50) 