import pytest

from src.company.domain.enums.company_user_invitation_status import CompanyUserInvitationStatus


class TestCompanyUserInvitationStatus:
    """Tests for CompanyUserInvitationStatus enum"""

    def test_enum_has_all_required_values(self):
        """Test that enum has all required status values"""
        assert CompanyUserInvitationStatus.PENDING == "pending"
        assert CompanyUserInvitationStatus.ACCEPTED == "accepted"
        assert CompanyUserInvitationStatus.REJECTED == "rejected"
        assert CompanyUserInvitationStatus.EXPIRED == "expired"
        assert CompanyUserInvitationStatus.CANCELLED == "cancelled"

    def test_enum_values_are_strings(self):
        """Test that all enum values are strings"""
        assert isinstance(CompanyUserInvitationStatus.PENDING.value, str)
        assert isinstance(CompanyUserInvitationStatus.ACCEPTED.value, str)
        assert isinstance(CompanyUserInvitationStatus.REJECTED.value, str)
        assert isinstance(CompanyUserInvitationStatus.EXPIRED.value, str)
        assert isinstance(CompanyUserInvitationStatus.CANCELLED.value, str)

    def test_enum_is_comparable(self):
        """Test that enum values can be compared"""
        assert CompanyUserInvitationStatus.PENDING != CompanyUserInvitationStatus.ACCEPTED
        assert CompanyUserInvitationStatus.PENDING == CompanyUserInvitationStatus.PENDING

