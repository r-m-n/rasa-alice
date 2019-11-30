from typing import Text, Any, Callable, Awaitable, List, Dict, Iterable

from rasa.core.channels.channel import (
    UserMessage, InputChannel, CollectingOutputChannel
)
from rasa.core import utils
from sanic import Blueprint, response
from sanic.request import Request
from sanic.response import HTTPResponse

from .types import AliceResponse


class AliceOutput(CollectingOutputChannel):
    @classmethod
    def name(cls) -> Text:
        return "alice"

    async def send_response(
        self, recipient_id: Text, message: Dict[Text, Any]
    ) -> None:
        message = utils.remove_none_values(message)
        await super().send_response(recipient_id, message)

    async def send_text_message(
        self, recipient_id: Text, text: Text, **kwargs: Any
    ) -> None:
        message = AliceResponse(text=text, **kwargs)
        await self._persist_message(message)

    async def send_text_with_buttons(
        self,
        recipient_id: Text,
        text: Text,
        buttons: List[Dict[Text, Any]],
        **kwargs: Any,
    ) -> None:
        message = AliceResponse(
            text=text,
            buttons=buttons,
            **kwargs
        )
        await self._persist_message(message)

    async def send_custom_json(
        self, recipient_id: Text, json_message: Dict[Text, Any], **kwargs: Any
    ) -> None:
        message = AliceResponse(**json_message)
        await self._persist_message(message)

    async def send_image_url(
        self, recipient_id: Text, image: Text, **kwargs: Any
    ) -> None:
        raise NotImplementedError

    async def send_attachment(
        self, recipient_id: Text, attachment: Text, **kwargs: Any
    ) -> None:
        raise NotImplementedError

    async def send_elements(
        self, recipient_id: Text, elements: Iterable[Dict[Text, Any]],
        **kwargs: Any
    ) -> None:
        raise NotImplementedError


class AliceInput(InputChannel):
    @classmethod
    def name(cls) -> Text:
        return "alice"

    def blueprint(
        self, on_new_message: Callable[[UserMessage], Awaitable[Any]]
    ) -> Blueprint:

        alice_webhook = Blueprint("alice_webhook", __name__)

        @alice_webhook.route("/", methods=["GET"])
        async def health(request: Request) -> HTTPResponse:
            return response.json({"status": "ok"})

        @alice_webhook.route("/webhook", methods=["POST"])
        async def receive(request: Request) -> HTTPResponse:
            data = request.json
            session = data["session"]
            version = data["version"]
            alice_request = data["request"]

            out_channel = AliceOutput()

            user_msg = UserMessage(
                text=alice_request["command"],
                output_channel=out_channel,
                sender_id=session["user_id"],
                input_channel=self.name(),
                metadata=data,
            )

            await on_new_message(user_msg)

            alice_response = out_channel.latest_output()
            alice_response_dict = {}
            if alice_response:
                alice_response_dict = alice_response.to_dict()

            return response.json({
                "response": alice_response_dict,
                "session": session,
                "version": version
            })

        return alice_webhook
