import dataclasses


@dataclasses.dataclass(init=True)
class Tools:
    assemble: str = None
    compile: str = None
    link: str = None
    deploy: str = None
