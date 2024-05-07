from exceptions import BaseHarvestException


class HarvestReportException(BaseHarvestException):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
