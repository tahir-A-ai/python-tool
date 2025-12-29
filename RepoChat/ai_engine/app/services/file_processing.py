import os
import zipfile
import shutil
import tempfile
from typing import List, Dict

class FileProcessor:
    """
    Handles the extraction, reading, and cleaning of code repositories.
    """
    
    # Whitelist: Only process these files to avoid reading binary/junk files
    SUPPORTED_EXTENSIONS = {'.py', '.js', '.ts', '.html', '.css', '.md', '.txt', '.json', '.java', '.cpp'}

    def process_zip(self, zip_path: str) -> List[Dict]:
        """
        Main entry point: Unzips, reads files, and returns a list of documents.
        Returns: [{'text': '...', 'metadata': {'source': 'main.py'}}, ...]
        """
        extracted_docs = []
        
        # creating a tenp-Dir to save the unzip file, after processing , we can delete this 
        # to avoid saving unnccessary files on the server
        temp_dir = tempfile.mkdtemp()
        
        try:
            # Extracting the Zip
            if not os.path.exists(zip_path):
                raise FileNotFoundError(f"Zip file not found at: {zip_path}")
                
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)
            
            # Walk through the files
            extracted_docs = self._read_files_recursively(temp_dir)
            
        except zipfile.BadZipFile:
            print(f"Error: The file at {zip_path} is not a valid zip.")
        except Exception as e:
            print(f"Error processing file: {e}")
        finally:
            # cleanup: delete the temp folder, even if errors occurred
            shutil.rmtree(temp_dir)
            
        return extracted_docs

    def _read_files_recursively(self, root_dir: str) -> List[Dict]:
        docs = []
        
        for root, _, files in os.walk(root_dir):
            for file in files:
                # split filename and extension > ['main', '.py']
                _, ext = os.path.splitext(file)
                # check if the extension is in supported extensions list
                if ext.lower() in self.SUPPORTED_EXTENSIONS:
                    # combine root folder and file name
                    file_path = os.path.join(root, file)
                    relative_path = os.path.relpath(file_path, root_dir)
                    
                    try:
                        # 'errors=ignore' tells python to ignore the weird characters, emojis 
                        # that you can't read instead of crashing
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()
                            
                        # Skip empty files
                        if not content.strip():
                            continue

                        # Create the Document Object
                        docs.append({
                            "text": content,
                            "metadata": {
                                "source": relative_path,
                                "extension": ext
                            }
                        })
                    except Exception as e:
                        print(f"Skipped file {file}: {e}")
                        
        return docs

    def chunk_text(self, text: str, chunk_size: int = 1000, overlap: int = 100) -> List[str]:
        """
        Splits long text into smaller overlapping chunks.
        """
        if not text:
            return []
            
        chunks = []
        start = 0
        text_len = len(text)
        
        while start < text_len:
            end = start + chunk_size
            chunk = text[start:end]
            chunks.append(chunk)
            
            # Stop if we reached the end
            if end >= text_len:
                break
                
            # Move forward, but step back by 'overlap' amount
            start += (chunk_size - overlap)
            
        return chunks