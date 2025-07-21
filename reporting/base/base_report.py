from abc import ABC, abstractmethod
from typing import Any, Dict


class AbstractReport(ABC):
    """
    Abstract base class for all reports in the system.
    Defines the standard lifecycle: validate → fetch → format.
    """

    def __init__(self, filters: Dict[str, Any], user=None, output_format="pdf"):
        self.filters = filters
        self.user = user
        self.output_format = output_format
        self.result = None

    def execute(self) -> Any:
        """
        Full lifecycle to run the report:
        - validate input
        - fetch data
        - format into output (PDF, Excel, etc.)
        """
        self.validate()
        self.result = self.fetch()
        return self.format(self.result)

    def validate(self) -> None:
        """
        Default validation logic. Can be overridden by subclasses.
        """
        if not isinstance(self.filters, dict):
            raise ValueError("Filters must be a dictionary.")

    @abstractmethod
    def fetch(self) -> Any:
        """
        Fetch the data. Must be implemented by the subclass.
        """
        pass

    @abstractmethod
    def format(self, data: Any) -> Any:
        """
        Format the result (PDF, Excel...). Must be implemented by the subclass.
        """
        pass
