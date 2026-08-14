import dataclasses


@dataclasses.dataclass(init=True)
class Tools:
    assemble: str
    compile: str
    link: str
    deploy: str
