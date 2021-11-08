class NotFoundError(Exception):
    def __init__(self, this) -> None:
        self.message = {"error": f"{this} Not found."}


class OnlyThisError(Exception):
    def __init__(self, this) -> None:
        self.message = {"errors": f"Only {this} can be enrolled in the course."}


class BadRequestError(Exception):
    def __init__(self) -> None:
        self.message = {"errors": "Bad request"}
