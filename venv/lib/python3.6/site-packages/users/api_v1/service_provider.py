from users.logic.business import (
    create_provider, get_user_from_id, relate_user_to_player
)
from users.schemas.service_provider import ServiceProviderSchema

from commons.auth import jwt_scope_any_of, get_request_id

from ripozo.decorators import apimethod
from ripozo.resources.resource_base import ResourceBase


class ProviderResource(ResourceBase):
    resource_name = "provider"

    @apimethod(methods=['POST'])
    @jwt_scope_any_of({"rougue", "admin"})
    def create_provider(cls, request):
        provider_data = ServiceProviderSchema().load(request.body_args)
        provider = create_provider(provider_data)
        user = get_user_from_id(get_request_id())
        relate_user_to_player(user, provider)
        return cls(status_code=200)
