import unittest
from task.spider import RoomStatus


class TestRoomStatus(unittest.TestCase):
    def test_room_status(self):
        self.assertEqual(RoomStatus.room_status(17301508), RoomStatus.selling)
        self.assertEqual(RoomStatus.room_status(524292), RoomStatus.selling)
        self.assertEqual(RoomStatus.room_status(549758435340), RoomStatus.sold)
        self.assertEqual(RoomStatus.room_status(655360), RoomStatus.invalid)
        self.assertEqual(RoomStatus.room_status(524288), RoomStatus.invalid)


if __name__ == "__main__":
    unittest.main()
