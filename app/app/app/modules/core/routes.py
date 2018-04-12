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
        'url': '/user-token',
        'name': 'core-user-token',
        'methods': ['POST'],
        'function': CoreController.user_token},
    {
        'url': '/user-check',
        'name': 'core-user-check',
        'methods': ['GET'],
        'middleware': [SessionMiddleware],
        'function': CoreController.user_check},
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
        'function': CoreController.test_form_upload},
    {
        'url': '/test-security',
        'name': 'core-test-security',
        'methods': ['GET'],
        'function': CoreController.test_security},
    {
        'url': '/test-render',
        'name': 'core-test-render',
        'methods': ['GET'],
        'function': CoreController.test_render}]
