# Jormungandr - Onboarding
from src.domain.response.model import ResponseModel
from src.domain.enums.code import InternalCode
from src.domain.validator import ElectronicSignature
from src.services.jwt import JwtService
from src.services.electronic_signature import ElectronicSignatureService

# Standards
from http import HTTPStatus

# Third party
from flask import request, Response
from etria_logger import Gladsheim


async def set_electronic_signature() -> Response:
    raw_electronic_signature = request.json
    jwt = request.headers.get("x-thebes-answer")
    msg_error = "Unexpected error occurred"
    try:
        unique_id = await JwtService.decode_jwt_and_get_unique_id(jwt=jwt)
        electronic_signature_validated = ElectronicSignature(**raw_electronic_signature).dict()
        success = await ElectronicSignatureService.set(unique_id=unique_id, electronic_signature=electronic_signature_validated)
        response = ResponseModel(
            success=success,
            code=InternalCode.SUCCESS,
            message="Electronic signature successfully created",
        ).build_http_response(status=HTTPStatus.OK)
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
