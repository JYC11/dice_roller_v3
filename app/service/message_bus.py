import logging
from collections import deque
from typing import Callable, Type

from app.domain.commands import Command
from app.domain.events import Event
from app.service.unit_of_work import AbstractUnitOfWork

logger = logging.getLogger(__name__)

Message = Event | Command


class MessageBus:
    def __init__(
        self,
        uow: AbstractUnitOfWork,
        event_handlers: dict[Type[Event], list[Callable]],
        command_handlers: dict[Type[Command], Callable],
    ):
        self.uow = uow
        self.event_handlers = event_handlers
        self.command_handlers = command_handlers

    def handle(
        self,
        message: Message,
    ):
        queue: deque = deque([message])  # self.queue?
        results: deque = deque()
        while queue:
            message = queue.popleft()
            match message:
                case Event():
                    self.handle_event(message, queue)
                case Command():
                    cmd_result = self.handle_command(message, queue)
                    results.append(cmd_result)
                case _:
                    raise Exception(f"{message} was not an Event or Command")
        return results

    def handle_event(
        self,
        event: Event,
        queue: deque,
    ):
        for handler in self.event_handlers[type(event)]:
            try:
                handler(message=event)
                queue.extend(self.uow.collect_new_events())
            except Exception:
                logger.exception("Failed to handle event ")
                continue

    def handle_command(
        self,
        command: Command,
        queue: deque,
    ):
        logger.debug("handling command %s", command)
        try:
            handler = self.command_handlers[type(command)]
            res = handler(message=command)
            queue.extend(self.uow.collect_new_events())
            return res
        except Exception as e:
            logger.exception("Exception handling command %s", command)
            raise e
