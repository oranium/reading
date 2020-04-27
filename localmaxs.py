import numpy as np
import nltk
#pls fix
signs_end = {';' : ' ', ':': ' ', '!': ' ', '?': ' ', '<': ' ', '>': ' ', '&': ' ', ')': ' ', ']': ' ', '[': ' ', '.': ' ', '"':' '}
signs_beginning = {'(': ' ', '<': ' ', '>': ' ', '"':' ' }

# the frequency of the ngram in our corpus
def freq(ngram):
    # so the letters of 1-grams dont get counted individually
    ngram = ngram if type(ngram) is list else [ngram]
    n = len(ngram)
    print(ngram)
    _freq = sum(1 for i in range(N) if words[i:i+n] == ngram )
    print(_freq)
    return sum(1 for i in range(N) if words[i:i+n] == ngram )

# the probability of the ngram in our corpus
def prob(ngram):
    ngram = ngram if type(ngram) is list else [ngram]
    return freq(ngram) * len(ngram) / N


# Needs to be averaged by the caller! (divide by 1/len_ngram -1)
def F_rec(ngram, i=1):
    # shouldnt get larger than length
    if not i >= len(ngram):
        return prob(ngram[:i]) * prob(ngram[i:])
    return prob(ngram[:i]) * prob(ngram[i:]) + F_rec(ngram, i+1)

# F factor for ngrams n>2 from the slides
def F(ngram):
    probs = 0
    for i in range(1,len(ngram)):
        probs += prob(ngram[:i]) * prob(ngram[i:]) 
    return 1/(len(ngram)-1) * probs


# Needs to be averaged by the caller! (divide by 1/len_ngram -1)
def _avq(ngram, i=1):
    # shouldn't get larger than length
    if i >= len(ngram):
        return 1/(i-1) * freq(ngram[:i]) * freq(ngram[i:])
    return freq(ngram[:i]) * freq(ngram[i:]) * _avq(ngram, i+1)


# Needs to be averaged by the caller! (divide by 1/len_ngram -1)
def _avd(ngram, i=1):
    # shouldn't get larger than length
    if i >= len(ngram):
        return freq(ngram[:i]) * freq(ngram[i:]) * (N - freq(ngram[:i])) * (N - freq(ngram[i:]))
    return freq(ngram[:i]) * freq(ngram[i:]) * (N - freq(ngram[:i])) * (N - freq(ngram[i:])) + _avd(ngram, i+1)


def dice(ngram):
    if len(ngram) == 2:
        return 2 * freq(ngram) / (freq(ngram[0]) + freq(ngram[1]))
    return 2 * freq(ngram) / F(ngram)


def scp(ngram):
    if len(ngram) == 2:
        # i imagine the joint probability of those ngrams is if they happen after another????
        # slices so we concatenate the lists and not the strings
        # otherwise we can just substitute it with ngram
        return (prob(ngram[:1] + ngram[1:]) + prob(ngram[1] + ngram[0])) ** 2 / prob(ngram[0]) ** prob(ngram[1])
    return prob(ngram) ** 2 / (1 / (len(ngram) - 1) * F_rec(ngram))

def phi_squared(ngram):
    if len(ngram) == 2:
        # slices so we concatenate the lists and not the strings
        # same as in scp
        dividend = (N * (freq(ngram[:1] + ngram[1:]) + freq(ngram[1] + ngram[0])) - freq(ngram[0]) + freq(ngram[1])) ** 2 
        divisor = freq(ngram[0]) * freq(ngram[1]) * (N - freq(ngram[0])) * (N - freq(ngram[1]))
        return dividend / divisor
    
    avq = 1 / (len(ngram)-1) * _avq(ngram) 
    avd = 1 / (len(ngram)-1) * _avd(ngram)

    return (N * freq(ngram) - avq) ** 2 / avd

def glue(ngram, glue_func):
    '''
    type scp, dice, phi_squared
    glue_func is the function to be passed, not a string or something
    '''
    return glue_func(ngram)


def init_data(which='one'):
    with open('corpus2mw/fil_1', 'r') as txt:
        words = txt.read()
        words = words.replace('\n', '')
        for k,v in signs_end.items():
            words = words.replace(k, v+k)
        for k,v in signs_beginning.items():
            words = words.replace(k, k+v)
        words = words.split(' ')
        return words

words = init_data()
N = len(words)
# i think this is useless
words_ngrams = [words, [words[i:i+2] for i in range(N)],
                [words[i:i+3] for i in range(N)],[words[i:i+4] for i in range(N)],
                [words[i:i+5] for i in range(N)],[words[i:i+6] for i in range(N)],
                [words[i:i+7] for i in range(N)]]

print(glue(words_ngrams[1][2], dice))