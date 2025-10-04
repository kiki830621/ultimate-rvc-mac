from types import ModuleType

def load(
    fullname: str,
    *,
    require: str | None = None,
    error_on_import: bool = False,
) -> ModuleType: ...
