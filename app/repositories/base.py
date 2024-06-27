from abc import ABC, abstractmethod


class AbstractRepository(ABC):

    @abstractmethod
    async def create(self, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def delete(self, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def get_single_record(self, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def get_multi_records(self, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def commit(self, *args):
        raise NotImplementedError
