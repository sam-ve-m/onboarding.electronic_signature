# Jormungandr - Onboarding
from ..domain.exceptions import ErrorOnEncryptElectronicSignature

# Third party
from etria_logger import Gladsheim
from mist_client import Mist, MistStatusResponses


class SecurityService:

    mist = Mist

    @classmethod
    async def encrypt_password(cls, electronic_signature: str):
        result, status = await cls.mist.generate_encrypted_password(
            user_password=electronic_signature
        )
        if status != MistStatusResponses.SUCCESS:
            Gladsheim.error(
                message=f"Error when encrypt password: {MistStatusResponses.SUCCESS.value}"
            )
            raise ErrorOnEncryptElectronicSignature
        return result["encrypted_password"]
