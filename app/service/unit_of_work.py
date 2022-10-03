import abc


class AbstractUnitOfWork(abc.ABC):
    def __enter__(self) -> "AbstractUnitOfWork":
        return (self,)

    @abc.abstractmethod
    def commit(self):
        pass

    @abc.abstractmethod
    def rollback(self):
        pass

    def collect_new_events(self):
        pass
