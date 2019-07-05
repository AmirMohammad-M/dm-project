from collections import Counter

import dpkt

class Sequence:
    def __init__(self, items, host_id):
        self.items = items
        self.host_id = host_id

    def __eq__(self, other):
        return self.items == other.items and self.host_id == other.host_id

    def __hash__(self):
      return hash((tuple(self.items), self.host_id))

def is_subsequence(sequence, candidate):
    for k in range(0, len(sequence.items)):
            p = k
            q = 0
            while q < len(candidate.items) and p < len(sequence.items) and sequence.items[p] == candidate.items[q]:
                p += 1
                q += 1
            if q == len(candidate.items):
                return True
    return False


def calculate_support(candidate, sequences):
    unique_host_count = len(list(set([sequence.host_id for sequence in sequences])))

    supported_hosts = set([])

    for sequence in sequences:
        if is_subsequence(sequence, candidate):
            supported_hosts.add(sequence.host_id)

    return len(list(supported_hosts))/unique_host_count

def remove_redundant_subsequent_sets(sequences):
    result = []

    for i in range(0, len(sequences)):
        is_redundant = False
        for j in range(i + 1, len(sequences)):
            if sequences[i].host_id == sequences[j].host_id and is_subsequence(sequences[j], sequences[i]):
                is_redundant = True
                break
        if not is_redundant:
            result.append(sequences[i])
    return result

def extract_candidate(sequences):
    next_length_level_sequences = []
    for sequence_1 in sequences:
        for sequence_2 in sequences:
            if len(sequence_1.items) == 1 and sequence_1.items != sequence_2.items:
                new_subsequence_items = []
                new_subsequence_items.extend(sequence_1.items)
                new_subsequence_items.append(sequence_2.items[len(sequence_2.items) - 1])
                #next_length_level_sequences.append(Sequence(new_subsequence_items, sequence_1.host_id))
                if sequence_1.host_id == sequence_2.host_id:
                    next_length_level_sequences.append(Sequence(new_subsequence_items, sequence_2.host_id))


            if len(sequence_1.items) > 1:
                is_subsequence = True
                for i in range(0, len(sequence_1.items) - 1):
                    is_subsequence = sequence_1.items[i + 1] == sequence_2.items[i] and is_subsequence
                if is_subsequence:
                    new_subsequence_items = []
                    new_subsequence_items.extend(sequence_1.items)
                    new_subsequence_items.append(sequence_2.items[len(sequence_2.items) - 1])
                    #next_length_level_sequences.append(Sequence(new_subsequence_items, sequence_1.host_id))
                    if sequence_1.host_id == sequence_2.host_id:
                        next_length_level_sequences.append(Sequence(new_subsequence_items, sequence_2.host_id))

    return next_length_level_sequences

def extract_subsequence_set(sequence_set, minimum_support):
    length_i_subsequence_sets=[[]]
    for sequence in sequence_set:
        for item in sequence.items:
            length_i_subsequence_sets[0].append(Sequence([item], sequence.host_id))

    length = 2

    while True:
        supported_sequences = []
        for sequence in length_i_subsequence_sets[length - 2]:
            if (calculate_support(sequence, sequence_set) >= minimum_support):
                supported_sequences.append(sequence)
        length_i_subsequence_sets[length - 2] = list(set(supported_sequences))
        length_i_subsequence_sets.append(extract_candidate(length_i_subsequence_sets[length - 2]))
        if len(length_i_subsequence_sets[length - 1]) == 0:
            break

        length += 1

    subsequence_set = []
    for subsequence in length_i_subsequence_sets:
        subsequence_set.extend(subsequence)

    subsequence_set = remove_redundant_subsequent_sets(subsequence_set)

    return subsequence_set


def main():
#    test_case = [Sequence([1, 2, 3], 1), Sequence([0, 1, 2], 1), Sequence([2, 3, 4], 2)]
#    for sequence in extract_candidate(test_case):
#        print(sequence.host_id)
#        print(sequence.items)
#
#    print(calculate_support(Sequence([1, 2, 3, 8], 1), test_case))
#
#    test_case.extend([Sequence([1, 2, 3, 5, 8, 9, 4, 8], 1), Sequence([0, 1, 2, 2, 6, 8], 1), Sequence([2, 3, 4, 5, 8, 9, 4], 1), Sequence([2, 3, 5, 8, 9, 4], 1)])
#    print(calculate_support(Sequence([2, 8], 1), test_case))
#
#
#    for sequence in extract_subsequence_set(test_case, 0.3):
#        print(sequence.host_id)
#        print(sequence.items)
#
#    for ts, pkt in dpkt.pcap.Reader(open(filename,'r')):

    pass


if __name__ == "__main__":
    main()
