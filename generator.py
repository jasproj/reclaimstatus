"""
Treasury Package Document Generator
Generates filled documents from questionnaire data
"""

import json
import os
import re
from datetime import datetime
import zipfile

class TreasuryPackageGenerator:
    """Generates Treasury Package documents from customer data."""
    
    def __init__(self, template_dir: str):
        self.template_dir = template_dir
        self.output_dir = None
        
    def format_date_written(self, date_str: str) -> str:
        """Convert YYYY-MM-DD to 'Month DDth, YYYY' format."""
        if not date_str:
            return ""
        try:
            dt = datetime.strptime(date_str, "%Y-%m-%d")
            day = dt.day
            suffix = 'th' if 11 <= day <= 13 else {1:'st', 2:'nd', 3:'rd'}.get(day % 10, 'th')
            return dt.strftime(f"%B {day}{suffix}, %Y")
        except:
            return date_str
    
    def number_to_words(self, num: int) -> str:
        """Convert number to words (simplified for large amounts)."""
        billions = num // 1_000_000_000
        millions = (num % 1_000_000_000) // 1_000_000
        thousands = (num % 1_000_000) // 1_000
        
        words = []
        if billions:
            words.append(f"{self._digit_words(billions)} BILLION")
        if millions:
            words.append(f"{self._digit_words(millions)} MILLION")
        if thousands:
            words.append(f"{self._digit_words(thousands)} THOUSAND")
        
        return " ".join(words) if words else "ZERO"
    
    def _digit_words(self, n: int) -> str:
        """Convert small number to words."""
        ones = ["", "ONE", "TWO", "THREE", "FOUR", "FIVE", "SIX", "SEVEN", "EIGHT", "NINE",
                "TEN", "ELEVEN", "TWELVE", "THIRTEEN", "FOURTEEN", "FIFTEEN", "SIXTEEN",
                "SEVENTEEN", "EIGHTEEN", "NINETEEN"]
        tens = ["", "", "TWENTY", "THIRTY", "FORTY", "FIFTY", "SIXTY", "SEVENTY", "EIGHTY", "NINETY"]
        
        if n < 20:
            return ones[n]
        elif n < 100:
            return tens[n // 10] + ("-" + ones[n % 10] if n % 10 else "")
        else:
            return ones[n // 100] + " HUNDRED" + (" " + self._digit_words(n % 100) if n % 100 else "")
    
    def prepare_replacements(self, data: dict) -> dict:
        """Build replacement dictionary from customer data."""
        
        # Parse names
        first = data.get('firstName', '')
        middle = data.get('middleName', '')
        last = data.get('lastName', '')
        
        # Build name variants
        full_parts = [first, middle, last] if middle else [first, last]
        full_name_upper = ' '.join(full_parts).upper()
        full_name_styled = f"{first}-{middle}: {last}" if middle else f"{first}: {last}"
        
        # SSN variants
        ssn = data.get('ssn', '')
        ssn_no_dashes = ssn.replace('-', '')
        
        # Lien amount
        lien_amount = int(data.get('lienAmount', 100000000))
        lien_formatted = f"${lien_amount:,.2f}"
        lien_words = self.number_to_words(lien_amount)
        
        # Dates
        doc_date = data.get('documentDate', '')
        doc_date_written = self.format_date_written(doc_date)
        birth_date = data.get('birthDate', '')
        birth_date_written = self.format_date_written(birth_date)
        
        return {
            # Name variants - ALL CAPS version
            'THOMAS KALLEN CLAYCOMB': full_name_upper,
            'THOMAS K CLAYCOMB': full_name_upper,
            'THOMAS CLAYCOMB': f"{first} {last}".upper(),
            'T KALLEN CLAYCOMB': f"{first[0] if first else ''} {middle} {last}".upper() if middle else full_name_upper,
            'TKC': f"{first[0]}{middle[0] if middle else ''}{last[0]}".upper() if first and last else '',
            
            # Name variants - Styled version  
            'Thomas-Kallen: Claycomb': full_name_styled,
            'Thomas-Kallen: CLaycomb': full_name_styled,
            'Thomas K. Claycomb': f"{first} {middle[0] if middle else ''}. {last}".strip().replace(' .', ''),
            'Thomas Kallen Claycomb': f"{first} {middle} {last}" if middle else f"{first} {last}",
            
            # SSN variants
            '493-74-8357': ssn,
            '493748357': ssn_no_dashes,
            '**493-74-8357**': f"**{ssn}**",
            '**493748357**': f"**{ssn_no_dashes}**",
            '#493-74-8357': f"#{ssn}",
            '#493748357': f"#{ssn_no_dashes}",
            
            # Address - Mixed case
            '6316 East 113th Avenue': data.get('streetAddress', ''),
            'c/o 6316 East 113th Avenue': f"c/o {data.get('streetAddress', '')}",
            
            # Address - UPPER CASE
            '6316 EAST 113TH AVENUE': data.get('streetAddress', '').upper(),
            
            # City variants
            'Temple Terrace': data.get('city', ''),
            'TEMPLE TERRACE': data.get('city', '').upper(),
            
            # State variants  
            'Florida': data.get('state', ''),
            'FLORIDA': data.get('state', '').upper(),
            'Florida Republic': f"{data.get('state', '')} Republic",
            'Florida State': f"{data.get('state', '')} State",
            
            # ZIP Code
            '33617': data.get('zipCode', ''),
            '[33617]': f"[{data.get('zipCode', '')}]",
            'near [33617]': f"near [{data.get('zipCode', '')}]",
            
            # County variants
            'Hillsborough': data.get('county', ''),
            'HILLSBOROUGH': data.get('county', '').upper(),
            'Hillsborough County': f"{data.get('county', '')} County",
            'HILLSBOROUGH COUNTY': f"{data.get('county', '').upper()} COUNTY",
            
            # UCC Info
            'XXXXXXXXXXXXX': data.get('uccFilingNumber', ''),
            'xxxxxxxxxxxxxxxxx': data.get('uccFilingNumber', ''),
            'XXXXXXXXXXXXXX': data.get('uccFilingNumber', ''),
            'numberXXXXXXXXXXX': f"number{data.get('uccFilingNumber', '')}",
            'New York': data.get('uccFilingState', ''),
            'NEW YORK': data.get('uccFilingState', '').upper(),
            
            # Registered Mail
            'RF737860948US': data.get('registeredMailNumber', ''),
            '**RF737860948US**': f"**{data.get('registeredMailNumber', '')}**",
            'RF737860934US': data.get('registeredMailNumber', ''),  # Variant in docs
            
            # Financial routing
            '0810-0004-5': data.get('dtcRoutingNumber', ''),
            '????????': data.get('dtcRoutingNumber', ''),
            '053045139': data.get('dtcAccountNumber', ''),
            
            # Lien amounts
            '$100,000,000.00': lien_formatted,
            '\\$100,000,000.00': lien_formatted,
            'ONE HUNDRED MILLION': lien_words,
            'one hundred million': lien_words.lower(),
            '$100,000,000,000.00': f"${lien_amount * 1000:,.2f}",
            'ONE HUNDRED BILLION': self.number_to_words(lien_amount * 1000),
            
            # Document dates
            'April 7, 2025': doc_date_written,
            'April 7th, 2025': doc_date_written,
            'March 25, 2025': doc_date_written,
            'March 9, 2025': doc_date_written,
            '4/7/2025': doc_date if doc_date else '',
            
            # Birth info
            'October 12th 1962': birth_date_written,
            'October 12th, 1962': birth_date_written,
            '124-62-071026': data.get('birthCertNumber', ''),
            '109-71-015876': data.get('birthCertNumber', ''),
            '109-1971-015876': data.get('birthCertNumber', ''),
            
            # File reference numbers (keep template structure)
            'TKC020371ANP': f"{last[:3].upper() if last else 'XXX'}020371ANP",
            'TKC-101362HHIA': f"{last[:3].upper() if last else 'XXX'}-101362HHIA",
            'TKC-101262CLC': f"{last[:3].upper() if last else 'XXX'}-101262CLC",
            'TKC-101262-CAD': f"{last[:3].upper() if last else 'XXX'}-101262-CAD",
            '101262HHIA': f"101262HHIA",
            'JAD-SA020371': f"{last[:3].upper() if last else 'XXX'}-SA020371",
            'TKC -- 10121962': f"{last[:3].upper() if last else 'XXX'} -- {birth_date.replace('-', '') if birth_date else ''}",
        }
    
    def replace_text_in_file(self, content: str, replacements: dict) -> str:
        """Replace all occurrences in text content."""
        result = content
        
        # Sort by length (longest first) to avoid partial replacements
        sorted_items = sorted(replacements.items(), key=lambda x: len(x[0]), reverse=True)
        
        for old, new in sorted_items:
            if old and new:  # Skip empty values
                result = result.replace(old, str(new))
        
        return result
    
    def process_docx_xml(self, docx_path: str, replacements: dict, output_path: str):
        """Process DOCX by extracting, modifying XML, and repacking."""
        import zipfile
        import tempfile
        import shutil
        
        # Create temp directory
        with tempfile.TemporaryDirectory() as temp_dir:
            # Extract DOCX
            with zipfile.ZipFile(docx_path, 'r') as zf:
                zf.extractall(temp_dir)
            
            # Process XML files
            xml_files = [
                'word/document.xml',
                'word/header1.xml', 'word/header2.xml', 'word/header3.xml',
                'word/footer1.xml', 'word/footer2.xml', 'word/footer3.xml',
            ]
            
            for xml_file in xml_files:
                xml_path = os.path.join(temp_dir, xml_file)
                if os.path.exists(xml_path):
                    with open(xml_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    modified = self.replace_text_in_file(content, replacements)
                    
                    with open(xml_path, 'w', encoding='utf-8') as f:
                        f.write(modified)
            
            # Repack DOCX
            with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zf:
                for root, dirs, files in os.walk(temp_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, temp_dir)
                        zf.write(file_path, arcname)
    
    def generate_package(self, customer_data: dict, output_dir: str) -> dict:
        """Generate complete Treasury Package for a customer."""
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
        replacements = self.prepare_replacements(customer_data)
        
        # Get list of template documents
        templates = [f for f in os.listdir(self.template_dir) if f.endswith('.docx')]
        templates.sort()
        
        generated_files = []
        errors = []
        
        for template_name in templates:
            template_path = os.path.join(self.template_dir, template_name)
            
            # Create output filename with customer name
            last_name = customer_data.get('lastName', 'Customer')
            output_name = template_name.replace('_TKC', f'_{last_name}').replace('_JAD', f'_{last_name}')
            output_path = os.path.join(output_dir, output_name)
            
            try:
                self.process_docx_xml(template_path, replacements, output_path)
                generated_files.append(output_path)
                print(f"✓ Generated: {output_name}")
            except Exception as e:
                errors.append({'file': template_name, 'error': str(e)})
                print(f"✗ Error processing {template_name}: {e}")
        
        return {
            'generated': generated_files,
            'errors': errors,
            'output_dir': output_dir
        }
    
    def convert_all_to_pdf(self, docx_files: list) -> list:
        """Convert all DOCX files to PDF using LibreOffice."""
        import subprocess
        
        pdf_files = []
        for docx_path in docx_files:
            output_dir = os.path.dirname(docx_path)
            result = subprocess.run([
                'soffice', '--headless', '--convert-to', 'pdf',
                '--outdir', output_dir, docx_path
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                pdf_path = docx_path.replace('.docx', '.pdf')
                if os.path.exists(pdf_path):
                    pdf_files.append(pdf_path)
                    print(f"✓ Converted to PDF: {os.path.basename(pdf_path)}")
            else:
                print(f"✗ PDF conversion failed for {os.path.basename(docx_path)}")
        
        return pdf_files
    
    def merge_pdfs(self, pdf_files: list, output_path: str):
        """Merge multiple PDFs into single file."""
        from pypdf import PdfWriter, PdfReader
        
        writer = PdfWriter()
        
        for pdf_file in sorted(pdf_files):
            try:
                reader = PdfReader(pdf_file)
                for page in reader.pages:
                    writer.add_page(page)
            except Exception as e:
                print(f"Warning: Could not add {pdf_file}: {e}")
        
        with open(output_path, 'wb') as f:
            writer.write(f)
        
        print(f"✓ Merged PDF: {output_path}")
    
    def create_zip_package(self, files: list, output_path: str):
        """Create ZIP archive of all files."""
        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zf:
            for file_path in files:
                arcname = os.path.basename(file_path)
                zf.write(file_path, arcname)
        
        print(f"✓ Created ZIP: {output_path}")
    
    def generate_full_package(self, customer_data: dict, output_dir: str) -> dict:
        """Generate complete package with PDFs and ZIP."""
        
        # Step 1: Generate DOCX files
        result = self.generate_package(customer_data, output_dir)
        
        if not result['generated']:
            return result
        
        # Step 2: Convert to PDF
        pdf_files = self.convert_all_to_pdf(result['generated'])
        
        # Step 3: Merge PDFs
        last_name = customer_data.get('lastName', 'Customer')
        doc_date = customer_data.get('documentDate', 'undated')
        merged_pdf = os.path.join(output_dir, f'Treasury_Package_{last_name}_{doc_date}_COMPLETE.pdf')
        
        if pdf_files:
            self.merge_pdfs(pdf_files, merged_pdf)
        
        # Step 4: Create ZIP of individual PDFs
        zip_path = os.path.join(output_dir, f'Treasury_Package_{last_name}_{doc_date}_Individual_PDFs.zip')
        if pdf_files:
            self.create_zip_package(pdf_files, zip_path)
        
        result['pdf_files'] = pdf_files
        result['merged_pdf'] = merged_pdf
        result['zip_file'] = zip_path
        
        return result


def main():
    """Test the generator with sample data."""
    
    sample_data = {
        "firstName": "John",
        "middleName": "Michael", 
        "lastName": "Smith",
        "ssn": "123-45-6789",
        "birthDate": "1985-06-15",
        "birthState": "Texas",
        "birthCertNumber": "124-85-061589",
        "streetAddress": "456 Oak Lane",
        "city": "Houston",
        "county": "Harris",
        "state": "Texas",
        "zipCode": "77001",
        "uccFilingNumber": "202512345678",
        "uccFilingState": "New York",
        "registeredMailNumber": "RF123456789US",
        "dtcRoutingNumber": "0810-0001-2",
        "dtcAccountNumber": "012345678",
        "documentDate": "2025-01-15",
        "lienAmount": "100000000"
    }
    
    generator = TreasuryPackageGenerator('/home/claude')
    result = generator.generate_package(sample_data, '/home/claude/output_test')
    
    print(f"\n{'='*50}")
    print(f"Generated {len(result['generated'])} documents")
    if result['errors']:
        print(f"Errors: {len(result['errors'])}")
        for err in result['errors']:
            print(f"  - {err['file']}: {err['error']}")


if __name__ == '__main__':
    main()
