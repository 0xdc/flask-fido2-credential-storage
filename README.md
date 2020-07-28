Credential Storage
==================

Storing FIDO2 public keys in a Flask-SQLalchemy app

Quickstart
----------

```bash
$ pip install .
$ python -mcred_storage
```

Then go to https://localhost:5000/

Support
-------

| | FIDO U2F (CTAP1) | FIDO2 (CTAP2) |
|---|-----|--------------|
| Chrome Linux | X | X |
| Firefox Linux | X | |

License
-------

* MIT.
* Uses MIT code published by Yubico AB in some flask and frontend (html5, css, javascript) code.
* Uses MIT code published by Patrick Gansterer in cbor.js library.
