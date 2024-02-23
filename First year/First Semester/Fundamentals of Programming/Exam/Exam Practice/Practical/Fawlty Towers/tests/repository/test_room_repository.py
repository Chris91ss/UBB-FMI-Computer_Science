from unittest import TestCase

from src.repository.room_repository import RoomRepository


class TestRoomRepository(TestCase):

    def setUp(self):
        self.room_repository = RoomRepository("repository/room_repository_test.txt")

    def test_get(self):
        assert self.room_repository.get("01") is not None

    def test_get_all(self):
        assert len(self.room_repository.get_all()) == 2
