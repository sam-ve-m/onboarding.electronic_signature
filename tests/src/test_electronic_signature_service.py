# Jormungandr - Onboarding
from func.src.services.electronic_signature import ElectronicSignatureService, UserElectronicSignatureAlreadyExists
from func.src.domain.exceptions import UserUniqueIdNotExists, ErrorOnUpdateUser, ErrorOnSendAuditLog
from .stubs import stub_unique_id, stub_user, stub_electronic_signature_validated, stub_user_updated, stub_user_not_updated

# Third party
from unittest.mock import patch
import pytest


@pytest.mark.asyncio
@patch("func.src.services.electronic_signature.UserRepository.find_one_by_unique_id", return_value={"stub": "stub"})
async def test_when_valid_user_and_signature_not_exists_then_return_true(mock_find_one):
    success = await ElectronicSignatureService._verify_user_and_electronic_signature_exists(
        unique_id=stub_unique_id
    )

    assert success is True


@pytest.mark.asyncio
@patch("func.src.services.electronic_signature.UserRepository.find_one_by_unique_id", return_value=None)
async def test_when_invalid_user_then_raises(mock_find_one):
    with pytest.raises(UserUniqueIdNotExists):
        await ElectronicSignatureService._verify_user_and_electronic_signature_exists(
            unique_id=stub_unique_id
        )


@pytest.mark.asyncio
@patch("func.src.services.electronic_signature.UserRepository.find_one_by_unique_id", return_value=stub_user)
async def test_when_valid_user_and_electronic_signature_exists_then_raises(mock_find_one):
    with pytest.raises(UserElectronicSignatureAlreadyExists):
        await ElectronicSignatureService._verify_user_and_electronic_signature_exists(
            unique_id=stub_unique_id
        )


@pytest.mark.asyncio
@patch("func.src.services.electronic_signature.UserRepository.update_one_with_electronic_signature",
       return_value=stub_user_updated)
@patch("func.src.services.electronic_signature.Audit.register_log")
@patch.object(ElectronicSignatureService, "_verify_user_and_electronic_signature_exists")
async def test_when_set_electronic_signature_with_success_then_return_true(mock_signature_exists, mock_audit, mock_update):
    success = await ElectronicSignatureService.set_on_user(
        unique_id=stub_unique_id,
        electronic_signature_validated=stub_electronic_signature_validated
    )

    assert success is True


@pytest.mark.asyncio
@patch("func.src.services.electronic_signature.UserRepository.update_one_with_electronic_signature",
       return_value=stub_user_not_updated)
@patch("func.src.services.electronic_signature.Audit.register_log")
@patch.object(ElectronicSignatureService, "_verify_user_and_electronic_signature_exists")
async def test_when_update_user_with_electronic_signature_then_raises(mock_signature_exists, mock_audit, mock_update):
    with pytest.raises(ErrorOnUpdateUser):
        await ElectronicSignatureService.set_on_user(
            unique_id=stub_unique_id,
            electronic_signature_validated=stub_electronic_signature_validated
        )


@pytest.mark.asyncio
@patch("func.src.transports.audit.transport.Audit.audit_client.send_to_persephone", return_value=(False, "teste"))
@patch.object(ElectronicSignatureService, "_verify_user_and_electronic_signature_exists")
async def test_when_fail_to_send_audit_log_then_raises(mock_signature_exists, mock_audit):
    with pytest.raises(ErrorOnSendAuditLog):
        await ElectronicSignatureService.set_on_user(
            unique_id=stub_unique_id,
            electronic_signature_validated=stub_electronic_signature_validated
        )
