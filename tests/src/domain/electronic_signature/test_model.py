from tests.src.services.electronic_signature.stubs import (
    stub_user_electronic_signature_model,
)


def test_when_create_signature_electronic_model_then_is_not_blocked():

    assert stub_user_electronic_signature_model.is_blocked_electronic_signature is False
