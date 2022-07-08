from func.src.domain.validator import ElectronicSignature


class UserUpdated:
    def __init__(self, acknowledged=None):
        self.acknowledged = acknowledged


stub_unique_id = "40db7fee-6d60-4d73-824f-1bf87edc4491"
stub_user = {
    "electronic_signature": "stub"
}
stub_user_not_updated = UserUpdated(acknowledged=False)
stub_user_updated = UserUpdated(acknowledged=True)
stub_raw_electronic_signature = {
    "electronic_signature": "aB2c354Cd"
}
stub_electronic_signature_str = "aB2c354Cd"
stub_electronic_signature_validated = ElectronicSignature(**stub_raw_electronic_signature).dict()
stub_mist_result = {
    "encrypted_password": "stub"
}
