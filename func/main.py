# Jormungandr - Onboarding
from src.domain.response.model import ResponseModel
from src.domain.enums.code import InternalCode
from src.domain.validator import ElectronicSignature
from src.domain.exceptions import (
    ErrorOnUpdateUser,
    UserUniqueIdNotExists,
    ErrorOnDecodeJwt,
    ErrorOnSendAuditLog,
    UserElectronicSignatureAlreadyExists,
    ErrorOnEncryptElectronicSignature
)
from src.services.jwt import JwtService
from src.services.electronic_signature import ElectronicSignatureService

# Standards
from http import HTTPStatus

# Third party
from etria_logger import Gladsheim
from flask import request, Response


async def set_electronic_signature() -> Response:
    raw_electronic_signature = request.json
    jwt = request.headers.get("x-thebes-answer")
    msg_error = "Unexpected error occurred"
    try:
        unique_id = await JwtService.decode_jwt_and_get_unique_id(jwt=jwt)
        electronic_signature_validated = ElectronicSignature(**raw_electronic_signature).dict()
        success = await ElectronicSignatureService.set_on_user(
            unique_id=unique_id,
            electronic_signature_validated=electronic_signature_validated
        )
        response = ResponseModel(
            success=success,
            code=InternalCode.SUCCESS,
            message="Electronic signature successfully created",
        ).build_http_response(status=HTTPStatus.OK)
        return response

    except ErrorOnDecodeJwt as ex:
        Gladsheim.error(error=ex, message=ex.msg)
        response = ResponseModel(
            success=False, code=InternalCode.JWT_INVALID, message='Unauthorized token'
        ).build_http_response(status=HTTPStatus.UNAUTHORIZED)
        return response

    except UserUniqueIdNotExists as ex:
        Gladsheim.info(error=ex, message=ex.msg)
        response = ResponseModel(
            success=False, code=InternalCode.DATA_NOT_FOUND, message='User unique_id not exists'
        ).build_http_response(status=HTTPStatus.BAD_REQUEST)
        return response

    except UserElectronicSignatureAlreadyExists as ex:
        Gladsheim.info(error=ex, message=ex.msg)
        response = ResponseModel(
            success=False, code=InternalCode.DATA_ALREADY_EXISTS, message="User electronic signature already exists"
        ).build_http_response(status=HTTPStatus.BAD_REQUEST)
        return response

    except ErrorOnEncryptElectronicSignature as ex:
        Gladsheim.error(error=ex, message=ex.msg)
        response = ResponseModel(
            success=False, code=InternalCode.INTERNAL_SERVER_ERROR, message=msg_error
        ).build_http_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
        return response

    except ErrorOnUpdateUser as ex:
        Gladsheim.error(error=ex, message=ex.msg)
        response = ResponseModel(
            success=False, code=InternalCode.INTERNAL_SERVER_ERROR, message=msg_error
        ).build_http_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
        return response

    except ErrorOnSendAuditLog as ex:
        Gladsheim.error(error=ex, message=ex.msg)
        response = ResponseModel(
            success=False, code=InternalCode.INTERNAL_SERVER_ERROR, message=msg_error
        ).build_http_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
        return response

    except ValueError:
        response = ResponseModel(
            success=False, code=InternalCode.INVALID_PARAMS, message="Invalid params"
        ).build_http_response(status=HTTPStatus.BAD_REQUEST)
        return response

    except Exception as ex:
        Gladsheim.error(error=ex)
        response = ResponseModel(
            success=False, code=InternalCode.INTERNAL_SERVER_ERROR, message=msg_error
        ).build_http_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
        return response
