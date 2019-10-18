from datetime import date
from io import StringIO
import unittest
import web_backend.utils.pubmed as pubmed


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


class TestAddPubMedSearchUrls(unittest.TestCase):
    def test_Marfan(self):
        self.maxDiff = None
        d = pubmed.addPubMedSearchUrls(
            ["Marfan Syndrome"], {"Europe": 124},
            date(1919, 2, 13), date(2019, 4, 15))
        self.assertEqual(
            d, {
                "Europe": {
                    "count": 124,
                    "pub_med": 'https://www.ncbi.nlm.nih.gov/pubmed/?term='
                    '%28+Marfan+Syndrome+%5BMH%5D++%29+AND+%28+Europe+%5BMH%5D'
                    '++%29++AND+%281919%2F02%2F13+%5BPDAT%5D+'
                    '%3A+g2019%2F04%2F15+%5BPDAT%5D%29'}})


class TestAutocompleteVocabulary(unittest.TestCase):
    def test_empty_words(self):
        a = pubmed.AutocompleteVocabulary([])
        self.assertEqual(a.autocomplete(""), [])
        self.assertEqual(a.autocomplete("foo"), [])

    def test_one_term(self):
        a = pubmed.AutocompleteVocabulary(['my term'])
        self.assertEqual(a.autocomplete(""), ['my term'])
        self.assertEqual(a.autocomplete("m"), ['my term'])
        self.assertEqual(a.autocomplete("M"), ['my term'])
        self.assertEqual(a.autocomplete("my"), ['my term'])
        self.assertEqual(a.autocomplete("foo"), [])

    def test_two_terms(self):
        a = pubmed.AutocompleteVocabulary(['my term', 'grubs'])
        self.assertEqual(set(a.autocomplete("")), {'my term', 'grubs'})
        self.assertEqual(set(a.autocomplete("m")), {'my term'})
        self.assertEqual(set(a.autocomplete("my")), {'my term'})
        self.assertEqual(set(a.autocomplete("mY")), {'my term'})
        self.assertEqual(set(a.autocomplete("MY")), {'my term'})
        self.assertEqual(set(a.autocomplete("foo")), set())
        self.assertEqual(set(a.autocomplete("g")), {'grubs'})

    def test_twentyfive_terms(self):
        a = pubmed.AutocompleteVocabulary(map(str, range(25)))
        self.assertEqual(
            set(a.autocomplete("")),
            {
                '0', '1', '10', '11', '12', '13', '14', '15', '16', '17',
                '18', '19', '20', '21', '22', '23', '24', '2', '3', '4'
            })
        self.assertEqual(
            set(a.autocomplete("1")),
            {'1', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19',
             '21'})

    def test_exact_match_first(self):
        a = pubmed.AutocompleteVocabulary(map(str, range(1000)))
        self.assertEqual(a.autocomplete("2")[0], "2")
        self.assertEqual(a.autocomplete("5")[0], "5")
        self.assertEqual(a.autocomplete("25")[0], "25")

    def test_loadVocabulary_primary(self):
        a = pubmed.loadVocabulary(pubmed.PRIMARY)
        self.assertEqual(set(a.autocomplete("marfan")), {
            "Marfan Syndrome",
            "Marfans Syndrome",
            "Marfan's Syndrome",
            "Marfan Syndrome, Type I",
            "Marfanil"
        })

    def test_headingsFileTerms_empty(self):
        t = list(pubmed.headingsFileTerms(StringIO("")))
        self.assertEqual(t, [])

    def test_headingsFileTerms_one(self):
        t = list(pubmed.headingsFileTerms(StringIO("123.45\tA term")))
        self.assertEqual(t, ['A term'])

    def test_headingsFileTerms_two(self):
        t = list(pubmed.headingsFileTerms(StringIO(
            "123.45\tA term\n67\tOther")))
        self.assertEqual(t, ['A term', 'Other'])

    def test_synonymsFileTerms_empty(self):
        t = list(pubmed.synonymsFileTerms(StringIO("")))
        self.assertEqual(t, [])

    def test_synonymsFileTerms_one_line_one_syn(self):
        t = list(pubmed.synonymsFileTerms(StringIO("123.45\tA syn")))
        self.assertEqual(t, ['A syn'])

    def test_synonymsFileTerms_one_line_two_syn(self):
        t = list(pubmed.synonymsFileTerms(StringIO(
            "123.45\tA syn\tSecond syn")))
        self.assertEqual(t, ['A syn', 'Second syn'])

    def test_synonymsFileTerms_two_lines_three_syn(self):
        t = list(pubmed.synonymsFileTerms(StringIO(
            "123.45\tA syn\n67\tOther\tfoo")))
        self.assertEqual(t, ['A syn', 'Other', 'foo'])
