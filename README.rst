=================
rasa-alice
=================

Rasa Connector for Yandex Dialogs.

Installing
------------

.. code-block:: console

    $ pip install rasa-alice

Usage
-----

URL: `/webhooks/alice/webhook`

`credentials.yml`

.. code:: yaml

  rasa_alice.AliceInput:

`domain.yml`

.. code:: yaml

  templates:
    utter_text:
      - text: "Здравствуйте! Это мы, хороводоведы."

    utter_text_custom:
      - custom:
          text: "Здравствуйте! Это мы, хороводоведы."
          tts: "Здравствуйте! Это мы, хоров+одо в+еды."
          end_session: true # false by default

    utter_text_with_buttons:
      - text: 'Hello'
        buttons:
        - title: 'Надпись на кнопке'
          url: 'https://example.com/'
          hide: true

    utter_big_image:
      - custom:
          text: "Здравствуйте! Это мы, хороводоведы."
          card:
            type: "BigImage"
            image_id: "1027858/46r960da47f60207e924"
            title: "Заголовок для изображения"
            description: "Описание изображения."
            button:
              text: "Надпись на кнопке"
              url: "http://example.com/"

    utter_items_list:
      - custom:
          text: "Здравствуйте! Это мы, хороводоведы."
          card:
            type: "ItemsList"
            header:
              text: "Заголовок галереи изображений"
            items:
              - image_id: "<image_id>"
                title: "Заголовок для изображения."
                description: "Описание изображения."
                button:
                  text: "Надпись на кнопке"
                  url: "http://example.com/"

The original request is stored in metadata, you can use it in custom actions:

.. code:: python

  class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_hello_world"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        events = tracker.current_state()['events']
        user_events = []
        for e in events:
            if e['event'] == 'user':
                user_events.append(e)
        original_request = user_events[-1]['metadata']

        payload = original_request['request']['payload']
