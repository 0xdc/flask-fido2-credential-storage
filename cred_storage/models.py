from sqlalchemy import Column, Integer, Text, JSON

import json

from fido2.utils import bytes2int, int2bytes
from fido2.ctap2 import AttestedCredentialData
from fido2.cose  import CoseKey

from .database import Base

class User(Base):
    __tablename__ = 'users'
    id            = Column(Integer, primary_key=True)
    aaguid        = Column(Integer)
    credential_id = Column(Text, unique=True)
    public_key    = Column(JSON)

    def __init__(self, auth_data):
        # aaguid: probably zeroes, maybe not in FIDO2? 16 bytes
        self.aaguid        = bytes2int( auth_data.credential_data.aaguid )

        # credential_id: too large to store as a BigInteger, so converted to string and stored in a Text field
        # we do lookups on this (see cls.get_by())
        self.credential_id = str(bytes2int( auth_data.credential_data.credential_id ))

        # public_key: AttestedCredentalData, like a dict but:
        #  * has numerical keys that get converted to strings
        #  * bytes cannot be serialised into JSON, so turn them into ints
        self.public_key    = dict({
            **auth_data.credential_data.public_key,
            -2: bytes2int( auth_data.credential_data.public_key.get(-2) ),
            -3: bytes2int( auth_data.credential_data.public_key.get(-3) ),
        })

    def __repr__(self):
        return str(self.credential_id)

    @property
    def create_data(self):
        return AttestedCredentialData.create(
                int2bytes( self.aaguid, 16 ),
                int2bytes( int( self.credential_id ) ),
                self.to_cose,
        )

    @property
    def to_cose(self):
        # TODO: un-hardcode this
        # * convert JSON string key to dict int keys
        # * convert x/y-coordinates from int to bytes (for es256, at least)
        return dict({
            1: self.public_key['1'],
            3: self.public_key['3'],
            -1: self.public_key['-1'],
            -2: int2bytes( self.public_key['-2'] ),
            -3: int2bytes( self.public_key['-3'] ),
        })

    @classmethod
    def get_by(cls, credential_id_bytes):
        return User.query.filter(cls.credential_id == str(bytes2int(credential_id_bytes))).one_or_none()
