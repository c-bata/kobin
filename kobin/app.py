import os
import types
from typing import Any, Callable, Dict, List, Union, Tuple
from .static_files import static_file
from .routes import Router, Route
from .environs import request, response


class Kobin:
    def __init__(self, static_url_path: str= 'static') -> None:
        self.router = Router()
        self.config = Config()
        route = Route('^/{}/(?P<filename>.*)'.format(static_url_path), 'GET', static_file)
        self.add_route(route)

    def run(self, host: str='127.0.0.1', port: int=8000, server: str='wsgiref', **kwargs) -> None:
        from .server_adapters import ServerAdapter, servers
        try:
            if server not in servers:
                raise ImportError('{server} is not supported.'.format(server))
            server_cls = servers.get(server)
            server_obj = server_cls(host=host, port=port, **kwargs)  # type: ServerAdapter

            print('Serving on port %d...' % port)
            server_obj.run(self)
        except KeyboardInterrupt:
            print('Goodbye.')

    def add_route(self, route: Route) -> None:
        self.router.add(route.rule, route.method, route)

    def route(self, path: str=None, method: str='GET',
              callback: Callable[..., Union[str, bytes]]=None) -> Callable[..., Union[str, bytes]]:
        def decorator(callback_func):
            route = Route(path, method, callback_func)
            self.add_route(route)
            return callback_func
        return decorator(callback) if callback else decorator

    def _handle(self, environ: Dict) -> Union[str, bytes]:
        route, kwargs = self.router.match(environ)
        environ['kobin.app'] = self
        request.bind(environ)  # type: ignore
        response.bind()        # type: ignore
        return route.call(**kwargs) if kwargs else route.call()

    def wsgi(self, environ: Dict,
             start_response: Callable[[bytes, List[Tuple[str, str]]], None]) -> List[bytes]:
        out = self._handle(environ)
        if isinstance(out, str):
            out = out.encode('utf-8')
        start_response(response.status, response.headerlist)
        return [out]

    def __call__(self, environ: Dict, start_response) -> List[bytes]:
        """It is called when receive http request."""
        return self.wsgi(environ, start_response)


class Config(dict):
    def load_from_pyfile(self, root_path: str, file_name: str) -> None:
        t = types.ModuleType('config')
        file_path = os.path.join(root_path, file_name)
        with open(file_path) as config_file:
            exec(compile(config_file.read(), file_path, 'exec'), t.__dict__)
            configs = {key: getattr(t, key) for key in dir(t) if key.isupper()}
            self.update(configs)
