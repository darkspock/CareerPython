#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.candidate.infrastructure.models.file_attachment_model import FileAttachmentModel
from src.candidate.infrastructure.repositories.file_attachment_repository import FileAttachmentRepository
from src.shared.domain.entities.base import generate_id
from datetime import datetime

def test_file_save():
    print("Testing file save...")
    
    # Create a test file attachment
    file_attachment = FileAttachmentModel(
        id=generate_id(),
        candidate_id="01K8S2VPJX9Z9TEM2W7NPSGG0T",
        filename="test.txt",
        original_name="test.txt",
        file_path="test/path/test.txt",
        file_url="http://localhost:8000/uploads/test/path/test.txt",
        content_type="text/plain",
        file_size=100,
        description="Test file",
        uploaded_at=datetime.utcnow()
    )
    
    print(f"Created file_attachment with file_path = {file_attachment.file_path}")
    print(f"Created file_attachment with file_url = {file_attachment.file_url}")
    
    # Save to database
    repository = FileAttachmentRepository()
    saved_file = repository.save(file_attachment)
    
    print(f"Saved file_attachment with file_path = {saved_file.file_path}")
    print(f"Saved file_attachment with file_url = {saved_file.file_url}")
    
    # Retrieve from database
    retrieved_file = repository.get_by_id(saved_file.id)
    if retrieved_file:
        print(f"Retrieved file_attachment with file_path = {retrieved_file.file_path}")
        print(f"Retrieved file_attachment with file_url = {retrieved_file.file_url}")
    else:
        print("Failed to retrieve file from database")

if __name__ == "__main__":
    test_file_save()
