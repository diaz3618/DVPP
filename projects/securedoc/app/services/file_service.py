"""
File service with LFI and AFO vulnerabilities
"""

import os
from werkzeug.utils import secure_filename
from typing import Optional

class FileService:
    """Handle file operations with vulnerabilities"""
    
    def __init__(self, upload_folder: str):
        self.upload_folder = upload_folder
    
    def read_file(self, filename: str) -> Optional[str]:
        """
        Read file from filesystem
        VULNERABILITY: Local File Inclusion (LFI)
        """
        # Vulnerable: No path validation or sanitization
        file_path = os.path.join(self.upload_folder, filename)
        
        try:
            with open(file_path, 'r') as f:
                return f.read()
        except Exception as e:
            return None
    
    def read_file_absolute(self, path: str) -> Optional[str]:
        """
        Read file from absolute path
        VULNERABILITY: Local File Inclusion (LFI)
        """
        # Vulnerable: Allows reading any file on the system
        try:
            with open(path, 'r') as f:
                return f.read()
        except Exception as e:
            return None
    
    def write_file(self, filename: str, content: str) -> bool:
        """
        Write file to filesystem
        VULNERABILITY: Arbitrary File Overwrite (AFO)
        """
        # Vulnerable: No path validation, can write anywhere
        file_path = os.path.join(self.upload_folder, filename)
        
        try:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            with open(file_path, 'w') as f:
                f.write(content)
            return True
        except Exception as e:
            return False
    
    def write_to_path(self, path: str, content: str) -> bool:
        """
        Write file to specific path
        VULNERABILITY: Arbitrary File Overwrite (AFO)
        """
        # Vulnerable: User controls full file path
        try:
            with open(path, 'w') as f:
                f.write(content)
            return True
        except Exception as e:
            return False
    
    def save_upload(self, file) -> str:
        """
        Save uploaded file
        VULNERABILITY: Path traversal in uploaded filename
        """
        # Vulnerable: Uses user-provided filename without proper sanitization
        filename = file.filename
        
        # Weak sanitization (can be bypassed)
        if '..' in filename:
            # Simple check that can be bypassed
            filename = filename.replace('..', '')
        
        file_path = os.path.join(self.upload_folder, filename)
        file.save(file_path)
        
        return filename
    
    def get_file_path(self, filename: str) -> str:
        """
        Get full path to file
        VULNERABILITY: Path traversal if filename contains ../
        """
        # Vulnerable: Simple path join without validation
        return os.path.join(self.upload_folder, filename)
    
    def delete_file(self, filename: str) -> bool:
        """
        Delete file
        VULNERABILITY: Can delete any accessible file
        """
        # Vulnerable: No path validation
        file_path = os.path.join(self.upload_folder, filename)
        
        try:
            os.remove(file_path)
            return True
        except Exception:
            return False
    
    def list_files(self, directory: str = None) -> list:
        """
        List files in directory
        VULNERABILITY: Directory traversal
        """
        # Vulnerable: User can specify any directory
        if directory:
            path = os.path.join(self.upload_folder, directory)
        else:
            path = self.upload_folder
        
        try:
            return os.listdir(path)
        except Exception:
            return []
