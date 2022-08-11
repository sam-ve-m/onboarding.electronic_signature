# Jormungandr - Onboarding
from .security import SecurityService
from ..domain.enums.user import UserOnboardingStep
from ..domain.exceptions import (
    UserUniqueIdNotExists,
    UserElectronicSignatureAlreadyExists,
    ErrorOnUpdateUser,
    InvalidOnboardingCurrentStep,
)
from ..domain.user_electronic_signature.model import UserElectronicSignature
from ..repositories.mongo_db.user.repository import UserRepository
from ..transports.audit.transport import Audit
from ..transports.onboarding_steps.transport import OnboardingSteps


class ElectronicSignatureService:
    @staticmethod
    async def validate_current_onboarding_step(jwt: str) -> bool:
        user_current_step = await OnboardingSteps.get_user_current_step(jwt=jwt)
        if not user_current_step == UserOnboardingStep.ELECTRONIC_SIGNATURE:
            raise InvalidOnboardingCurrentStep
        return True

    @staticmethod
    async def set_on_user(unique_id: str, payload_validated: dict) -> bool:
        await ElectronicSignatureService._verify_user_and_electronic_signature_exists(
            unique_id=unique_id
        )
        electronic_signature = payload_validated.get("electronic_signature")
        encrypted_electronic_signature = await SecurityService.encrypt_password(
            electronic_signature=electronic_signature
        )
        electronic_signature_model = UserElectronicSignature(
            unique_id=unique_id,
            electronic_signature=electronic_signature,
            encrypted_electronic_signature=encrypted_electronic_signature,
        )
        await Audit.register_log(electronic_signature_model=electronic_signature_model)
        user_electronic_signature = (
            await electronic_signature_model.get_user_update_template()
        )
        user_updated = await UserRepository.update_one_with_electronic_signature(
            unique_id=unique_id, user_electronic_signature=user_electronic_signature
        )
        if not user_updated.matched_count:
            raise ErrorOnUpdateUser
        return True

    @staticmethod
    async def _verify_user_and_electronic_signature_exists(unique_id: str) -> bool:
        user = await UserRepository.find_one_by_unique_id(unique_id=unique_id)
        if not user:
            raise UserUniqueIdNotExists
        electronic_signature = user.get("electronic_signature")
        if electronic_signature:
            raise UserElectronicSignatureAlreadyExists
        return True
