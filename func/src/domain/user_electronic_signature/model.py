from ..enums.user import UserLevel
from ..models.device_info import DeviceInfo


class UserElectronicSignature:
    def __init__(
        self,
        electronic_signature: str,
        encrypted_electronic_signature: str,
        unique_id: str,
        device_info: DeviceInfo,
    ):
        self.electronic_signature_not_encrypted = electronic_signature
        self.unique_id = unique_id
        self.encrypted_electronic_signature = encrypted_electronic_signature
        self.user_level = UserLevel.CLIENT
        self.is_blocked_electronic_signature = False
        self.electronic_signature_wrong_attempts = 0
        self.device_info = device_info

    async def get_user_update_template(self) -> dict:
        template = {
            "scope.user_level": self.user_level,
            "electronic_signature": self.encrypted_electronic_signature,
            "is_blocked_electronic_signature": self.is_blocked_electronic_signature,
            "electronic_signature_wrong_attempts": self.electronic_signature_wrong_attempts,
        }
        return template

    async def get_user_electronic_signature_template(self) -> dict:
        template = {
            "unique_id": self.unique_id,
            "electronic_signature": self.electronic_signature_not_encrypted,
            "is_blocked_electronic_signature": self.is_blocked_electronic_signature,
            "electronic_signature_wrong_attempts": self.electronic_signature_wrong_attempts,
            "device_info": self.device_info.device_info,
            "device_id": self.device_info.device_id,
        }
        return template
