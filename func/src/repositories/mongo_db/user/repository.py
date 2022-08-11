# Jormungandr - Onboarding
from ..base_repository.base import MongoDbBaseRepository

# Third party
from decouple import config
from etria_logger import Gladsheim


class UserRepository(MongoDbBaseRepository):

    @classmethod
    async def find_one_by_unique_id(cls, unique_id: str) -> dict:
        collection = await cls._get_collection()
        try:
            user = await collection.find_one({"unique_id": unique_id})
            return user
        except Exception as ex:
            message = f'UserRepository::find_one_user::with this query::"unique_id":{unique_id}'
            Gladsheim.error(error=ex, message=message)
            raise ex

    @classmethod
    async def update_one_with_electronic_signature(
        cls, unique_id: str, user_electronic_signature
    ):
        collection = await cls._get_collection()
        try:
            user_updated = await collection.update_one(
                {"unique_id": unique_id}, {"$set": user_electronic_signature}
            )
            return user_updated
        except Exception as ex:
            message = (
                f'UserRepository::update_one_with_user_complementary_data::error on update complementary data":'
                f"{user_electronic_signature}"
            )
            Gladsheim.error(error=ex, message=message)
            raise ex
