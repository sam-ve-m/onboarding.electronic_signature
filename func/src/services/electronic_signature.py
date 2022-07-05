# Jormungandr - Onboarding
from ..repositories.mongo_db.user.repository import UserRepository
from ..domain.exceptions import UserUniqueIdNotExists, UserElectronicSignatureAlreadyExists


class ElectronicSignatureService:

    @classmethod
    async def set(cls, unique_id: str, electronic_signature: dict ):

        return True

    @classmethod
    async def _verify_user_electronic_signature_exists(cls, unique_id: str) -> True:
        user = await UserRepository.find_one_by_unique_id(unique_id=unique_id)
        if not user:
            raise UserUniqueIdNotExists
        electronic_signature = user.get("electronic_signature")
        if electronic_signature:
            raise UserElectronicSignatureAlreadyExists
        return True
