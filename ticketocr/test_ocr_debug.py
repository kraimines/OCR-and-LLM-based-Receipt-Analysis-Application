#!/usr/bin/env python
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ticketocr.settings')
django.setup()

from ocrapp.views import extract_text_doctr, extract_text_docling, extract_text_tesseract, analyze_three_texts_with_llm

def test_ocr_extraction(image_path):
    """Test OCR extraction on a sample image"""
    print(f"Testing OCR extraction on: {image_path}")
    print("=" * 60)
    
    if not os.path.exists(image_path):
        print(f"❌ Image not found: {image_path}")
        return
    
    # Test each OCR engine
    print("\n1. Testing Doctr OCR:")
    try:
        doctr_text = extract_text_doctr(image_path)
        print(f"✅ Doctr extracted {len(doctr_text)} characters")
        print(f"First 200 chars: {doctr_text[:200]}...")
        if len(doctr_text.strip()) == 0:
            print("⚠️  WARNING: Doctr returned empty text!")
    except Exception as e:
        print(f"❌ Doctr error: {e}")
        doctr_text = ""
    
    print("\n2. Testing Tesseract OCR:")
    try:
        tesseract_text = extract_text_tesseract(image_path)
        print(f"✅ Tesseract extracted {len(tesseract_text)} characters")
        print(f"First 200 chars: {tesseract_text[:200]}...")
        if len(tesseract_text.strip()) == 0:
            print("⚠️  WARNING: Tesseract returned empty text!")
    except Exception as e:
        print(f"❌ Tesseract error: {e}")
        tesseract_text = ""
    
    print("\n3. Testing Docling OCR:")
    try:
        docling_text = extract_text_docling(image_path)
        print(f"✅ Docling extracted {len(docling_text)} characters")
        print(f"First 200 chars: {docling_text[:200]}...")
        if len(docling_text.strip()) == 0:
            print("⚠️  WARNING: Docling returned empty text!")
    except Exception as e:
        print(f"❌ Docling error: {e}")
        docling_text = ""
    
    # Test LLM analysis
    print("\n4. Testing LLM Analysis:")
    ocr_results = {
        'doctr': doctr_text,
        'tesseract': tesseract_text,
        'docling': docling_text
    }
    
    # Check if any OCR returned text
    total_chars = len(doctr_text) + len(tesseract_text) + len(docling_text)
    print(f"Total characters extracted: {total_chars}")
    
    if total_chars == 0:
        print("❌ No text extracted by any OCR engine!")
        return
    
    try:
        llm_result = analyze_three_texts_with_llm(ocr_results)
        print(f"✅ LLM analysis completed")
        print(f"Result type: {type(llm_result)}")
        
        if isinstance(llm_result, dict):
            print("\nExtracted Information:")
            print(f"  Magasin: {llm_result.get('Magasin', 'Not found')}")
            print(f"  Date: {llm_result.get('Date', 'Not found')}")
            print(f"  NumeroTicket: {llm_result.get('NumeroTicket', 'Not found')}")
            print(f"  Total: {llm_result.get('Total', 'Not found')}")
            print(f"  Articles count: {len(llm_result.get('Articles', []))}")
            print(f"  Commentaire: {llm_result.get('Commentaire', 'No comment')}")
            
            if llm_result.get('Articles'):
                print("\nArticles found:")
                for i, article in enumerate(llm_result['Articles'], 1):
                    print(f"  {i}. {article.get('nom', 'Unknown')} - {article.get('prix', 'Unknown')}")
        else:
            print(f"❌ LLM returned unexpected type: {llm_result}")
            
    except Exception as e:
        print(f"❌ LLM analysis error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # Test with a sample image
    sample_image = "../tickets/aziza1.jpg"  # Adjust path as needed
    
    if len(sys.argv) > 1:
        sample_image = sys.argv[1]
    
    test_ocr_extraction(sample_image) 