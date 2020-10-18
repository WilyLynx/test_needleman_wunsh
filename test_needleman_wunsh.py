import unittest
from needleman_wunsh import make_alignment

MATCH = 2
MISMATCH = -1
GAP = -2


class TestNeedlemanWunsh(unittest.TestCase):
    @staticmethod
    def calculate_score(seq1: str, seq2: str, match: int, mismatch: int, gap: int) -> int:
        """Calculates score of alignment. Helper function used for results validation. """

        def s(a, b):
            """Score of pair"""
            if a == '-' or b == '-':
                return gap
            elif a == b:
                return match
            else:
                return mismatch

        return sum(s(x, y) for x, y in zip(seq1, seq2))

    def check_answer_correctness(self, aligned_seq1, aligned_seq2, score, seq1, seq2):
        dealigned_seq1 = aligned_seq1.replace('-', '')
        dealigned_seq2 = aligned_seq2.replace('-', '')

        self.assertEqual(len(aligned_seq1), len(aligned_seq2), f'aligned sequences must have the same lenghts')
        self.assertEqual(len(seq1), len(dealigned_seq1),
                              f'Length of seq1 does not match length of aligned_seq1: {len(seq1)} !=  {len(dealigned_seq1)}')
        self.assertEqual(len(seq2), len(dealigned_seq2),
                              f'Length of seq1 does not match length of aligned_seq1: {len(seq2)} !=  {len(dealigned_seq2)}')
        self.assertEqual(dealigned_seq1, seq1, f'Output seq1 is different than input seq1')
        self.assertEqual(dealigned_seq2, seq2, f'Output seq2 is different than input seq2')
        for i in range(len(aligned_seq1)):
            self.assertFalse((aligned_seq1[i] == '-' and aligned_seq2[i] == '-'),
                                  f'alignment can not have dash in both sequences at the same position: {i}')
        actual_score = self.calculate_score(aligned_seq1, aligned_seq2, MATCH, MISMATCH, GAP)
        self.assertEqual(actual_score, score, f'Reported score does not match actual score: {score} != {actual_score}')

    def test_empty(self):
        seq = ''
        al_1, al_2, s = make_alignment(seq, seq, MATCH, MISMATCH, GAP)
        self.check_answer_correctness(al_1, al_2, s, seq, seq)
        self.assertEqual(seq, al_1)
        self.assertEqual(seq, al_2)
        self.assertEqual(0, s)

    def test_single_character_match(self):
        seq = 'A'
        al_1, al_2, s = make_alignment(seq, seq, MATCH, MISMATCH, GAP)
        self.check_answer_correctness(al_1, al_2, s, seq, seq)
        self.assertEqual(seq, al_1)
        self.assertEqual(seq, al_2)
        self.assertEqual(MATCH, s)

    def test_single_character_mismatch(self):
        seq1 = 'A'
        seq2 = 'B'
        al_1, al_2, s = make_alignment(seq1, seq2, MATCH, MISMATCH, GAP)
        self.check_answer_correctness(al_1, al_2, s, seq1, seq2)
        self.assertEqual(seq1, al_1)
        self.assertEqual(seq2, al_2)
        self.assertEqual(MISMATCH, s)

    def test_match_gap(self):
        seq1 = 'A'
        seq2 = 'AG'
        al_1, al_2, s = make_alignment(seq1, seq2, MATCH, MISMATCH, GAP)
        self.check_answer_correctness(al_1, al_2, s, seq1, seq2)
        self.assertEqual('A-', al_1)
        self.assertEqual('AG', al_2)
        self.assertEqual(MATCH + GAP, s)

    def test_match_mismatch(self):
        seq1 = 'AT'
        seq2 = 'AG'
        al_1, al_2, s = make_alignment(seq1, seq2, MATCH, MISMATCH, GAP)
        self.check_answer_correctness(al_1, al_2, s, seq1, seq2)
        self.assertEqual(seq1, al_1)
        self.assertEqual(seq2, al_2)
        self.assertEqual(MATCH + MISMATCH, s)

    def test_mismatch_gap(self):
        seq1 = 'T'
        seq2 = 'AG'
        al_1, al_2, s = make_alignment(seq1, seq2, MATCH, MISMATCH, GAP)
        self.check_answer_correctness(al_1, al_2, s, seq1, seq2)
        self.assertEqual(MISMATCH + GAP, s)

    def test_border(self):
        seq1 = 'A'
        seq2 = 'TGGGTA'
        al_1, al_2, s = make_alignment(seq1, seq2, MATCH, MISMATCH, GAP)
        self.check_answer_correctness(al_1, al_2, s, seq1, seq2)
        self.assertEqual('-----A', al_1)
        self.assertEqual(seq2, al_2)
        self.assertEqual(MATCH + 5 * GAP, s)

    def test_border_flip(self):
        seq1 = 'TGGGTA'
        seq2 = 'A'
        al_1, al_2, s = make_alignment(seq1, seq2, MATCH, MISMATCH, GAP)
        self.check_answer_correctness(al_1, al_2, s, seq1, seq2)
        self.assertEqual(seq1, al_1)
        self.assertEqual('-----A', al_2)
        self.assertEqual(MATCH + 5 * GAP, s)

    def test_shifted(self):
        seq1 = 'ATG'
        seq2 = 'GAT'
        al_1, al_2, s = make_alignment(seq1, seq2, MATCH, MISMATCH, GAP)
        self.check_answer_correctness(al_1, al_2, s, seq1, seq2)
        self.assertEqual('-ATG', al_1)
        self.assertEqual('GAT-', al_2)
        self.assertEqual(2 * MATCH + 2 * GAP, s)

    def test_complex_1(self):
        s_1WFN = 'GSSGSSGPQLVRTHEDVPGPVGHLSFSEILDTSLKVSWQEPGEKNGILTGYRISWEEYNRTNTRVTHYLPNVTLEYRVTGLTALTTYTIEVAAMTSKGQGQVSASTISSGVPPSGPSSG'
        s_1WFO = 'GSSGSSGRIGDGSPSHPPILERTLDDVPGPPMGILFPEVRTTSVRLIWQPPAAPNGIILAYQITHRLNTTTANTATVEVLAPSARQYTATGLKPESVYLFRITAQTRKGWGEAAEALVVTTEKRSGPSSG'
        al_1, al_2, s = make_alignment(s_1WFN, s_1WFO, MATCH, MISMATCH, GAP)
        self.check_answer_correctness(al_1, al_2, s, s_1WFN, s_1WFO)
        self.assertEqual(6, s)

    def test_complex_2(self):
        s_1WFN = 'GSSGSSGPQLVRTHEDVPGPVGHLSFSEILDTSLKVSWQEPGEKNGILTGYRISWEEYNRTNTRVTHYLPNVTLEYRVTGLTALTTYTIEVAAMTSKGQGQVSASTISSGVPPSGPSSG'
        s_1WIS = 'GSSGSSGTISSGVPPELPGPPTNLGISNIGPRSVTLQFRPGYDGKTSISRWLVEAQVGVVGEGEEWLLIHQLSNEPDARSMEVPDLNPFTCYSFRMRQVNIVGTSPPSQPSRKIQTLQSGPSSG'
        al_1, al_2, s = make_alignment(s_1WFN, s_1WIS, MATCH, MISMATCH, GAP)
        self.check_answer_correctness(al_1, al_2, s, s_1WFN, s_1WIS)
        self.assertEqual(-27, s)


if __name__ == '__main__':
    unittest.main()
