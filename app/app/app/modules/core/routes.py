from .controllers import CoreController
from evernode.middleware import SessionMiddleware # noqa

routes = [
    {
        'url': '/test',
        'name': 'core-test',
        'methods': ['GET', 'POST'],
        'function': CoreController.test},
    {
        'url': '/make-user',
        'name': 'core-make-user',
        'methods': ['GET'],
        'function': CoreController.make_user},
    {
        'url': '/login',
        'name': 'core-login',
        'methods': ['POST'],
        'function': CoreController.create_session_jwt},
    {
        'url': '/test_form',
        'name': 'core-test-form',
        'methods': ['GET', 'POST'],
        'function': CoreController.test_form},
    {
        'url': '/generate_key',
        'name': 'core-generate-key',
        'methods': ['GET', 'POST'],
        'function': CoreController.generate_key},
    {
        'url': '/upload',
        'name': 'core-upload',
        'methods': ['POST'],
        'function': CoreController.test_form_upload}]
