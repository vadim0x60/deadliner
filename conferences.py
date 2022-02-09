import re
from embed import embed
from scrape import find_date, find_site, find_sequences
import numpy as np
from scipy.spatial import distance

DIST_TOL = 0.1
workshop_vector = np.load('examples.npy')

# This should be in itertools
# It's like string.split, but for all types of iterables
def split_by(seq, condition):
    chunk = []
    for elem in seq:
        if condition(elem):
            if chunk:
                yield chunk
            chunk = []
        else:
            chunk.append(elem)
    if chunk:
        yield chunk

def is_too_long_for_name(content):
    if re.match('.*\..*\.', content):
        # Contains several sentences
        return True
    if len(content) > 256:
        # Impossible to display as a one-line title
        return True
    return False

def find_workshops(site):
    best_sequence, best_dist = [], float('inf')

    for protosequence in find_sequences(site):
        for sequence in split_by(protosequence, is_too_long_for_name):
            if len(sequence) > 1:
                dist = distance.cosine(embed(*sequence), workshop_vector)
                if dist < best_dist:
                    best_sequence, best_dist = sequence, dist

    return best_sequence, best_dist

def find_workshop_deadlines(conference):
    site = find_site(conference + ' list of workshops')
    workshops, dist = find_workshops(site)
    if dist < DIST_TOL:
        for workshop in workshops:
            date = find_date(workshop + ' deadline')
            if date:
                yield workshop, date

if __name__ == '__main__':
    try:
        import os
        conference = os.environ['CONFERENCE']
        print(conference)
        print(f'Main track deadline: {find_date(conference + " deadline")}')

        for workshop, deadline in find_workshop_deadlines(conference):
            print(workshop, deadline)
    except Exception as ex:
        import traceback
        tb = traceback.TracebackException.from_exception(ex, capture_locals=True)
        print(''.join(tb.format()))