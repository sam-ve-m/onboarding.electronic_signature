# Jormungandr - Onboarding
from src.domain.response.model import ResponseModel
from src.domain.enums.code import InternalCode
from src.domain.validators.validator import ElectronicSignature
from src.domain.exceptions.exceptions import (
    ErrorOnUpdateUser,
    UserUniqueIdNotExists,
    ErrorOnDecodeJwt,
    ErrorOnSendAuditLog,
    UserElectronicSignatureAlreadyExists,
    ErrorOnEncryptElectronicSignature,
    ErrorOnGetUniqueId,
    OnboardingStepsStatusCodeNotOk,
    InvalidOnboardingCurrentStep,
)
from src.services.jwt import JwtService
from src.services.electronic_signature import ElectronicSignatureService

# Standards
from http import HTTPStatus

# Third party
from etria_logger import Gladsheim
import flask


async def set_electronic_signature() -> flask.Response:
    raw_payload = flask.request.json
    jwt = flask.request.headers.get("x-thebes-answer")
    msg_error = "Unexpected error occurred"
    try:
        payload_validated = ElectronicSignature(**raw_payload)
        unique_id = await JwtService.decode_jwt_and_get_unique_id(jwt=jwt)
        await ElectronicSignatureService.validate_current_onboarding_step(jwt=jwt)
        success = await ElectronicSignatureService.set_on_user(
            unique_id=unique_id, payload_validated=payload_validated
        )
        response = ResponseModel(
            success=success,
            code=InternalCode.SUCCESS.value,
            message="Electronic signature successfully created",
        ).build_http_response(status=HTTPStatus.OK)
        return response

    except ErrorOnDecodeJwt as ex:
        Gladsheim.error(error=ex, message=ex.msg)
        response = ResponseModel(
            success=False, code=InternalCode.JWT_INVALID.value, message="Unauthorized token"
        ).build_http_response(status=HTTPStatus.UNAUTHORIZED)
        return response

    except ErrorOnGetUniqueId as ex:
        Gladsheim.error(error=ex, message=ex.msg)
        response = ResponseModel(
            success=False,
            code=InternalCode.JWT_INVALID.value,
            message="Fail to get unique_id",
        ).build_http_response(status=HTTPStatus.UNAUTHORIZED)
        return response

    except OnboardingStepsStatusCodeNotOk as ex:
        Gladsheim.error(error=ex, message=ex.msg)
        response = ResponseModel(
            success=False,
            code=InternalCode.ONBOARDING_STEP_REQUEST_FAILURE.value,
            message=msg_error,
        ).build_http_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
        return response

    except InvalidOnboardingCurrentStep as ex:
        Gladsheim.error(error=ex, message=ex.msg)
        response = ResponseModel(
            success=False,
            code=InternalCode.ONBOARDING_STEP_INCORRECT.value,
            message="User is not in correct step",
        ).build_http_response(status=HTTPStatus.BAD_REQUEST)
        return response

    except UserUniqueIdNotExists as ex:
        Gladsheim.error(error=ex, message=ex.msg)
        response = ResponseModel(
            success=False,
            code=InternalCode.DATA_NOT_FOUND.value,
            message="User unique_id not exists",
        ).build_http_response(status=HTTPStatus.BAD_REQUEST)
        return response

    except UserElectronicSignatureAlreadyExists as ex:
        Gladsheim.error(error=ex, message=ex.msg)
        response = ResponseModel(
            success=False,
            code=InternalCode.DATA_ALREADY_EXISTS.value,
            message="User electronic signature already exists",
        ).build_http_response(status=HTTPStatus.BAD_REQUEST)
        return response

    except ErrorOnEncryptElectronicSignature as ex:
        Gladsheim.error(error=ex, message=ex.msg)
        response = ResponseModel(
            success=False, code=InternalCode.INTERNAL_SERVER_ERROR.value, message=msg_error
        ).build_http_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
        return response

    except ErrorOnUpdateUser as ex:
        Gladsheim.error(error=ex, message=ex.msg)
        response = ResponseModel(
            success=False, code=InternalCode.INTERNAL_SERVER_ERROR.value, message=msg_error
        ).build_http_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
        return response

    except ErrorOnSendAuditLog as ex:
        Gladsheim.error(error=ex, message=ex.msg)
        response = ResponseModel(
            success=False, code=InternalCode.INTERNAL_SERVER_ERROR.value, message=msg_error
        ).build_http_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
        return response

    except ValueError as ex:
        Gladsheim.error(error=ex, message=str(ex))
        response = ResponseModel(
            success=False, code=InternalCode.INVALID_PARAMS.value, message="Invalid params"
        ).build_http_response(status=HTTPStatus.BAD_REQUEST)
        return response

    except Exception as ex:
        Gladsheim.error(error=ex, message=str(ex))
        response = ResponseModel(
            success=False, code=InternalCode.INTERNAL_SERVER_ERROR.value, message=msg_error
        ).build_http_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
        return response
