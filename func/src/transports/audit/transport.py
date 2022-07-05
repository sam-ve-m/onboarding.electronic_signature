# Jormungandr - Onboarding
from ...domain.exceptions import ErrorOnSendAuditLog
from ...domain.enums.types import QueueTypes
from ...domain.complementary_data.model import ComplementaryDataModel

# Third party
from decouple import config
from etria_logger import Gladsheim
from persephone_client import Persephone


class Audit:
    audit_client = Persephone
    partition = QueueTypes.USER_SET_ELECTRONIC_SIGNATURE
    topic = config("PERSEPHONE_TOPIC_USER")
    schema_name = config("PERSEPHONE_SET_ELECTRONIC_SIGNATURE")

    @classmethod
    async def register_log(cls, complementary_data_model: ComplementaryDataModel):
        message = await complementary_data_model.get_audit_template()
        (
            success,
            status_sent_to_persephone
        ) = await cls.audit_client.send_to_persephone(
            topic=cls.topic,
            partition=cls.partition,
            message=message,
            schema_name=cls.schema_name,
        )
        if not success:
            Gladsheim.error(message="Audit::register_user_log::Error on trying to register log")
            raise ErrorOnSendAuditLog

        def get_user_set_electronic_signature_schema_template_with_data(
                payload: dict, unique_id: str
        ) -> dict:
            return {
                "unique_id": unique_id,
                "electronic_signature": payload.get("electronic_signature"),
                "is_blocked_electronic_signature": payload.get(
                    "is_blocked_electronic_signature"
                ),
                "electronic_signature_wrong_attempts": payload.get(
                    "electronic_signature_wrong_attempts"
                ),
            }
