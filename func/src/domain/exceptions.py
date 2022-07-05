class ErrorOnDecodeJwt(Exception):
    msg = "Jormungandr-Onboarding::decode_jwt_and_get_unique_id::Fail when trying to get unique id," \
          " jwt not decoded successfully"


class UserUniqueIdNotExists(Exception):
    msg = "Jormungandr-Onboarding::get_registration_data::Not exists an user with this unique_id"


class UserElectronicSignatureAlreadyExists(Exception):
    mas = ''
