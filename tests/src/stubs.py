# Jormungandr - Onboarding
from func.src.domain.validator import ElectronicSignature


class UserUpdated:
    def __init__(self, matched_count=0):
        self.matched_count = matched_count


stub_unique_id = "40db7fee-6d60-4d73-824f-1bf87edc4491"
stub_user = {"electronic_signature": "stub"}
stub_user_not_updated = UserUpdated(matched_count=0)
stub_user_updated = UserUpdated(matched_count=1)
stub_raw_payload = {"electronic_signature": "aB2c354Cd"}
stub_electronic_signature_str = "aB2c354Cd"
stub_payload_validated = ElectronicSignature(**stub_raw_payload).dict()
stub_mist_result = {"encrypted_password": "stub"}
