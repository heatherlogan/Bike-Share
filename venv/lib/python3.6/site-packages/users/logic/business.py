# encoding: utf-8
""" Business Logic. """
import uuid
from first import first
from users.logic.db import (
    WithSalt, OfPlayer, WithDocument, WithScope
)
from commons.business import fromSchema, filter_all
from commons.auth import hash_pwd
from commons.persistence import (
    get, create, upsert, push,
    has_relation, get_or_create
)


# Util function
def get_if_in(x, y):
    if y in x:
        return y


@fromSchema
def create_user(data):
    user = create("User", email=data['email'])
    salt = create("Salt", salt=str(uuid.uuid4()), algo="md5")
    data['passwd'] = hash_pwd(data['password'], salt['algo'], salt['salt'])

    del data['password']
    upsert(user, uid=uuid.uuid4().hex, **data)

    r = WithSalt(user, salt)

    push(r)

    return user


def get_user_from_id(uid):
    return get("User", "uid", uid)


def get_kind(scopes):
    return first(get_if_in(scopes, i) for i in ["provider", "client"])


def get_player(kind, uid):
    if kind in {"client", "provider"}:
        return get(kind.capitalize(), "uid", uid)


def query_scopes(**kwargs):
    return filter_all("Scope", **kwargs)


@fromSchema
def client_exists(data):
    return get("Client", "name", data["name"]) is not None


def user_has_client(user):
    return has_relation(user, "OF_PLAYER")


def get_or_create_scope(data):
    node = get_or_create("Scope", ("scope", data['name']))
    return node


@fromSchema
def create_client(data):
    node = create(
        "Client",
        uid=uuid.uuid4().hex,
        kind="client",
        **data
    )
    return node


@fromSchema
def create_provider(data):
    node = create(
        "Provider",
        uid=uuid.uuid4().hex,
        kind="provider",
        **data
    )
    return node


@fromSchema
def create_document(data):
    node = create(
        "Document",
        uid=uuid.uuid4().hex,
        **data
    )
    return node


def relate_player_to_document(player, document):
    return push(WithDocument(player, document))


def relate_user_to_player(user, player):
    return push(OfPlayer(user, player))


def add_scope_to_user(user, scope):
    return push(WithScope(user, scope))
