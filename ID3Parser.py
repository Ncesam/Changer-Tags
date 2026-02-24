import enum
import logging
import struct
from dataclasses import dataclass
from typing import BinaryIO, List, Any

from Frame import Frame, FrameId


class ID3Parser:

    @staticmethod
    def parse(file: BinaryIO) -> Info:
        version = ID3Parser.get_version(file)
        flags = ID3Parser.get_flags(file)
        size = ID3Parser.get_size(file)
        end_file_tags = file.tell() + size
        frames = []

        while file.tell() < end_file_tags:
            if ID3Parser._check_padding(file): break

            try:
                frame = ID3Parser.get_frame(file)
                frames.append(frame)
            except Exception as e:
                raise e
                break

        return Info(version, flags, size, frames)

    @staticmethod
    def _check_padding(file: BinaryIO) -> bool:
        data = file.read(4)
        if not data or data == b"\x00\x00\x00\x00" or data[0] == 0xff:
            return True
        file.seek(-4, 1)
        return False

    @staticmethod
    def get_version(file: BinaryIO) -> str:
        try:
            logging.debug("Try get version metadata")
            data = file.read(5)
            if data[:3] == b"ID3":
                version = struct.unpack(">H", data[3:5])[0]
                formatted_version = version >> 8
                return f"v2.{formatted_version}.0"
            else:
                raise Exception(f"File are not support ID3")
        except struct.error as e:
            raise e
        except Exception as e:
            raise e

    @staticmethod
    def get_flags(file: BinaryIO) -> List[Flag]:
        data = file.read(1)[0]
        flags = []
        if data >> 7 & 1:
            flags.append(Flag.Unsynchronisation)
        if data >> 6 & 1:
            flags.append(Flag.Extended_Header)
        if data >> 5 & 1:
            flags.append(Flag.Experimental_Indicator)
        return flags

    @staticmethod
    def get_size(file: BinaryIO) -> int:
        """
        Get size from tags
        :param file:
        :return: size in bytes
        """
        data = file.read(4)
        size = struct.unpack(">I", data)[0]
        return size

    @staticmethod
    def get_frame(file: BinaryIO) -> Frame:
        data = file.read(10)
        tag = FrameId(struct.unpack(">4s", data[:4])[0].decode())
        size = struct.unpack(">I", data[4:8])[0]
        flags = struct.unpack(">BB", data[8:10])
        content = None
        match tag:
            case tag if tag.is_text:
                content = ID3Parser.get_text_frame(file, size)
            case FrameId.ATTACHED_PICTURE:
                content = ID3Parser.get_image_frame(file, size)
            case FrameId.COMMENTS:
                content = ID3Parser.get_comment_frame(file, size)
        return Frame(tag, size, flags[0], content=content)

    @staticmethod
    def get_text_frame(file: BinaryIO, size: int) -> str:
        data = file.read(size)
        encoding_id = data[0]
        text = data[1:].decode(ENCODING_MAPPING[encoding_id], "replace")
        return text

    @staticmethod
    def get_image_frame(file: BinaryIO, size: int) -> Image:
        data = file.read(size)
        encoding_id = data[0]
        encoding_type = ENCODING_MAPPING[encoding_id]

        mime_end = data[1:].find(b"\x00") + 1
        mime_type = data[1:mime_end].decode("ascii")

        picture_type_index = mime_end + 1
        picture_type = PictureType(data[picture_type_index])

        desc_start = picture_type_index + 1

        # UTF-16 has EOF like \x00\x00
        if encoding_id in (1, 2):
            desc_end = data.find(b'\x00\x00', desc_start)
            if desc_end == -1:
                desc_end = desc_start
            else:
                desc_end += 2
        else:
            desc_end = data.find(b'\x00', desc_start)
            if desc_end == -1:
                desc_end = desc_start
            else:
                desc_end += 1

        description = data[desc_start:desc_end].decode(encoding_type, errors='replace').strip('\x00')

        image_data = data[desc_end:]

        return Image(encoding_type, mime_type, picture_type, description, image_data)

    @staticmethod
    def get_comment_frame(file: BinaryIO, size: int) -> Comment:
        data = file.read(size)
        encoding_id = data[0]
        encoding_type = ENCODING_MAPPING[encoding_id]

        language = data[1:4].decode("ascii")

        content_data = data[4:]
        separator = b'\x00\x00' if encoding_id in (1, 2) else b'\x00'
        sep_pos = content_data.find(separator)

        if sep_pos == -1:
            short_descr = ""
            description = content_data.decode(encoding_type, errors='replace').strip('\x00')
        else:
            short_descr_bytes = content_data[:sep_pos]
            description_bytes = content_data[sep_pos + len(separator):]

            short_descr = short_descr_bytes.decode(encoding_type, errors='replace').strip('\x00')
            description = description_bytes.decode(encoding_type, errors='replace').strip('\x00')

        return Comment(encoding_type, language, short_descr, description)


ENCODING_MAPPING = {
    0: "iso-8859-1",
    1: "utf-16",
    2: "utf-16-be",
    3: "utf-8",
}


@dataclass
class Info:
    version: str
    flags: List[Flag]
    size: int
    frames: List[Frame]


@dataclass
class Image:
    text_encoding: str
    mime_type: str
    picture_type: PictureType
    description: str
    image: Any


@dataclass
class Comment:
    text_encoding: str
    language: str
    short_description: str
    description: str


class Flag(enum.Enum):
    Unsynchronisation: int
    Extended_Header: int
    Experimental_Indicator: int


class PictureType(enum.IntEnum):
    OTHER = 0
    FILE_ICON = 1
    OTHER_FILE_ICON = 2
    FRONT_COVER = 3
    BACK_COVER = 4
    LEAFLET_PAGE = 5
    MEDIA = 6
    LEAD_ARTIST = 7
    ARTIST = 8
    CONDUCTOR = 9
    BAND = 10
    COMPOSER = 11
    LYRICIST = 12
    RECORDING_LOCATION = 13
    DURING_RECORDING = 14
    DURING_PERFORMANCE = 15
    MOVIE_SCREEN_CAPTURE = 16
    A_BRIGHT_COLOURED_FISH = 17
    ILLUSTRATION = 18
    BAND_LOGOTYPE = 19
    PUBLISHER_LOGOTYPE = 20

    def __str__(self):
        return self.name
