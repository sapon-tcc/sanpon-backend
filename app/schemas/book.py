from pydantic import BaseModel
from typing import List

class IndustryIdentifier(BaseModel):
    type: str
    identifier: str

class ReadingModes(BaseModel):
    text: bool
    image: bool

class PanelizationSummary(BaseModel):
    containsEpubBubbles: bool
    containsImageBubbles: bool

class ImageLinks(BaseModel):
    smallThumbnail: str
    thumbnail: str

class VolumeInfo(BaseModel):
    title: str
    authors: List[str]
    publishedDate: str
    description: str
    industryIdentifiers: List[IndustryIdentifier]
    readingModes: ReadingModes
    pageCount: int
    printType: str
    categories: List[str]
    averageRating: float
    ratingsCount: int
    maturityRating: str
    allowAnonLogging: bool
    contentVersion: str
    panelizationSummary: PanelizationSummary
    imageLinks: ImageLinks
    language: str
    previewLink: str
    infoLink: str
    canonicalVolumeLink: str

class SaleInfo(BaseModel):
    country: str
    saleability: str
    isEbook: bool

class AccessInfo(BaseModel):
    country: str
    viewability: str
    embeddable: bool
    publicDomain: bool
    textToSpeechPermission: str
    epub: dict
    pdf: dict
    webReaderLink: str
    accessViewStatus: str
    quoteSharingAllowed: bool

class Item(BaseModel):
    kind: str
    id: str
    etag: str
    selfLink: str
    volumeInfo: VolumeInfo
    saleInfo: SaleInfo
    accessInfo: AccessInfo
    searchInfo: dict

class VolumesResponse(BaseModel):
    kind: str
    totalItems: int
    items: List[Item]
