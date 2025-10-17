import unittest
from datetime import timedelta

from src.main import YouTubeSearchPlugin


class TestYouTubeSearchPlugin(unittest.TestCase):
    def setUp(self):
        self.plugin = YouTubeSearchPlugin()
        # Manually set the API key for testing
        self.plugin.youtube_api_key = "test_api_key"

    def test_parse_duration_iso8601(self):
        """Test ISO 8601 duration parsing"""
        # Test PT1H2M30S (1 hour, 2 minutes, 30 seconds)
        result = self.plugin._parse_duration_iso8601("PT1H2M30S")
        expected = timedelta(hours=1, minutes=2, seconds=30)
        self.assertEqual(result, expected)

        # Test PT5M10S (5 minutes, 10 seconds)
        result = self.plugin._parse_duration_iso8601("PT5M10S")
        expected = timedelta(minutes=5, seconds=10)
        self.assertEqual(result, expected)

        # Test PT45S (45 seconds)
        result = self.plugin._parse_duration_iso8601("PT45S")
        expected = timedelta(seconds=45)
        self.assertEqual(result, expected)

    def test_format_duration(self):
        """Test duration formatting"""
        # Test 1 hour, 2 minutes, 30 seconds
        duration = timedelta(hours=1, minutes=2, seconds=30)
        formatted = self.plugin._format_duration(duration)
        self.assertEqual(formatted, "1:02:30")

        # Test 5 minutes, 10 seconds
        duration = timedelta(minutes=5, seconds=10)
        formatted = self.plugin._format_duration(duration)
        self.assertEqual(formatted, "5:10")

        # Test 45 seconds
        duration = timedelta(seconds=45)
        formatted = self.plugin._format_duration(duration)
        self.assertEqual(formatted, "0:45")

    def test_format_number_human_readable(self):
        """Test number formatting for human readability"""
        # Test thousands
        self.assertEqual(self.plugin._format_number_human_readable(1500), "1.5K")
        self.assertEqual(self.plugin._format_number_human_readable(2500000), "2.5M")
        self.assertEqual(self.plugin._format_number_human_readable(500), "500")
        self.assertEqual(self.plugin._format_number_human_readable(0), "0")

    def test_build_search_params(self):
        """Test search parameter building"""
        params = self.plugin._build_search_params("python tutorial", "video", "relevance", 10)

        self.assertEqual(params["q"], "python tutorial")
        self.assertEqual(params["part"], "snippet")
        self.assertEqual(params["type"], "video")
        self.assertEqual(params["order"], "relevance")
        self.assertEqual(params["maxResults"], "10")
        self.assertEqual(params["key"], "test_api_key")  # Test API key


if __name__ == "__main__":
    unittest.main()
