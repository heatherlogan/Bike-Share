from users.logic.business import (
    create_document, get_kind, get_player, relate_player_to_document
)
from users.schemas.documents import DocumentSchema

from commons.auth import get_scoped_info

from flask_jwt import jwt_required
from ripozo.decorators import apimethod
from ripozo.resources.resource_base import ResourceBase


class DocumentResource(ResourceBase):
    resource_name = "document"

    @apimethod(methods=['POST'])
    @jwt_required
    def create_document(cls, request):
        document_data = DocumentSchema().load(request.body_args)
        document = create_document(document_data)
        kind = get_kind(get_scoped_info("scopes"))
        player = get_player(kind, get_scoped_info(kind))

        relate_player_to_document(player, document)

        return cls(status_code=200)
