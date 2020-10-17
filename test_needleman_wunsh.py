import unittest
from needleman_wunsh import make_alignment

MATCH = 2
MISMATCH = -1
GAP = -2


class TestNeedlemanWunsh(unittest.TestCase):

    def test_empty(self):
        al_1, al_2, s = make_alignment('', '', MATCH, MISMATCH, GAP)
        self.assertEqual('', al_1)
        self.assertEqual('', al_2)
        self.assertEqual(0, s)

    def test_single_character_match(self):
        c = 'A'
        al_1, al_2, s = make_alignment(c, c, MATCH, MISMATCH, GAP)
        self.assertEqual(c, al_1)
        self.assertEqual(c, al_2)
        self.assertEqual(MATCH, s)

    def test_single_character_mismatch(self):
        s1 = 'A'
        s2 = 'B'
        al_1, al_2, s = make_alignment(s1, s2, MATCH, MISMATCH, GAP)
        self.assertEqual(s1, al_1)
        self.assertEqual(s2, al_2)
        self.assertEqual(MISMATCH, s)

    def test_match_gap(self):
        al_1, al_2, s = make_alignment('A', 'AG', MATCH, MISMATCH, GAP)
        self.assertEqual('A-', al_1)
        self.assertEqual('AG', al_2)
        self.assertEqual(MATCH + GAP, s)

    def test_match_mismatch(self):
        s1 = 'AT'
        s2 = 'AG'
        al_1, al_2, s = make_alignment(s1, s2, MATCH, MISMATCH, GAP)
        self.assertEqual(s1, al_1)
        self.assertEqual(s2, al_2)
        self.assertEqual(MATCH + MISMATCH, s)

    def test_mismatch_gap(self):
        al_1, al_2, s = make_alignment('T', 'AG', MATCH, MISMATCH, GAP)
        self.assertEqual(MISMATCH + GAP, s)

    def test_complex_1(self):
        s_1WFN = 'GSSGSSGPQLVRTHEDVPGPVGHLSFSEILDTSLKVSWQEPGEKNGILTGYRISWEEYNRTNTRVTHYLPNVTLEYRVTGLTALTTYTIEVAAMTSKGQGQVSASTISSGVPPSGPSSG'
        s_1WFO = 'GSSGSSGRIGDGSPSHPPILERTLDDVPGPPMGILFPEVRTTSVRLIWQPPAAPNGIILAYQITHRLNTTTANTATVEVLAPSARQYTATGLKPESVYLFRITAQTRKGWGEAAEALVVTTEKRSGPSSG'
        al_1, al_2, s = make_alignment(s_1WFN, s_1WFO, MATCH, MISMATCH, GAP)
        self.assertEqual(6, s)

    def test_complex_2(self):
        s_1WFN = 'GSSGSSGPQLVRTHEDVPGPVGHLSFSEILDTSLKVSWQEPGEKNGILTGYRISWEEYNRTNTRVTHYLPNVTLEYRVTGLTALTTYTIEVAAMTSKGQGQVSASTISSGVPPSGPSSG'
        s_1WIS = 'GSSGSSGTISSGVPPELPGPPTNLGISNIGPRSVTLQFRPGYDGKTSISRWLVEAQVGVVGEGEEWLLIHQLSNEPDARSMEVPDLNPFTCYSFRMRQVNIVGTSPPSQPSRKIQTLQSGPSSG'
        al_1, al_2, s = make_alignment(s_1WFN, s_1WIS, MATCH, MISMATCH, GAP)
        self.assertEqual(-27, s)


if __name__ == '__main__':
    unittest.main()
