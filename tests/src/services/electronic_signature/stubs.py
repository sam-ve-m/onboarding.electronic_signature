from func.src.domain.user_electronic_signature.model import UserElectronicSignature
from func.src.domain.validators.validator import ElectronicSignature
from src.domain.models.device_info import DeviceInfo


class UserUpdated:
    def __init__(self, matched_count=0):
        self.matched_count = matched_count


stub_unique_id = "40db7fee-6d60-4d73-824f-1bf87edc4491"
stub_user = {"electronic_signature": "stub"}
stub_user_not_updated = UserUpdated(matched_count=0)
stub_user_updated = UserUpdated(matched_count=1)
stub_raw_payload = {"electronic_signature": "aB2c354Cd"}
stub_electronic_signature_str = "aB2c354Cd"
stub_payload_validated = ElectronicSignature(**stub_raw_payload)
stub_mist_result = {"encrypted_password": "stub"}
stub_device_info = DeviceInfo({"precision": 1}, "")
stub_user_electronic_signature_model = UserElectronicSignature(
    electronic_signature=stub_payload_validated.electronic_signature,
    unique_id=stub_unique_id,
    encrypted_electronic_signature="12345678910",
    device_info=stub_device_info,
)
