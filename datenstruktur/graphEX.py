class AddNodeException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class AddEdgeException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class GraphNotBipartiteException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
