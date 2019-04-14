from web import create_app


def get_client():
    app = create_app()
    client = app.test_client()
    return client
