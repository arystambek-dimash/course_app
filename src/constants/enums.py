import enum


class ContentType(enum.Enum):
    # Image formats
    JPEG = 'image/jpeg'
    PNG = 'image/png'
    GIF = 'image/gif'
    WEBP = 'image/webp'
    SVG = 'image/svg+xml'
    TIFF = 'image/tiff'
    BMP = 'image/bmp'

    # Video formats
    MP4 = 'video/mp4'
    WEBM = 'video/webm'
    OGV = 'video/ogg'
    AVI = 'video/x-msvideo'
    MOV = 'video/quicktime'
    FLV = 'video/x-flv'
    MKV = 'video/x-matroska'

    # Audio formats
    MP3 = 'audio/mpeg'
    WAV = 'audio/wav'
    OGG = 'audio/ogg'
    AAC = 'audio/aac'
    FLAC = 'audio/flac'
    M4A = 'audio/mp4'
    WMA = 'audio/x-ms-wma'

    @classmethod
    def is_image(cls, mime_type: str) -> bool:
        return mime_type.startswith('image/')

    @classmethod
    def is_video(cls, mime_type: str) -> bool:
        return mime_type.startswith('video/')

    @classmethod
    def is_audio(cls, mime_type: str) -> bool:
        return mime_type.startswith('audio/')

    @classmethod
    def get_extension(cls, mime_type: str) -> str:
        try:
            return cls(mime_type).name.lower()
        except ValueError:
            return mime_type.split('/')[-1]


class Status(enum.Enum):
    CREATED = 'created'
    UPDATED = 'updated'
    DELETED = 'deleted'

    @classmethod
    def is_created(cls, status: str) -> bool:
        return cls.CREATED == status

    @classmethod
    def is_updated(cls, status: str) -> bool:
        return cls.UPDATED == status

    @classmethod
    def is_deleted(cls, status: str) -> bool:
        return cls.DELETED == status
