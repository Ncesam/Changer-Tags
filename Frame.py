import enum
from dataclasses import dataclass
from typing import Any


class FrameType(enum.Enum):
    TEXT = "Text Information"
    URL = "URL Link"
    OTHER = "Misc/Other"


class FrameId(str, enum.Enum):
    # Текстовая информация (Категория: TEXT)
    ALBUM_MOVIE_SHOW_TITLE = ("TALB", FrameType.TEXT)
    BPM_BEATS_PER_MINUTE = ("TBPM", FrameType.TEXT)
    COMPOSER = ("TCOM", FrameType.TEXT)
    CONTENT_TYPE = ("TCON", FrameType.TEXT)
    COPYRIGHT_MESSAGE = ("TCOP", FrameType.TEXT)
    DATE = ("TDAT", FrameType.TEXT)
    PLAYLIST_DELAY = ("TDLY", FrameType.TEXT)
    ENCODED_BY = ("TENC", FrameType.TEXT)
    LYRICIST_TEXT_WRITER = ("TEXT", FrameType.TEXT)
    FILE_TYPE = ("TFLT", FrameType.TEXT)
    TIME = ("TIME", FrameType.TEXT)
    CONTENT_GROUP_DESCRIPTION = ("TIT1", FrameType.TEXT)
    TITLE_SONGNAME_CONTENT_DESCRIPTION = ("TIT2", FrameType.TEXT)
    SUBTITLE_DESCRIPTION_REFINEMENT = ("TIT3", FrameType.TEXT)
    INITIAL_KEY = ("TKEY", FrameType.TEXT)
    LANGUAGES = ("TLAN", FrameType.TEXT)
    LENGTH = ("TLEN", FrameType.TEXT)
    MEDIA_TYPE = ("TMED", FrameType.TEXT)
    ORIGINAL_ALBUM_MOVIE_SHOW_TITLE = ("TOAL", FrameType.TEXT)
    ORIGINAL_FILENAME = ("TOFN", FrameType.TEXT)
    ORIGINAL_LYRICIST_TEXT_WRITER = ("TOLY", FrameType.TEXT)
    ORIGINAL_ARTIST_PERFORMER = ("TOPE", FrameType.TEXT)
    ORIGINAL_RELEASE_YEAR = ("TORY", FrameType.TEXT)
    FILE_OWNER_LICENSEE = ("TOWN", FrameType.TEXT)
    LEAD_PERFORMER_SOLOIST = ("TPE1", FrameType.TEXT)
    BAND_ORCHESTRA_ACCOMPANIMENT = ("TPE2", FrameType.TEXT)
    CONDUCTOR_PERFORMER_REFINEMENT = ("TPE3", FrameType.TEXT)
    INTERPRETED_REMIXED_OR_MODIFIED_BY = ("TPE4", FrameType.TEXT)
    PART_OF_A_SET = ("TPOS", FrameType.TEXT)
    PUBLISHER = ("TPUB", FrameType.TEXT)
    TRACK_NUMBER_POSITION_IN_SET = ("TRCK", FrameType.TEXT)
    RECORDING_DATES = ("TRDA", FrameType.TEXT)
    INTERNET_RADIO_STATION_NAME = ("TRSN", FrameType.TEXT)
    INTERNET_RADIO_STATION_OWNER = ("TRSO", FrameType.TEXT)
    SIZE = ("TSIZ", FrameType.TEXT)
    ISRC_INTERNATIONAL_STANDARD_RECORDING_CODE = ("TSRC", FrameType.TEXT)
    SOFTWARE_HARDWARE_SETTINGS_USED_FOR_ENCODING = ("TSSE", FrameType.TEXT)
    YEAR = ("TYER", FrameType.TEXT)
    USER_DEFINED_TEXT_INFORMATION_FRAME = ("TXXX", FrameType.TEXT)

    # URL ссылки (Категория: URL)
    COMMERCIAL_INFORMATION = ("WCOM", FrameType.URL)
    COPYRIGHT_LEGAL_INFORMATION = ("WCOP", FrameType.URL)
    OFFICIAL_AUDIO_FILE_WEBPAGE = ("WOAF", FrameType.URL)
    OFFICIAL_ARTIST_PERFORMER_WEBPAGE = ("WOAR", FrameType.URL)
    OFFICIAL_AUDIO_SOURCE_WEBPAGE = ("WOAS", FrameType.URL)
    OFFICIAL_INTERNET_RADIO_STATION_HOMEPAGE = ("WORS", FrameType.URL)
    PAYMENT = ("WPAY", FrameType.URL)
    PUBLISHERS_OFFICIAL_WEBPAGE = ("WPUB", FrameType.URL)
    USER_DEFINED_URL_LINK_FRAME = ("WXXX", FrameType.URL)

    # Прочие фреймы (Категория: OTHER)
    ATTACHED_PICTURE = ("APIC", FrameType.OTHER)
    COMMENTS = ("COMM", FrameType.OTHER)
    COMMERCIAL_FRAME = ("COMR", FrameType.OTHER)
    ENCRYPTION_METHOD_REGISTRATION = ("ENCR", FrameType.OTHER)
    EQUALIZATION = ("EQUA", FrameType.OTHER)
    EVENT_TIMING_CODES = ("ETCO", FrameType.OTHER)
    GENERAL_ENCAPSULATED_OBJECT = ("GEOB", FrameType.OTHER)
    GROUP_IDENTIFICATION_REGISTRATION = ("GRID", FrameType.OTHER)
    INVOLVED_PEOPLE_LIST = ("IPLS", FrameType.OTHER)
    LINKED_INFORMATION = ("LINK", FrameType.OTHER)
    MUSIC_CD_IDENTIFIER = ("MCDI", FrameType.OTHER)
    MPEG_LOCATION_LOOKUP_TABLE = ("MLLT", FrameType.OTHER)
    OWNERSHIP_FRAME = ("OWNE", FrameType.OTHER)
    PRIVATE_FRAME = ("PRIV", FrameType.OTHER)
    PLAY_COUNTER = ("PCNT", FrameType.OTHER)
    POPULARIMETER = ("POPM", FrameType.OTHER)
    POSITION_SYNCHRONISATION_FRAME = ("POSS", FrameType.OTHER)
    RECOMMENDED_BUFFER_SIZE = ("RBUF", FrameType.OTHER)
    RELATIVE_VOLUME_ADJUSTMENT = ("RVAD", FrameType.OTHER)
    REVERB = ("RVRB", FrameType.OTHER)
    SYNCHRONIZED_LYRIC_TEXT = ("SYLT", FrameType.OTHER)
    SYNCHRONIZED_TEMPO_CODES = ("SYTC", FrameType.OTHER)
    UNIQUE_FILE_IDENTIFIER = ("UFID", FrameType.OTHER)
    TERMS_OF_USE = ("USER", FrameType.OTHER)
    UNSYNCHRONIZED_LYRIC_TEXT_TRANSCRIPTION = ("USLT", FrameType.OTHER)

    def __new__(cls, value, category):
        obj = str.__new__(cls, value)
        obj._value_ = value
        obj.category = category
        return obj

    def __str__(self):
        return self.value

    def __repr__(self):
        return self.value

    @property
    def is_text(self):
        return self.category == FrameType.TEXT

    @classmethod
    def get_by_category(cls, category: FrameType):
        return [f for f in cls if f.category == category]





@dataclass
class Frame:
    id: FrameId
    size: int
    flags: int
    content: Any | None = None