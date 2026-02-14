"""Tests for database layer."""
import pytest

from chat_app.models import Chat, Message


def test_create_and_query_chat(test_session):
    """Can create a Chat and retrieve it."""
    chat = Chat(title="Test Chat")
    test_session.add(chat)
    test_session.commit()
    test_session.refresh(chat)

    found = test_session.query(Chat).filter(Chat.id == chat.id).first()
    assert found is not None
    assert found.title == "Test Chat"


def test_chat_message_relationship(test_session):
    """Chat and Message are properly related."""
    chat = Chat(title="Chat with messages")
    test_session.add(chat)
    test_session.commit()
    test_session.refresh(chat)

    msg = Message(chat_id=chat.id, content="Hello")
    test_session.add(msg)
    test_session.commit()

    found_chat = test_session.query(Chat).filter(Chat.id == chat.id).first()
    assert len(found_chat.messages) == 1
    assert found_chat.messages[0].content == "Hello"
