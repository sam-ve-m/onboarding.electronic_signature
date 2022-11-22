class ErrorOnDecodeJwt(Exception):
    msg = "Jormungandr-Onboarding::decode_jwt::Fail when trying to decode jwt"


class ErrorOnGetUniqueId(Exception):
    msg = "Jormungandr-Onboarding::get_unique_id::Fail when trying to get unique_id"


class ErrorOnEncryptElectronicSignature(Exception):
    msg = "Jormungandr-Onboarding::encrypt_password::Fail when trying to encrypt electronic signature"


class UserUniqueIdNotExists(Exception):
    msg = "Jormungandr-Onboarding::_verify_user_and_electronic_signature_exists::Not exists an user with this unique_id"


class UserElectronicSignatureAlreadyExists(Exception):
    msg = (
        "Jormungandr-Onboarding::_verify_user_and_electronic_signature_exists::User electronic signature already"
        " exists"
    )


class ErrorOnSendAuditLog(Exception):
    msg = (
        "Jormungandr-Onboarding::set_electronic_signature::Error when trying to send log audit on "
        "Persephone"
    )


class ErrorOnUpdateUser(Exception):
    msg = "Jormungandr-Onboarding::set_electronic_signature::Error on trying to update user in mongo_db"


class OnboardingStepsStatusCodeNotOk(Exception):
    msg = "Jormungandr-Onboarding::get_user_current_step::Error when trying to get onboarding steps br"


class InvalidOnboardingCurrentStep(Exception):
    msg = "Jormungandr-Onboarding::validate_current_onboarding_step::User is not in the electronic signature step"


class DeviceInfoRequestFailed(Exception):
    msg = "Error trying to get device info"


class DeviceInfoNotSupplied(Exception):
    msg = "Device info not supplied"
