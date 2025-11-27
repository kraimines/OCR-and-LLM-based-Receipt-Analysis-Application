#!/usr/bin/env python
import os
import sys
import django
from django.test import Client
from django.core.files.uploadedfile import SimpleUploadedFile

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ticketocr.settings')
django.setup()

def test_web_interface():
    """Test the web interface upload functionality"""
    print("Testing web interface...")
    
    # Create a test client
    client = Client()
    
    # Test GET request to the upload page
    print("\n1. Testing GET request to upload page:")
    response = client.get('/')
    print(f"Status code: {response.status_code}")
    
    if response.status_code == 200:
        print("✅ Upload page loads successfully")
    else:
        print(f"❌ Upload page failed to load: {response.status_code}")
        return
    
    # Test POST request with image upload
    print("\n2. Testing POST request with image upload:")
    
    # Use a sample image
    image_path = "../tickets/aziza1.jpg"
    if not os.path.exists(image_path):
        print(f"❌ Sample image not found: {image_path}")
        return
    
    # Read the image file
    with open(image_path, 'rb') as f:
        image_data = f.read()
    
    # Create uploaded file
    uploaded_file = SimpleUploadedFile(
        "test_ticket.jpg",
        image_data,
        content_type="image/jpeg"
    )
    
    # Test OCR extraction only
    print("\n2a. Testing OCR extraction:")
    response = client.post('/', {
        'ocr_all': '1',
        'image': uploaded_file
    })
    
    print(f"Status code: {response.status_code}")
    if response.status_code == 200:
        print("✅ OCR extraction request successful")
        
        # Check if OCR results are in the response
        if hasattr(response, 'context') and response.context and 'ocr_results' in response.context:
            ocr_results = response.context['ocr_results']
            print(f"OCR results found: {bool(ocr_results)}")
            if ocr_results:
                print(f"  Doctr text length: {len(ocr_results.get('doctr', ''))}")
                print(f"  Tesseract text length: {len(ocr_results.get('tesseract', ''))}")
                print(f"  Docling text length: {len(ocr_results.get('docling', ''))}")
        else:
            print("❌ No OCR results in response context")
    else:
        print(f"❌ OCR extraction failed: {response.status_code}")
    
    # Test LLM analysis
    print("\n2b. Testing LLM analysis:")
    
    # First get OCR results
    with open(image_path, 'rb') as f:
        image_data = f.read()
    
    uploaded_file = SimpleUploadedFile(
        "test_ticket.jpg",
        image_data,
        content_type="image/jpeg"
    )
    
    response = client.post('/', {
        'analyze_llm': '1',
        'image': uploaded_file
    })
    
    print(f"Status code: {response.status_code}")
    if response.status_code == 200:
        print("✅ LLM analysis request successful")
        
        # Check if LLM results are in the response
        if hasattr(response, 'context') and response.context and 'llm_analysis' in response.context:
            llm_analysis = response.context['llm_analysis']
            print(f"LLM analysis found: {bool(llm_analysis)}")
            if llm_analysis and isinstance(llm_analysis, dict):
                print(f"  Magasin: {llm_analysis.get('Magasin', 'Not found')}")
                print(f"  Date: {llm_analysis.get('Date', 'Not found')}")
                print(f"  Total: {llm_analysis.get('Total', 'Not found')}")
                print(f"  Articles count: {len(llm_analysis.get('Articles', []))}")
                print(f"  Commentaire: {llm_analysis.get('Commentaire', 'No comment')}")
            else:
                print(f"❌ LLM analysis is not a dict: {type(llm_analysis)}")
        else:
            print("❌ No LLM analysis in response context")
    else:
        print(f"❌ LLM analysis failed: {response.status_code}")

if __name__ == "__main__":
    test_web_interface() 