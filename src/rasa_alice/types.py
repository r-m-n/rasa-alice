from typing import List, Union

from pydantic import BaseModel, Field, conlist


class ImageButton(BaseModel):
    text: str = None
    url: str = None
    payload: dict = {}


class Image(BaseModel):
    image_id: str
    title: str = None
    description: str = None
    button: ImageButton = {}


class ItemsListHeader(BaseModel):
    text: str


class ItemsListFooter(BaseModel):
    text: str
    button: ImageButton = {}


class BigImage(Image):
    type: str = Field("BigImage", const=True)


class ItemsList(BaseModel):
    type: str = Field("ItemsList", const=True)
    header: ItemsListHeader = {}
    items: conlist(Image, min_items=1, max_items=5)
    footer: ItemsListFooter = {}


class Button(BaseModel):
    title: str
    payload: dict = {}
    url: str = None
    hide: bool = False


class AliceResponse(BaseModel):
    text: str
    tts: str = None
    card: Union[BigImage, ItemsList] = {}
    buttons: List[Button] = []
    end_session: bool = False

    def to_dict(self):
        self.__fields_set__.add("end_session")
        return self.dict(exclude_unset=True)
