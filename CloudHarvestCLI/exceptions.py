from CloudHarvestCoreTasks.tasks.base import BaseHarvestException

class HarvestClientException(BaseHarvestException):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
