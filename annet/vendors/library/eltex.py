from annet.annlib.command import Command, CommandList
from annet.annlib.netdev.views.hardware import HardwareView
from annet.vendors.tabparser import EltexFormatter
from annet.vendors.base import AbstractVendor
from annet.vendors.registry import registry


@registry.register
class EltexVendor(AbstractVendor):
    NAME = "eltex"

    def apply(self, hw: HardwareView, do_commit: bool, do_finalize: bool, path: str) -> tuple[CommandList, CommandList]:
        before, after = CommandList(), CommandList()

        before.add_cmd(Command("conf t"))
        after.add_cmd(Command("exit"))
        if do_finalize:
            after.add_cmd(Command("copy running-config startup-config", timeout=30))

        return before, after

    def match(self) -> list[str]:
        return ["Eltex"]

    @property
    def reverse(self) -> str:
        return "no"

    @property
    def hardware(self) -> HardwareView:
        return HardwareView("Eltex")

    def svi_name(self, num: int) -> str:
        return f"Vlan {num}"

    def make_formatter(self, **kwargs) -> EltexFormatter:
        return EltexFormatter(**kwargs)

    @property
    def exit(self) -> str:
        return "exit"
