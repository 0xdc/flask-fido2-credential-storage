def test_app_import():
    from cred_storage import create_app
    app = create_app({
        'TESTING': True,
        'DATABASE': 'sqlite:///:memory:'
    })
