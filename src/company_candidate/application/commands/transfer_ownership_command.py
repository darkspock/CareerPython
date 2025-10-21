from dataclasses import dataclass

from src.shared.application.command import Command


@dataclass(frozen=True)
class TransferOwnershipCommand(Command):
    """Command to transfer ownership from company to user"""
    id: str
