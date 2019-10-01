from users.logic.business import (
    get_or_create_scope, get_user_from_id, add_scope_to_user
)
from users.schemas.scope import ScopeSchema

from commons.auth import jwt_scope_all_of

from ripozo.decorators import apimethod
from ripozo.resources.resource_base import ResourceBase


class ScopeResource(ResourceBase):
    resource_name = "scope"

    @apimethod(methods=['POST'])
    @jwt_scope_all_of({'admin'})
    def create_scope(cls, request):
        scope_data, err = ScopeSchema().load(request.body_args).dump()

        if err:
            return cls(properties=err, status_code=400)

        get_or_create_scope(scope_data)
        return cls(status_code=200)

    @apimethod(methods=['GET'])
    @jwt_scope_all_of({'admin'})
    def list_scopes(cls, request):
        scopes = query_scopes(**request.get_query_arg_dict())
        return cls(status_code=200)


    @apimethod(methods=['POST'], route="<user_uid>")
    @jwt_scope_all_of({'admin'})
    def add_scopes(cls, request):
        scope_data, err = ScopeSchema(many=True).load(request.body_args)

        if err:
            return cls(properties=err, status_code=400)

        user = get_user_from_id(request.get("user_uid"))

        [add_scope_to_user(user, get_or_create_scope(scope))
         for scope
         in scope_data]

        return cls(status_code=200)
