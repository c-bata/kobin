from typing import Dict, List, Tuple, Any, Callable, Union

WSGIEnviron = Dict[str, Any]


class Request:
    __slots__: List[str]
    environ: WSGIEnviron
    _body: str

    def __init__(self, environ: Dict = ...) -> None: ...
    def get(self, value: str, default: Any = ...): ...
    @property
    def path(self) -> str: ...
    @property
    def method(self) -> str: ...
    @property
    def headers(self) -> Dict[str, str]: ...
    @property
    def query(self) -> Dict[str, str]: ...
    @property
    def forms(self) -> Dict[str, str]: ...
    @property
    def raw_body(self) -> bytes: ...
    @property
    def body(self) -> str: ...
    @property
    def json(self) -> Dict[str, Any]: ...
    @property
    def url(self) -> str: ...
    @property
    def cookies(self) -> Dict[str, str]: ...
    def get_cookie(self, key: str, default: str = ..., secret: Union[str, bytes] = ...) -> str: ...
    def __getitem__(self, key: str): ...
    def __delitem__(self, key: str): ...
    def __setitem__(self, key: str, value: Any): ...
    def __len__(self): ...
    def __repr__(self): ...


def _split_type_and_priority(x: str) -> Tuple[str, float]: ...

def _parse_and_sort_accept_header(accept_header: str) -> List[Tuple[str, float]]: ...

def accept_best_match(accept_header: str, mimetypes: List[str]) -> str: ...

def _local_property() -> Any: ...


class LocalRequest(Request):
    bind: Callable[[Dict], None]
    environ: WSGIEnviron
    _body: str


request: LocalRequest
