from evoting.paillier import *
from typing import List
from hashlib import sha256

class Voting:
    def __init__(self, list_of_candidates: List[str], multi_choice: bool) -> None:
        self.list_of_candidates = list_of_candidates
        self.number_of_candidates = len(list_of_candidates)
        self.multi_choice = multi_choice

        self.encrypted_votes = []
        self.encrypted_votes_sum = [1 for _ in range(self.number_of_candidates)]

        self.r_values = [1 for _ in range(self.number_of_candidates)]

    def generate_keys(self, bits: int) -> None:
        self.private_key, self.public_key = generate_keypair(bits)

    def vote(self, vote: List[int]) -> List[int]:
        # check correctness of parameters      
        if len(vote) != self.number_of_candidates:
            raise ValueError('Incorrect length of the vote')

        for sub_vote in vote:
            if sub_vote != 0 and sub_vote != 1:
                raise ValueError('Incorrect values in the vote')

        vote_sum = 0
        for sub_vote in vote:
            vote_sum += sub_vote

        if vote_sum == 0:
            raise ValueError('No candidates were selected')
        if vote_sum != 1 and not self.multi_choice:
            raise ValueError('Voted for multiple candidates when multi choice is set to False')

        # encrypt vote using public key
        encrypted_vote = []
        
        for index, subvote in enumerate(vote):
            encrypted, r = encrypt(self.public_key, subvote)
            encrypted_vote.append(encrypted)
            self.r_values[index] *= r

        self.encrypted_votes.append(encrypted_vote)
        
        for i in range(self.number_of_candidates):
            self.encrypted_votes_sum[i] = add_encrypted(self.encrypted_votes_sum[i], encrypted_vote[i], self.public_key)
        
        # print(self.hash_vote(encrypted_vote))    
        return encrypted_vote

    def get_results(self) -> List[int]:
        votes_sum = [decrypt(self.private_key, self.public_key, self.encrypted_votes_sum[i]) for i in range(self.number_of_candidates)]
        return votes_sum

    def print_results(self) -> None:
        votes_sum = self.get_results()

        for candidate in self.list_of_candidates:
            print(f'{candidate}: {votes_sum.pop(0)}')

    def export_public_info(self, filename: str):
        with open(filename, 'w', encoding='UTF-8') as file:
            file.write('result = ' + str(self.get_results()) + '\n')
            file.write('r_values = ' + str(self.r_values) + '\n')
            file.write('public_key_n = ' + str(self.public_key.n) + '\n')
            file.write('encrypted_votes = ' + str(self.encrypted_votes) + '\n')
        
    def hash_vote(self, encrypted_vote: List[int]):
        return sha256(str(encrypted_vote).encode()).hexdigest()


if __name__ == '__main__':
    my_voting = Voting(['Kandydat1', 'Kandydat2', 'Kandydat3'], False)

    my_voting.generate_keys(2048)

    my_voting.vote([1, 0, 0])
    my_voting.vote([1, 0, 0])
    my_voting.vote([0, 1, 0])
    my_voting.vote([0, 0, 1])

    my_voting.print_results()


    my_voting.export_public_info('results.py.txt')

