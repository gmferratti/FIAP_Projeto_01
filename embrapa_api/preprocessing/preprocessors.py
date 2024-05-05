"""Preprocessor module for the Embrapa API project."""


class BasePreprocessor:
    """Preprocessor class for the Embrapa API project."""

    def __init__(self, data):
        self.data = data

    def preprocess(self):
        """Preprocess the data."""
        return self.data
