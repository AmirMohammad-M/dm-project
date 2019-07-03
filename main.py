from collections import Counter

class Sequence:
    def __init__(self, items, host_id):
        self.items = items
        self.host_id = host_id

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
        length_i_subsequence_sets[length - 2] = supported_sequences
        length_i_subsequence_sets.append(extract_candidate(supported_sequences))
        if len(length_i_subsequence_sets[length - 1]) == 0:
            break
        
        is_redundants = []
        for sequence1 in length_i_subsequence_sets[length - 1]:
            is_redundant = False
            for sequence2 in length_i_subsequence_sets[length - 1]:
                if is_subsequence(sequence2, sequence1):
                    is_redundant = True
                    break
            is_redundants.append(is_redundant)

        final_subsequence_set = []

        for i in range(0, len(is_redundants)):
            if (not is_redundants[i]):
                final_subsequence_set.append(length_i_subsequence_sets[length - 1][i])
        length_i_subsequence_sets[length - 1] = final_subsequence_set
        length += 1

    subsequence_set = []
    for subsequence in length_i_subsequence_sets:
        subsequence_set.extend(subsequence)

    return subsequence_set
        

def main():
    test_case = [Sequence([1, 2, 3], 1), Sequence([0, 1, 2], 1), Sequence([2, 3, 4], 2)]
    for sequence in extract_candidate(test_case):
        print(sequence.host_id)
        print(sequence.items)

    print(calculate_support(Sequence([1, 2, 3, 8], 1), test_case))

    test_case.extend([Sequence([1, 2, 3, 5, 8, 9, 4, 8], 3), Sequence([0, 1, 2, 2, 6, 8], 4), Sequence([2, 3, 4, 5, 8, 9, 4], 6), Sequence([2, 3, 5, 8, 9, 4], 5)])
    print(calculate_support(Sequence([2, 8], 1), test_case))


    for sequence in extract_subsequence_set(test_case, 0.1):
        print(sequence.host_id)
        print(sequence.items)

if __name__ == "__main__":
    main()
