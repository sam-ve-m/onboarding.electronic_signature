from strenum import StrEnum


class UserLevel(StrEnum):
    CLIENT = "client"


class UserOnboardingStep(StrEnum):
    ELECTRONIC_SIGNATURE = "electronic_signature"
