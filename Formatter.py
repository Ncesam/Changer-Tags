from enum import Enum
from typing import Any

from Frame import FrameId
from ID3Parser import Info

ROW_PADDING = 20


class Formatter:
    class Mode(Enum):
        KeyValue = 0
        Table = 1

    def __init__(self, mode: Formatter.Mode):
        self.mode = mode

    def pretty_print(self, info: Info, padding: int = 1, filename: str = ""):
        if self.mode == Formatter.Mode.KeyValue:
            self._key_value_view_print(info, padding)
        elif self.mode == Formatter.Mode.Table:
            self._table_view_print(info, padding, filename)

    def _print_row(self, key: str, value: Any):
        print(f"{key:<{ROW_PADDING}} | {value}")

    def _key_value_view_print(self, info: Info, padding: int = 1):
        print(f"--- Metadata for ID3v{info.version} ---", end="\n" * padding)
        for frame in info.frames:
            content = "[Image Data]" if frame.id == FrameId.ATTACHED_PICTURE else frame.content
            print(f"{frame.id.name}: {content}")
        print("-" * 30)

    def _table_view_print(self, info: Info, padding: int = 1, filename: str = ""):
        sep = "=" * 60
        print(sep, end="\n" * padding)
        self._print_row("ID3 version", info.version)
        self._print_row("Tag size", f"{info.size / 1024 / 1024:.2f} MB")
        print(sep, end="\n" * padding)

        for frame in info.frames:
            self._print_row("Frame ID", frame.id.value)
            self._print_row("Frame Name", frame.id.name)
            self._print_row("Frame Size", f"{frame.size} Bytes")

            if frame.id == FrameId.ATTACHED_PICTURE:
                img = frame.content
                self._print_row("Mime Type", img.mime_type)
                self._print_row("Pic Type", img.picture_type.name)

                filename = f"{filename.split(".mp3")[0]}_{img.picture_type.name.capitalize()}.jpg"

                with open(filename, "wb") as f:
                    f.write(img.image)
                self._print_row("Saved as", filename)
            else:
                content = str(frame.content)
                display_content = (content[:50] + '...') if len(content) > 50 else content
                self._print_row("Content", display_content)

            print("-" * 60, end="\n" * padding)
