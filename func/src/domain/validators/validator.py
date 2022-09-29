# Third party
from pydantic import BaseModel, constr

signature_regex = r"^(?=.*?[a-z])(?=.*?[A-Z])(?=.*?[0-9])[a-zA-Z0-9!\"#$%&'\(\)\*\+,-\.\/:;<=>?@\[\\\]_\{\}]{8,}$"


class ElectronicSignature(BaseModel):
    electronic_signature: constr(regex=signature_regex)
