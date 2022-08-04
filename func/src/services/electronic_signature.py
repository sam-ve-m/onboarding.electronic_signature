# Jormungandr - Onboarding
from ..repositories.mongo_db.user.repository import UserRepository
from ..domain.exceptions import UserUniqueIdNotExists, UserElectronicSignatureAlreadyExists, ErrorOnUpdateUser
from ..domain.user_electronic_signature.model import UserElectronicSignature
from ..transports.audit.transport import Audit
from .security import SecurityService


class ElectronicSignatureService:

    @staticmethod
    async def set_on_user(unique_id: str, electronic_signature_validated: dict):
        # TODO: Onboarding step validator
        await ElectronicSignatureService._verify_user_and_electronic_signature_exists(unique_id=unique_id)
        electronic_signature = electronic_signature_validated.get("electronic_signature")
        encrypted_electronic_signature = await SecurityService.encrypt_password(
            electronic_signature=electronic_signature
        )
        electronic_signature_model = UserElectronicSignature(
            unique_id=unique_id,
            electronic_signature=electronic_signature,
            encrypted_electronic_signature=encrypted_electronic_signature
        )
        await Audit.register_log(electronic_signature_model=electronic_signature_model)
        user_electronic_signature = await electronic_signature_model.get_user_update_template()
        user_updated = await UserRepository.update_one_with_electronic_signature(
            unique_id=unique_id,
            user_electronic_signature=user_electronic_signature
        )
        if not user_updated.acknowledged:
            raise ErrorOnUpdateUser
        return True

    @staticmethod
    async def _verify_user_and_electronic_signature_exists(unique_id: str) -> True:
        user = await UserRepository.find_one_by_unique_id(unique_id=unique_id)
        if not user:
            raise UserUniqueIdNotExists
        electronic_signature = user.get("electronic_signature")
        if electronic_signature:
            raise UserElectronicSignatureAlreadyExists
        return True
