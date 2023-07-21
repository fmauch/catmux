class InvalidConfig(Exception):
    """A given catmux config is not valid."""

    def __init__(self, message):
        self.message = message
        super().__init__("Illegal catmux config: " + self.message)
