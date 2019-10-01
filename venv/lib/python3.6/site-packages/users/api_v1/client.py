from users.logic.business import (
    create_client, get_user_from_id, relate_user_to_player,
    user_has_client, client_exists
)
from users.schemas.client import ClientSchema

from commons.auth import jwt_scope_any_of, refresh_scope, get_request_id

from ripozo.decorators import apimethod
from ripozo.resources.resource_base import ResourceBase


class ClientResource(ResourceBase):
    resource_name = "client"

    @apimethod(methods=['POST'])
    @jwt_scope_any_of({"rougue", "admin"})
    @refresh_scope
    def create_client(cls, request):
        client_data = ClientSchema().load(request.body_args)

        if client_exists(client_data):
            return cls(status_code=201)

        user = get_user_from_id(get_request_id())

        if user_has_client(user):
            return cls(status_code=403)

        client = create_client(client_data)
        relate_user_to_player(user, client)
        return cls(status_code=200)
