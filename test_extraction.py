"""Test improved section extraction with font-based title detection."""
from analyzer import extract_structure_from_pdf
import os

input_dir = './input'
total_sections = 0
for pdf_file in sorted(os.listdir(input_dir)):
    if not pdf_file.endswith('.pdf'):
        continue
    path = os.path.join(input_dir, pdf_file)
    structure, content = extract_structure_from_pdf(path)
    sections = len(structure['outline'])
    total_sections += sections
    print(f'\n=== {pdf_file}: {sections} sections ===')
    for item in structure['outline']:
        text_len = len(content.get(item['text'], ''))
        print(f'  p.{item["page"]:2d}: "{item["text"]}" ({text_len} chars)')

print(f'\n{"="*60}')
print(f'TOTAL: {total_sections} sections (was 9 before fix)')
