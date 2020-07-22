from unittest import TestCase
from unittest import mock
from server import ImageStatistics
import imagestatistics_pb2


class TestImageStatistics(TestCase):
    def test_AveragePixel(self):
        mock_request = mock.Mock()
        mock_context = mock.Mock()
        ims = ImageStatistics()
        with mock.patch.object(ims, "get_average_rgb", return_value=(1, 2, 3)):
            value = ims.AveragePixel(mock_request, mock_context)
            self.assertEqual(
                value, imagestatistics_pb2.PixelValue(red=1, green=2, blue=3)
            )

    def test_get_average_rgb(self):
        ims = ImageStatistics()
        with mock.patch("server.Image") as mockImageFile:
            mock_image = mockImageFile.open.return_value.__enter__.return_value
            mock_image.size = (3, 1)
            mock_image.getdata.return_value = [(2, 2, 2), (4, 4, 4), (3, 6, 9)]
            mock_file = mock.Mock()
            actual_average = ims.get_average_rgb(mock_file)
            expected_average = (3, 4, 5)

            self.assertEqual(actual_average, expected_average)
            mockImageFile.open.assert_called_once_with(mock_file)
            mock_image.getdata.assert_called_once_with()
