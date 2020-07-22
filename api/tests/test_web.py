from unittest import TestCase
from unittest import mock
from web import PostImagePixelAverage
import imagestatistics_pb2


class TestPostImagePixelAverage(TestCase):
    def test_allowed_file(self):
        with mock.patch("web.config") as mock_config:
            mock_config.ALLOWED_IMAGE_EXTENSIONS = ("a", "b")
            pipa = PostImagePixelAverage()
            self.assertTrue(pipa.allowed_file("/path/to/file.a"))
            self.assertTrue(pipa.allowed_file("/path/to/file.b"))
            self.assertFalse(pipa.allowed_file("/path/to/file.c"))

    def test_storage_filename(self):
        with mock.patch("web.uuid") as mock_uuid, mock.patch(
            "web.config"
        ) as mock_config:
            mock_uuid.uuid3.return_value = "x"
            mock_config.DATA_STORAGE = "/path/to/data"
            mock_filename = mock.Mock()

            pipa = PostImagePixelAverage()
            storage_filename = pipa.storage_filename(mock_filename)
            self.assertEqual(storage_filename, "/path/to/data/x")
            mock_uuid.uuid3.assert_called_once_with(
                mock_uuid.NAMESPACE_URL, mock_filename
            )

    def test_post_image_field_not_populated(self):
        pipa = PostImagePixelAverage()
        with mock.patch("web.request") as mock_request:
            mock_request.files = {"a": 1}
            _, code = pipa.post()
            self.assertEqual(code, 400)

    def test_post_no_selected_file(self):
        pipa = PostImagePixelAverage()
        with mock.patch("web.request") as mock_request:
            mock_request.files = {"image": mock.Mock(filename="")}
            self.assertEqual(pipa.post(), ({"error": "No selected file"}, 400))

    def test_post_empty_file(self):
        pipa = PostImagePixelAverage()
        with mock.patch("web.request") as mock_request:
            mock_request.files = {"image": mock.MagicMock()}
            mock_request.files["image"].__bool__.return_value = False
            self.assertEqual(pipa.post(), ({"error": "Empty file"}, 400))
