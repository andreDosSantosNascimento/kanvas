class NotFoundError(Exception):
    def __init__(self, this) -> None:
        self.message = {"error": f"{this} Not found."}
