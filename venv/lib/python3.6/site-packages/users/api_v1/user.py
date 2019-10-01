from users.logic.business import create_user
from users.schemas.user import UserSchema

from ripozo.decorators import apimethod
from ripozo.resources.resource_base import ResourceBase


class UserResource(ResourceBase):
    resource_name = "user"

    @apimethod(methods=['POST'])
    def create_user(cls, request):
        user_data = UserSchema().load(request.body_args)
        create_user(user_data)
        return cls(status_code=200)
