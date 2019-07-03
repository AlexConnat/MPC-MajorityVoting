#!/usr/bin/python3

from mpyc.runtime import mpc
import numpy as np
from collections import Counter
from operator import itemgetter

def pprint(d):
    print("{\n" + "\n".join("    {}: {}".format(k, v) for k, v in d.items()) + "\n}")


NB_CANDIDATES = 10

##### WHERE???? #######
mpc.run(mpc.start())
#######################
print('\n')

secint = mpc.SecInt()
secfxp = mpc.SecFxp()

# Iteratively call mpc.vector_add() to add all votes in the given list
# votes = [ [1,2,3,4,5], [1,1,0,1,1], [10,20,30,40,50] ] --> returns [12,23,33,45,56]
def add_all_votes(votes):

    if len(votes) == 1:
        return votes[0]
    
    v = mpc.vector_add(votes[0], votes[1])

    for i in range(2, len(votes)):
        v = mpc.vector_add(v, votes[i])

    return v

M = len(mpc.parties)

print(M, '- party secure vote counts')
print('You are party', mpc.pid) 
print('-------------------------------------------\n')


# Reading teachers votes from file
with open('vote'+str(mpc.pid)+'.txt', 'r') as f:
    vote = int(f.read()[:-1])

assert (vote >= 0 and vote <= 9)

# Perform one hot-encoded on this vote --> 2 becomes [0, 0, 1, 0, 0, 0, 0, 0, 0, 0]
vote_one_hot = [ 1 if x == vote else 0 for x in range(0,NB_CANDIDATES) ]
sec_vote_one_hot = list(map(secint, vote_one_hot))

senders = list(range(0,M))
inputs_sec_votes = mpc.input(sec_vote_one_hot, senders) # By default, if doesn't specify the second argument, everyone is a sender

sec_total_votes = add_all_votes(inputs_sec_votes)
total_votes = mpc.run(mpc.output(sec_total_votes))
total_votes = list(map(int, total_votes))

# Decode the array total_votes as an json repr
#votes_count = Counter(total_votes)
#print(votes_count)

votes_count = {}
for i, count in enumerate(total_votes):
    votes_count[i] = count

pprint(votes_count)

candidateID, nb_votes = max(votes_count.items(), key=itemgetter(1))
print('\nCandidate Number', candidateID, 'is elected!')

print('\n')
mpc.run(mpc.shutdown())
