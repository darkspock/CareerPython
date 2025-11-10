#!/usr/bin/env python3
"""
Script to delete a company by ID
Usage: python scripts/delete_company.py <company_id>
"""
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.container import Container
from src.company_bc.company.domain.value_objects.company_id import CompanyId
from src.company_bc.company.application.commands.delete_company_command import DeleteCompanyCommand


def delete_company(company_id: str):
    """Delete a company by ID"""
    container = Container()
    command_bus = container.command_bus()
    
    try:
        company_id_vo = CompanyId.from_string(company_id)
        command = DeleteCompanyCommand(id=company_id_vo)
        
        print(f"Deleting company {company_id}...")
        command_bus.dispatch(command)
        print(f"✅ Company {company_id} deleted successfully (soft delete)")
        
    except Exception as e:
        print(f"❌ Error deleting company: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python scripts/delete_company.py <company_id>")
        sys.exit(1)
    
    company_id = sys.argv[1]
    delete_company(company_id)

