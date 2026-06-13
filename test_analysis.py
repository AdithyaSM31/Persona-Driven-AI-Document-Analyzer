"""Test the full analysis pipeline with all 9 PDFs after fixes."""
import requests
import json
import os

input_dir = './input'
pdf_files = sorted([f for f in os.listdir(input_dir) if f.endswith('.pdf')])

files_data = []
file_handles = []
for pdf_file in pdf_files:
    fh = open(os.path.join(input_dir, pdf_file), 'rb')
    file_handles.append(fh)
    files_data.append(('files[]', (pdf_file, fh, 'application/pdf')))

data = {
    'persona': 'Food Contractor',
    'job_to_be_done': 'Prepare a vegetarian buffet-style dinner menu for a corporate gathering, including gluten-free items.'
}

print("Sending analysis request...")
r = requests.post('http://127.0.0.1:5000/api/analyze', files=files_data, data=data)
result = r.json()

# Close all files
for fh in file_handles:
    fh.close()

print(f"\n=== Metadata ===")
meta = result['metadata']
print(f"  Processing time: {meta['processing_time']}s")
print(f"  Total sections analyzed: {meta.get('total_sections_analyzed', 'N/A')}")
print(f"  Documents: {len(meta['input_documents'])}")

print(f"\n=== Top 5 Ranked Sections ===")
for s in result['extracted_sections']:
    print(f"  #{s['importance_rank']}: [{s['relevance_score']}%] \"{s['section_title']}\" — {s['document']} p.{s['page_number']}")

print(f"\n=== Detailed Analysis Snippets ===")
for a in result['sub_section_analysis']:
    print(f"\n  [{a['document']} p.{a['page_number']}] {a.get('section_title', '')}")
    print(f"    {a['refined_text'][:200]}...")

# Also save full output for inspection
with open('test_output.json', 'w') as f:
    json.dump(result, f, indent=2)
print(f"\nFull output saved to test_output.json")
