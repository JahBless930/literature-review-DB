from supabase import create_client, Client
from fastapi import UploadFile, HTTPException
import os
import uuid
import io
import asyncio
from typing import Dict, Any, Optional, Union
from ..core.config import settings

class SupabaseStorageService:
    def __init__(self):
        """Initialize Supabase Storage Service"""
        if not settings.has_supabase:
            raise ValueError("Supabase credentials not configured")
        
        try:
            # Initialize Supabase client
            self.supabase: Client = create_client(
                settings.SUPABASE_URL,
                settings.SUPABASE_ANON_KEY
            )
            self.bucket_name = settings.SUPABASE_BUCKET_NAME
            
            # Verify connection
            self._verify_connection()
            print(f"✅ Supabase Storage initialized successfully")
            
        except Exception as e:
            print(f"❌ Supabase Storage initialization failed: {str(e)}")
            raise e
    
    def _verify_connection(self) -> bool:
        """Verify bucket exists and is accessible"""
        try:
            # Simple bucket access test
            self.supabase.storage.from_(self.bucket_name).list()
            print(f"✅ Bucket '{self.bucket_name}' is accessible")
            return True
        except Exception as e:
            print(f"⚠️  Bucket verification failed: {str(e)}")
            # Don't raise error - bucket might exist but be empty
            return False
    
    async def upload_file(
        self, 
        file: UploadFile, 
        folder: str = "projects", 
        filename: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Upload file to Supabase Storage
        
        Args:
            file: FastAPI UploadFile object
            folder: Folder path in bucket (default: "projects")
            filename: Custom filename (optional, will generate UUID if not provided)
            
        Returns:
            Dict with upload result information
        """
        try:
            # Validate file
            await self._validate_file(file)
            
            # Read file content
            file_content = await file.read()
            file_size = len(file_content)
            
            print(f"📁 Uploading: {file.filename} ({file_size / 1024 / 1024:.2f} MB)")
            
            # Generate unique filename
            if not filename:
                file_extension = self._get_file_extension(file.filename)
                filename = f"{uuid.uuid4()}{file_extension}"
            
            # Create full storage path
            storage_path = f"{folder}/{filename}" if folder else filename
            
            # Upload file with retry logic
            upload_result = await self._upload_with_retry(
                file_content, 
                storage_path, 
                file.content_type
            )
            
            # Generate public URL
            public_url = self._get_public_url(storage_path)
            
            # Return upload information
            result = {
                "path": storage_path,
                "url": public_url,
                "size": file_size,
                "content_type": file.content_type or "application/octet-stream",
                "storage": "supabase",
                "original_filename": file.filename
            }
            
            print(f"✅ Upload successful: {storage_path}")
            return result
            
        except HTTPException:
            raise
        except Exception as e:
            error_msg = f"Upload failed for {file.filename}: {str(e)}"
            print(f"❌ {error_msg}")
            raise HTTPException(status_code=500, detail=error_msg)
    
    async def _validate_file(self, file: UploadFile) -> None:
        """Validate file before upload"""
        if not file.filename:
            raise HTTPException(status_code=400, detail="No filename provided")
        
        # Check file extension
        file_extension = self._get_file_extension(file.filename).lower()
        if file_extension not in settings.ALLOWED_FILE_TYPES:
            raise HTTPException(
                status_code=400,
                detail=f"File type {file_extension} not allowed. Allowed: {', '.join(settings.ALLOWED_FILE_TYPES)}"
            )
        
        # Check file size (read a bit to check)
        current_pos = file.file.tell()
        file.file.seek(0, 2)  # Seek to end
        file_size = file.file.tell()
        file.file.seek(current_pos)  # Reset position
        
        if file_size > settings.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=413,
                detail=f"File too large: {file_size / 1024 / 1024:.1f}MB. Max: {settings.MAX_FILE_SIZE / 1024 / 1024:.1f}MB"
            )
    
    def _get_file_extension(self, filename: str) -> str:
        """Get file extension, default to .pdf if none"""
        if not filename:
            return '.pdf'
        extension = os.path.splitext(filename)[1]
        return extension if extension else '.pdf'
    
    async def _upload_with_retry(
        self, 
        file_content: bytes, 
        storage_path: str, 
        content_type: str,
        max_retries: int = 3
    ) -> Any:
        """Upload file with retry logic and timeout"""
        
        for attempt in range(max_retries):
            try:
                print(f"🔄 Upload attempt {attempt + 1}/{max_retries}")
                
                # Try upload with timeout
                upload_task = self._perform_upload(file_content, storage_path, content_type)
                result = await asyncio.wait_for(upload_task, timeout=45.0)
                
                print(f"✅ Upload attempt {attempt + 1} successful")
                return result
                
            except asyncio.TimeoutError:
                print(f"⏰ Upload attempt {attempt + 1} timed out")
                if attempt == max_retries - 1:
                    raise HTTPException(
                        status_code=408,
                        detail="Upload timed out. Please try with a smaller file."
                    )
                
            except Exception as e:
                print(f"❌ Upload attempt {attempt + 1} failed: {str(e)}")
                if attempt == max_retries - 1:
                    raise HTTPException(
                        status_code=500,
                        detail=f"Upload failed after {max_retries} attempts: {str(e)}"
                    )
            
            # Wait before retry (exponential backoff)
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt
                print(f"⏳ Waiting {wait_time}s before retry...")
                await asyncio.sleep(wait_time)
    
    async def _perform_upload(self, file_content: bytes, storage_path: str, content_type: str) -> Any:
        """Perform the actual upload to Supabase"""
        try:
            # Primary upload method
            result = self.supabase.storage.from_(self.bucket_name).upload(
                path=storage_path,
                file=file_content,
                file_options={
                    "content-type": content_type or "application/octet-stream",
                    "upsert": True
                }
            )
            return result
            
        except Exception as e:
            print(f"⚠️  Primary upload method failed: {str(e)}")
            
            # Fallback: Try with BytesIO
            try:
                print("🔄 Trying BytesIO fallback...")
                file_obj = io.BytesIO(file_content)
                result = self.supabase.storage.from_(self.bucket_name).upload(
                    path=storage_path,
                    file=file_obj,
                    file_options={
                        "content-type": content_type or "application/octet-stream",
                        "upsert": True
                    }
                )
                return result
            except Exception as e2:
                print(f"❌ BytesIO fallback also failed: {str(e2)}")
                raise e2
    
    def _get_public_url(self, storage_path: str) -> str:
        """Get public URL for uploaded file"""
        try:
            return self.supabase.storage.from_(self.bucket_name).get_public_url(storage_path)
        except Exception as e:
            print(f"⚠️  Could not generate public URL: {str(e)}")
            # Return a fallback URL format
            return f"{settings.SUPABASE_URL}/storage/v1/object/public/{self.bucket_name}/{storage_path}"
    
    async def delete_file(self, file_path: str) -> bool:
        """
        Delete file from Supabase Storage
        
        Args:
            file_path: Path to file in storage
            
        Returns:
            True if deletion successful, False otherwise
        """
        try:
            print(f"🗑️  Deleting file: {file_path}")
            
            result = self.supabase.storage.from_(self.bucket_name).remove([file_path])
            
            # Check if deletion was successful
            if isinstance(result, list) and len(result) > 0:
                print(f"✅ File deleted successfully: {file_path}")
                return True
            else:
                print(f"⚠️  File deletion returned empty result: {file_path}")
                return False
                
        except Exception as e:
            print(f"❌ Error deleting file {file_path}: {str(e)}")
            return False
    
    def get_file_url(self, file_path: str) -> str:
        """
        Get public URL for a file
        
        Args:
            file_path: Path to file in storage
            
        Returns:
            Public URL string
        """
        return self._get_public_url(file_path)
    
    def list_files(self, folder: str = "") -> list:
        """
        List files in a folder
        
        Args:
            folder: Folder path (empty string for root)
            
        Returns:
            List of file objects
        """
        try:
            # Use simple list without limit parameter
            if folder:
                result = self.supabase.storage.from_(self.bucket_name).list(folder)
            else:
                result = self.supabase.storage.from_(self.bucket_name).list()
            
            files = result if result else []
            print(f"📂 Found {len(files)} files in folder: {folder or 'root'}")
            return files
            
        except Exception as e:
            print(f"❌ Error listing files in {folder or 'root'}: {str(e)}")
            return []
    
    def get_file_info(self, file_path: str) -> Optional[Dict[str, Any]]:
        """
        Get information about a specific file
        
        Args:
            file_path: Path to file in storage
            
        Returns:
            File information dict or None if not found
        """
        try:
            # Extract folder and filename
            folder = os.path.dirname(file_path)
            filename = os.path.basename(file_path)
            
            # List files in folder
            files = self.list_files(folder)
            
            # Find specific file
            for file_obj in files:
                if file_obj.get('name') == filename:
                    return {
                        'name': file_obj.get('name'),
                        'size': file_obj.get('metadata', {}).get('size'),
                        'last_modified': file_obj.get('updated_at'),
                        'content_type': file_obj.get('metadata', {}).get('mimetype'),
                        'url': self.get_file_url(file_path)
                    }
            
            return None
            
        except Exception as e:
            print(f"❌ Error getting file info for {file_path}: {str(e)}")
            return None
    
    def health_check(self) -> Dict[str, Any]:
        """
        Check health of Supabase Storage connection
        
        Returns:
            Health status information
        """
        try:
            # Try to list files as a health check
            files = self.list_files()
            
            return {
                "status": "healthy",
                "bucket": self.bucket_name,
                "accessible": True,
                "file_count": len(files),
                "url": settings.SUPABASE_URL
            }
            
        except Exception as e:
            return {
                "status": "unhealthy",
                "bucket": self.bucket_name,
                "accessible": False,
                "error": str(e),
                "url": settings.SUPABASE_URL
            }

# Initialize service with proper error handling
try:
    if settings.has_supabase:
        supabase_storage = SupabaseStorageService()
    else:
        print("⚠️  Supabase credentials not configured")
        supabase_storage = None
except Exception as e:
    print(f"⚠️  Supabase Storage initialization failed: {str(e)}")
    supabase_storage = None

# Export for easy importing
__all__ = ["supabase_storage", "SupabaseStorageService"]
