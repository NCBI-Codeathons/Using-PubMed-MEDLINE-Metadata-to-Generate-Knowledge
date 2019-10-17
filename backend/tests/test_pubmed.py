import web_backend.utils.pubmed as pubmed
import unittest


class TestCountGroupedIds(unittest.TestCase):
    @staticmethod
    def stub_term_bucket_mapping():
        return {
            "Philadelphia": {"Cities"},
            "Boston": {"Cities"},
            "Finland": {"Europe"},
            "Baltimore": {"Cities"},
            "England": {"Europe"}}

    @staticmethod
    def simple_input():
        # Should give Cities: 2 and Europe: 3
        MID = pubmed.MeshAndId
        return (
            [
                MID(1, ["Philadelphia"]),
                MID(2, ["Georgia"]),
                MID(3, ["Boston", "Finland"]),
                MID(3, ["England", "Finland"]),
                MID(3, ["England", "Europe"]),
                MID(3, ["Europe"]),
            ])

    def test_CountGroupedIdsForSimpleInput(self):
        actual = pubmed.countGroupedIds(
            TestCountGroupedIds.stub_term_bucket_mapping(),
            TestCountGroupedIds.simple_input())
        self.assertEqual(actual, {'Cities': 2, 'Europe': 3})
