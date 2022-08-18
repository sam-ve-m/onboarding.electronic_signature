# Jormungandr - Onboarding
from ...domain.exceptions.exceptions import ErrorOnSendAuditLog
from ...domain.enums.types import QueueTypes
from ...domain.user_electronic_signature.model import UserElectronicSignature

# Third party
from decouple import config
from etria_logger import Gladsheim
from persephone_client import Persephone


class Audit:
    audit_client = Persephone

    @classmethod
    async def record_message_log(cls, electronic_signature_model: UserElectronicSignature) -> bool:
        message = (
            await electronic_signature_model.get_user_electronic_signature_template()
        )
        partition = QueueTypes.USER_SET_ELECTRONIC_SIGNATURE
        topic = config("PERSEPHONE_TOPIC_USER")
        schema_name = config("PERSEPHONE_ELECTRONIC_SIGNATURE_SCHEMA")
        (
            success,
            status_sent_to_persephone,
        ) = await cls.audit_client.send_to_persephone(
            topic=topic,
            partition=partition,
            message=message,
            schema_name=schema_name,
        )
        if not success:
            Gladsheim.error(
                message="Audit::register_user_log::Error on trying to record message log"
            )
            raise ErrorOnSendAuditLog
        return True
