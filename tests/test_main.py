import logging.config
from http import HTTPStatus
from unittest.mock import patch, MagicMock

import flask
import pytest
from decouple import RepositoryEnv, Config

from src.transports.device_info.transport import DeviceSecurity

with patch.object(RepositoryEnv, "__init__", return_value=None):
    with patch.object(Config, "__init__", return_value=None):
        with patch.object(Config, "__call__"):
            with patch.object(logging.config, "dictConfig"):
                from etria_logger import Gladsheim
                from src.services.jwt import JwtService
                from main import set_electronic_signature
                from src.domain.enums.code import InternalCode
                from src.domain.response.model import ResponseModel
                from src.domain.exceptions.exceptions import (
                    UserUniqueIdNotExists,
                    UserElectronicSignatureAlreadyExists,
                    ErrorOnSendAuditLog,
                    ErrorOnUpdateUser,
                    OnboardingStepsStatusCodeNotOk,
                    InvalidOnboardingCurrentStep,
                    ErrorOnGetUniqueId,
                    ErrorOnEncryptElectronicSignature,
                    ErrorOnDecodeJwt,
                    DeviceInfoRequestFailed,
                    DeviceInfoNotSupplied,
                )
                from src.domain.validators.validator import ElectronicSignature
                from src.services.electronic_signature import ElectronicSignatureService


error_on_update_user_case = (
    ErrorOnUpdateUser(),
    ErrorOnUpdateUser.msg,
    InternalCode.INTERNAL_SERVER_ERROR,
    "Unexpected error occurred",
    HTTPStatus.INTERNAL_SERVER_ERROR,
)
user_unique_id_not_exists_case = (
    UserUniqueIdNotExists(),
    UserUniqueIdNotExists.msg,
    InternalCode.DATA_NOT_FOUND,
    "User unique_id not exists",
    HTTPStatus.BAD_REQUEST,
)
error_on_decode_jwt_case = (
    ErrorOnDecodeJwt(),
    ErrorOnDecodeJwt.msg,
    InternalCode.JWT_INVALID,
    "Unauthorized token",
    HTTPStatus.UNAUTHORIZED,
)
error_on_send_audit_log_case = (
    ErrorOnSendAuditLog(),
    ErrorOnSendAuditLog.msg,
    InternalCode.INTERNAL_SERVER_ERROR,
    "Unexpected error occurred",
    HTTPStatus.INTERNAL_SERVER_ERROR,
)
user_electronic_signature_already_exists_case = (
    UserElectronicSignatureAlreadyExists(),
    UserElectronicSignatureAlreadyExists.msg,
    InternalCode.DATA_ALREADY_EXISTS,
    "User electronic signature already exists",
    HTTPStatus.BAD_REQUEST,
)
error_on_encrypt_electronic_signature_case = (
    ErrorOnEncryptElectronicSignature(),
    ErrorOnEncryptElectronicSignature.msg,
    InternalCode.INTERNAL_SERVER_ERROR,
    "Unexpected error occurred",
    HTTPStatus.INTERNAL_SERVER_ERROR,
)
error_on_get_unique_id_case = (
    ErrorOnGetUniqueId(),
    ErrorOnGetUniqueId.msg,
    InternalCode.JWT_INVALID,
    "Fail to get unique_id",
    HTTPStatus.UNAUTHORIZED,
)
onboarding_steps_status_code_not_ok_case = (
    OnboardingStepsStatusCodeNotOk(),
    OnboardingStepsStatusCodeNotOk.msg,
    InternalCode.ONBOARDING_STEP_REQUEST_FAILURE,
    "Unexpected error occurred",
    HTTPStatus.INTERNAL_SERVER_ERROR,
)
invalid_onboarding_current_step_case = (
    InvalidOnboardingCurrentStep(),
    InvalidOnboardingCurrentStep.msg,
    InternalCode.ONBOARDING_STEP_INCORRECT,
    "User is not in correct step",
    HTTPStatus.BAD_REQUEST,
)
device_info_request_case = (
    DeviceInfoRequestFailed(),
    "Error trying to get device info",
    InternalCode.INTERNAL_SERVER_ERROR,
    "Error trying to get device info",
    HTTPStatus.INTERNAL_SERVER_ERROR,
)
no_device_info_case = (
    DeviceInfoNotSupplied(),
    "Device info not supplied",
    InternalCode.INVALID_PARAMS,
    "Device info not supplied",
    HTTPStatus.BAD_REQUEST,
)

value_exception_case = (
    ValueError("dummy"),
    "dummy",
    InternalCode.INVALID_PARAMS,
    "Invalid params",
    HTTPStatus.BAD_REQUEST,
)
exception_case = (
    Exception("dummy"),
    "dummy",
    InternalCode.INTERNAL_SERVER_ERROR,
    "Unexpected error occurred",
    HTTPStatus.INTERNAL_SERVER_ERROR,
)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "exception,error_message,internal_status_code,response_message,response_status_code",
    [
        error_on_update_user_case,
        user_unique_id_not_exists_case,
        error_on_decode_jwt_case,
        error_on_send_audit_log_case,
        user_electronic_signature_already_exists_case,
        error_on_encrypt_electronic_signature_case,
        error_on_get_unique_id_case,
        onboarding_steps_status_code_not_ok_case,
        invalid_onboarding_current_step_case,
        value_exception_case,
        exception_case,
        device_info_request_case,
        no_device_info_case,
    ],
)
@patch.object(ElectronicSignatureService, "validate_current_onboarding_step")
@patch.object(ElectronicSignatureService, "set_on_user")
@patch.object(Gladsheim, "error")
@patch.object(JwtService, "decode_jwt_and_get_unique_id")
@patch.object(ElectronicSignature, "__init__", return_value=None)
@patch.object(ResponseModel, "__init__", return_value=None)
@patch.object(ResponseModel, "build_http_response")
@patch.object(DeviceSecurity, "get_device_info")
async def test_set_electronic_signature_raising_errors(
    device_info,
    mocked_build_response,
    mocked_response_instance,
    mocked_model,
    mocked_jwt_decode,
    mocked_logger,
    mocked_service,
    mocked_validation,
    monkeypatch,
    exception,
    error_message,
    internal_status_code,
    response_message,
    response_status_code,
):
    monkeypatch.setattr(flask, "request", MagicMock())
    mocked_jwt_decode.side_effect = exception
    await set_electronic_signature()
    mocked_service.assert_not_called()
    mocked_logger.assert_called_once_with(error=exception, message=error_message)
    mocked_response_instance.assert_called_once_with(
        success=False, code=internal_status_code.value, message=response_message
    )
    mocked_build_response.assert_called_once_with(status=response_status_code)


dummy_response = "response"


@pytest.mark.asyncio
@patch.object(ElectronicSignatureService, "validate_current_onboarding_step")
@patch.object(ElectronicSignatureService, "set_on_user", return_value=dummy_response)
@patch.object(Gladsheim, "error")
@patch.object(JwtService, "decode_jwt_and_get_unique_id")
@patch.object(ElectronicSignature, "__init__", return_value=None)
@patch.object(ResponseModel, "__init__", return_value=None)
@patch.object(ResponseModel, "build_http_response", return_value=dummy_response)
@patch.object(DeviceSecurity, "get_device_info")
async def test_set_electronic_signature(
    device_info,
    mocked_build_response,
    mocked_response_instance,
    mocked_model,
    mocked_jwt_decode,
    mocked_logger,
    mocked_service,
    mocked_validation,
    monkeypatch,
):
    monkeypatch.setattr(flask, "request", MagicMock())
    response = await set_electronic_signature()
    mocked_jwt_decode.assert_called()
    mocked_service.assert_called()
    mocked_logger.assert_not_called()
    mocked_response_instance.assert_called_once_with(
        success=dummy_response,
        code=InternalCode.SUCCESS.value,
        message="Electronic signature successfully created",
    )
    mocked_build_response.assert_called_once_with(status=HTTPStatus.OK)
    assert dummy_response == response
