# Jormungandr - Onboarding
from func.src.services.security import SecurityService
from func.src.domain.exceptions import ErrorOnEncryptElectronicSignature
from tests.src.stubs import stub_electronic_signature_str, stub_mist_result

# Standards
from unittest.mock import patch

# Third party
from mist_client import MistStatusResponses
import pytest


@pytest.mark.asyncio
@patch(
    "func.src.services.security.SecurityService.mist.generate_encrypted_password",
    return_value=("test", False),
)
async def test_when_encrypt_failed_then_raises(mock_mist):
    with pytest.raises(ErrorOnEncryptElectronicSignature):
        await SecurityService.encrypt_password(
            electronic_signature=stub_electronic_signature_str
        )


@pytest.mark.asyncio
@patch(
    "func.src.services.security.SecurityService.mist.generate_encrypted_password",
    return_value=(stub_mist_result, MistStatusResponses.SUCCESS),
)
async def test_when_encrypt_success_then_return_encrypted_password(mock_mist):
    result = await SecurityService.encrypt_password(
        electronic_signature=stub_electronic_signature_str
    )

    assert result is "stub"
