"""
    Loads custom Modules into flask in modules folder. Routes use: routes.py
"""
import os
import importlib
from pathlib import Path
from ..functions import get_subdirectories

class LoadModules(object):
    """ Loads folders with routes.py into application """
    routes = []
    app = None

    def __init__(self, app):
        self.app = app
        self.construct_routes()

    def __call__(self):
        """ After init, add urls to flask app """
        routes = self.routes
        for route in routes:
            call = importlib.import_module(route['callback']['module'])
            class_to_call = getattr(call, route['callback']['class'])
            method_to_call = getattr(class_to_call, route['callback']['function'])
            defaults = {}
            if route['middleware'] is not None:
                defaults = {'middleware':route['middleware']}
            self.app.add_url_rule(route['url'], \
                route['name'], method_to_call, methods=route['methods'], defaults=defaults)

    def get_modules(self) -> list:
        """  Get the subdirectories of modules folder """
        directory = os.path.join(Path(__file__).parents[2], 'modules')
        return get_subdirectories(directory)

    def make_route(self, route) -> dict:
        """ Construct a route to be parsed into flask App """
        middleware = route['middleware'] if 'middleware' in route else None
        #Added to ALL requests to support xhr cross-site requests
        route['methods'].append('OPTIONS')
        return {
            'url': route['url'],
            'name': route['name'],
            'methods': route['methods'],
            'middleware': middleware,
            'callback': {
                'module': route['function'].__module__,
                'class': route['function'].__qualname__.rsplit('.', 1)[0],
                'function': route['function'].__name__
            }
        }

    def construct_routes(self):
        """ Gets modules routes.py and converts to module imports """
        modules = self.get_modules()
        for module_name in modules:
            with self.app.app_context():
                module = importlib.import_module('modules.'+module_name+'.routes')
                for route in module.routes:
                    self.routes.append(self.make_route(route))

    def save_routes(self):
        """ NotImplemented """
        #Intended to save as a cache.
        raise NotImplementedError
"""
        temp_dir = tempfile.gettempdir();
        with open(os.path.join(temp_dir, 'routes.txt'),"w") as f:
            f.write(json.dumps(routes));
"""
