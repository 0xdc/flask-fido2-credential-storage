
# Copyright (c) 2018 Yubico AB
# All rights reserved.
#
#   Redistribution and use in source and binary forms, with or
#   without modification, are permitted provided that the following
#   conditions are met:
#
#    1. Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#    2. Redistributions in binary form must reproduce the above
#       copyright notice, this list of conditions and the following
#       disclaimer in the documentation and/or other materials provided
#       with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

"""
Example demo server to use a supported web browser to call the WebAuthn APIs
to register and use a credential.

See the file README.adoc in this directory for details.

Navigate to https://localhost:5000 in a supported web browser.
"""

from fido2.client import ClientData
from fido2.server import Fido2Server, PublicKeyCredentialRpEntity
from fido2.ctap2 import AttestationObject, AuthenticatorData
from fido2 import cbor
from flask import session, request, abort

import os


from . import app
from ..database import db_session
from ..models import User


rp = PublicKeyCredentialRpEntity("localhost", "Demo server")
server = Fido2Server(rp)


@app.route("/api/register/begin", methods=["POST"])
def register_begin():
    registration_data, state = server.register_begin(
        {
            "id": os.urandom(32),
            "name": "",
            "displayName": "",
        },
        [],
        user_verification="discouraged",
    )

    session["state"] = state
    return cbor.encode(registration_data)


@app.route("/api/register/complete", methods=["POST"])
def register_complete():
    try:
        data = cbor.decode(request.get_data())
        client_data = ClientData(data["clientDataJSON"])
        att_obj = AttestationObject(data["attestationObject"])
    except IndexError:
        abort(400)

    auth_data = server.register_complete(session["state"], client_data, att_obj)
    db_session.add(User(auth_data))
    db_session.commit()
    return cbor.encode({"status": "OK"})


@app.route("/api/authenticate/begin", methods=["POST"])
def authenticate_begin():
    if not User.query.count():
        abort(404)

    auth_data, state = server.authenticate_begin(
            [User.query.get(session['User']).create_data] if 'User' in session else [u.create_data for u in User.query.all()]
    )
    session["state"] = state
    return cbor.encode(auth_data)


@app.route("/api/authenticate/complete", methods=["POST"])
def authenticate_complete():
    if not User.query.count():
        abort(404)

    try:
        data = cbor.decode(request.get_data())
        credential_id = data["credentialId"]
        client_data = ClientData(data["clientDataJSON"])
        auth_data = AuthenticatorData(data["authenticatorData"])
        signature = data["signature"]
    except IndexError:
        abort(400)

    try:
        user = User.get_by(credential_id)
        server.authenticate_complete(
            session.pop("state"),
            [user.create_data],
            credential_id,
            client_data,
            auth_data,
            signature,
        )
    except Exception:
        abort(401)

    return cbor.encode({"status": "OK"})
