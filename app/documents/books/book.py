from beanie import Document
from typing import List, Optional

class Opinion(Document):
    text: Optional[str]
    book_id: Optional[str]
    
    class Settings:
        name = "opinioes"

class IndustryIdentifier(Document):
    type: Optional[str]
    identifier: Optional[str]

    class Settings:
        name = "books"

class ReadingModes(Document):
    text: Optional[bool]
    image: Optional[bool]

    class Settings:
        name = "books"

class PanelizationSummary(Document):
    containsEpubBubbles: Optional[bool]
    containsImageBubbles: Optional[bool]

    class Settings:
        name = "books"

class ImageLinks(Document):
    smallThumbnail: Optional[str]
    thumbnail: Optional[str]

    class Settings:
        name = "books"

class VolumeInfo(Document):
    title: Optional[str]
    authors: Optional[List[Optional[str]]]
    publishedDate: Optional[str]
    description: Optional[str]
    industryIdentifiers: Optional[List[IndustryIdentifier]]
    readingModes: ReadingModes
    pageCount: Optional[int]
    printType: Optional[str]
    categories: Optional[List[Optional[str]]]
    averageRating: Optional[float]
    ratingsCount: Optional[int]
    maturityRating: Optional[str]
    allowAnonLogging: Optional[bool]
    contentVersion: Optional[str]
    panelizationSummary: Optional[PanelizationSummary]
    imageLinks: Optional[ImageLinks]
    language: Optional[str]
    previewLink: Optional[str]
    infoLink: Optional[str]
    canonicalVolumeLink: Optional[str]

    class Settings:
        name = "books"

class SaleInfo(Document):
    country: Optional[str]
    saleability: Optional[str]
    isEbook: Optional[bool]

    class Settings:
        name = "books"

class AccessInfo(Document):
    country: Optional[str]
    viewability: Optional[str]
    embeddable: Optional[bool]
    publicDomain: Optional[bool]
    textToSpeechPermission: Optional[str]
    epub: Optional[dict]
    pdf: Optional[dict]
    webReaderLink: Optional[str]
    accessViewStatus: Optional[str]
    quoteSharingAllowed: Optional[bool]

    class Settings:
        name = "books"

class BookItem(Document):
    isGrated: bool = False
    kind: Optional[str]
    id: Optional[str]
    etag: Optional[str]
    selfLink: Optional[str]
    volumeInfo: Optional[VolumeInfo]
    saleInfo: Optional[SaleInfo]
    accessInfo: Optional[AccessInfo]
    searchInfo: Optional[dict]
    opnions: Optional[List[Opinion]]

    class Settings:
        name = "books"


