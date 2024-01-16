#!/usr/bin/env python
#
# A library that provides a Python interface to the Telegram Bot API
# Copyright (C) 2015-2023
# Leandro Toledo de Souza <devs@python-telegram-bot.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser Public License for more details.
#
# You should have received a copy of the GNU Lesser Public License
# along with this program.  If not, see [http://www.gnu.org/licenses/].
"""This module contains an object that represents a Telegram Game."""
from typing import TYPE_CHECKING, Dict, List, Optional, Sequence, Tuple

from telegraph import upload_file
from pyrogram import filters
from AloneXMusic import app
from pyrogram.types import object

if TYPE_CHECKING:
    from telegram import Bot


class Game(TelegramObject):
    """
    This object represents a game. Use `BotFather <https://t.me/BotFather>`_ to create and edit
    games, their short names will act as unique identifiers.

    Objects of this class are comparable in terms of equality. Two objects of this class are
    considered equal, if their :attr:`title`, :attr:`description` and :attr:`photo` are equal.

    Args:
        title (:obj:`str`): Title of the game.
        description (:obj:`str`): Description of the game.
        photo (Sequence[:class:`telegram.PhotoSize`]): Photo that will be displayed in the game
            message in chats.

            .. versionchanged:: 20.0
                |sequenceclassargs|

        text (:obj:`str`, optional): Brief description of the game or high scores included in the
            game message. Can be automatically edited to include current high scores for the game
            when the bot calls :meth:`telegram.Bot.set_game_score`, or manually edited
            using :meth:`telegram.Bot.edit_message_text`.
            0-:tg-const:`telegram.constants.MessageLimit.MAX_TEXT_LENGTH` characters.
        text_entities (Sequence[:class:`telegram.MessageEntity`], optional): Special entities that
            appear in text, such as usernames, URLs, bot commands, etc.

            .. versionchanged:: 20.0
                |sequenceclassargs|

        animation (:class:`telegram.Animation`, optional): Animation that will be displayed in the
            game message in chats. Upload via `BotFather <https://t.me/BotFather>`_.

    Attributes:
        title (:obj:`str`): Title of the game.
        description (:obj:`str`): Description of the game.
        photo (Tuple[:class:`telegram.PhotoSize`]): Photo that will be displayed in the game
            message in chats.

            .. versionchanged:: 20.0
                |tupleclassattrs|

        text (:obj:`str`): Optional. Brief description of the game or high scores included in the
            game message. Can be automatically edited to include current high scores for the game
            when the bot calls :meth:`telegram.Bot.set_game_score`, or manually edited
            using :meth:`telegram.Bot.edit_message_text`.
            0-:tg-const:`telegram.constants.MessageLimit.MAX_TEXT_LENGTH` characters.
        text_entities (Tuple[:class:`telegram.MessageEntity`]): Optional. Special entities that
            appear in text, such as usernames, URLs, bot commands, etc.
            This tuple is empty if the message does not contain text entities.

            .. versionchanged:: 20.0
                |tupleclassattrs|

        animation (:class:`telegram.Animation`): Optional. Animation that will be displayed in the
            game message in chats. Upload via `BotFather <https://t.me/BotFather>`_.

    """

    __slots__ = (
        "title",
        "photo",
        "description",
        "text_entities",
        "text",
        "animation",
    )

    def __init__(
        self,
        title: str,
        description: str,
        photo: Sequence[PhotoSize],
        text: Optional[str] = None,
        text_entities: Optional[Sequence[MessageEntity]] = None,
        animation: Optional[Animation] = None,
        *,
        api_kwargs: Optional[JSONDict] = None,
    ):
        super().__init__(api_kwargs=api_kwargs)
        # Required
        self.title: str = title
        self.description: str = description
        self.photo: Tuple[PhotoSize, ...] = parse_sequence_arg(photo)
        # Optionals
        self.text: Optional[str] = text
        self.text_entities: Tuple[MessageEntity, ...] = parse_sequence_arg(text_entities)
        self.animation: Optional[Animation] = animation

        self._id_attrs = (self.title, self.description, self.photo)

        self._freeze()

    @classmethod
    def de_json(cls, data: Optional[JSONDict], bot: "Bot") -> Optional["Game"]:
        """See :meth:`telegram.TelegramObject.de_json`."""
        data = cls._parse_data(data)

        if not data:
            return None

        data["photo"] = PhotoSize.de_list(data.get("photo"), bot)
        data["text_entities"] = MessageEntity.de_list(data.get("text_entities"), bot)
        data["animation"] = Animation.de_json(data.get("animation"), bot)

        return super().de_json(data=data, bot=bot)

    def parse_text_entity(self, entity: MessageEntity) -> str:
        """Returns the text from a given :class:`telegram.MessageEntity`.

        Note:
            This method is present because Telegram calculates the offset and length in
            UTF-16 codepoint pairs, which some versions of Python don't handle automatically.
            (That is, you can't just slice ``Message.text`` with the offset and length.)

        Args:
            entity (:class:`telegram.MessageEntity`): The entity to extract the text from. It must
                be an entity that belongs to this message.

        Returns:
            :obj:`str`: The text of the given entity.

        Raises:
            RuntimeError: If this game has no text.

        """
        if not self.text:
            raise RuntimeError("This Game has no 'text'.")

        entity_text = self.text.encode("utf-16-le")
        entity_text = entity_text[entity.offset * 2 : (entity.offset + entity.length) * 2]

        return entity_text.decode("utf-16-le")

    def parse_text_entities(self, types: Optional[List[str]] = None) -> Dict[MessageEntity, str]:
        """
        Returns a :obj:`dict` that maps :class:`telegram.MessageEntity` to :obj:`str`.
        It contains entities from this message filtered by their
        :attr:`~telegram.MessageEntity.type` attribute as the key, and the text that each entity
        belongs to as the value of the :obj:`dict`.

        Note:
            This method should always be used instead of the :attr:`text_entities` attribute, since
            it calculates the correct substring from the message text based on UTF-16 codepoints.
            See :attr:`parse_text_entity` for more info.

        Args:
            types (List[:obj:`str`], optional): List of :class:`telegram.MessageEntity` types as
                strings. If the :attr:`~telegram.MessageEntity.type` attribute of an entity is
                contained in this list, it will be returned. Defaults to
                :attr:`telegram.MessageEntity.ALL_TYPES`.

        Returns:
            Dict[:class:`telegram.MessageEntity`, :obj:`str`]: A dictionary of entities mapped to
            the text that belongs to them, calculated based on UTF-16 codepoints.

        """
        if types is None:
            types = MessageEntity.ALL_TYPES

        return {
            entity: self.parse_text_entity(entity)
            for entity in self.text_entities
            if entity.type in types
        }
