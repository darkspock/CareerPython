import pytest

from src.company.domain.value_objects.invitation_token import InvitationToken


class TestInvitationToken:
    """Tests for InvitationToken value object"""

    def test_generate_creates_valid_token(self):
        """Test that generate() creates a valid token"""
        token = InvitationToken.generate()
        
        assert token is not None
        assert isinstance(token.value, str)
        assert len(token.value) >= 16

    def test_from_string_creates_token(self):
        """Test that from_string creates a token from string"""
        token_str = "test_token_string_12345"
        token = InvitationToken.from_string(token_str)
        
        assert token.value == token_str

    def test_from_string_raises_on_empty(self):
        """Test that from_string raises error on empty string"""
        with pytest.raises(ValueError, match="Token string cannot be empty"):
            InvitationToken.from_string("")

    def test_constructor_raises_on_empty_value(self):
        """Test that constructor raises error on empty value"""
        with pytest.raises(ValueError, match="InvitationToken cannot be empty"):
            InvitationToken("")

    def test_constructor_raises_on_short_token(self):
        """Test that constructor raises error on token shorter than 16 chars"""
        with pytest.raises(ValueError, match="InvitationToken must be at least 16 characters"):
            InvitationToken("short")

    def test_token_is_immutable(self):
        """Test that token is immutable (frozen dataclass)"""
        token = InvitationToken.generate()
        
        with pytest.raises(Exception):  # dataclass frozen should raise
            token.value = "new_value"

    def test_tokens_are_comparable(self):
        """Test that tokens can be compared"""
        same_token_str = "same_token_1234567890"  # At least 16 chars
        different_token_str = "different_token_123456"
        
        token1 = InvitationToken.from_string(same_token_str)
        token2 = InvitationToken.from_string(same_token_str)
        token3 = InvitationToken.from_string(different_token_str)
        
        assert token1 == token2
        assert token1 != token3

    def test_token_hashable(self):
        """Test that token is hashable"""
        token = InvitationToken.generate()
        
        token_set = {token}
        assert token in token_set

