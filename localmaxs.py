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
    #print("ngram:",ngram)
    _freq = sum(1 for i in range(N) if words[i:i+n] == ngram )
    #print("freq",_freq)
    return _freq

# the probability of the ngram in our corpus
def prob(ngram):
    ngram = ngram if type(ngram) is list else [ngram]
    return freq(ngram) * len(ngram) / N


# Needs to be averaged by the caller! (divide by 1/len_ngram -1)
def F_rec_dice(ngram, i=1):
    # shouldnt get larger than length
    #print(f'F_rec called for {ngram[:i]}, {ngram[i:]}')
    if i >= len(ngram) - 1:
        #print('calling freq')
        return freq(ngram[:i]) + freq(ngram[i:])
    return freq(ngram[:i]) + freq(ngram[i:]) + F_rec_dice(ngram, i+1)

# Needs to be averaged by the caller! (divide by 1/len_ngram -1)
def F_rec_scp(ngram, i=1):
    # shouldnt get larger than length
    if i >= len(ngram) - 1:
        return prob(ngram[:i]) * prob(ngram[i:])
    return prob(ngram[:i]) * prob(ngram[i:]) + F_rec_scp(ngram, i+1)

# F factor for ngrams n>2 from the slides
def F_dice(ngram):
    freqs = 0
    for i in range(1,len(ngram)):
        print(f'F called for {ngram[:i]}, {ngram[i:]}')
        freqs += freq(ngram[:i]) * freq(ngram[i:]) 
    return 1/(len(ngram)-1) * freqs


# Needs to be averaged by the caller! (divide by 1/len_ngram -1)
def _avq(ngram, i=1):
    # shouldn't get larger than length
    if i >= len(ngram) - 1:
        return freq(ngram[:i]) * freq(ngram[i:])
    return freq(ngram[:i]) * freq(ngram[i:]) + _avq(ngram, i+1)


# Needs to be averaged by the caller! (divide by 1/len_ngram -1)
def _avd(ngram, i=1):
    # shouldn't get larger than length
    if i >= len(ngram) - 1:
        return freq(ngram[:i]) * freq(ngram[i:]) * (N - freq(ngram[:i])) * (N - freq(ngram[i:]))
    return freq(ngram[:i]) * freq(ngram[i:]) * (N - freq(ngram[:i])) * (N - freq(ngram[i:])) + _avd(ngram, i+1)


def dice(ngram):
    if len(ngram) == 2:
        return 2 * freq(ngram) / (freq(ngram[0]) + freq(ngram[1]))
    F_dice = (1 / (len(ngram) - 1)) * F_rec_dice(ngram)
    return 2 * freq(ngram) / F_dice


def scp(ngram):
    if len(ngram) == 2:
        return prob(ngram) ** 2 / prob(ngram[0]) * prob(ngram[1])
    F_scp = (1 / (len(ngram) - 1)) * F_rec_scp(ngram)
    return prob(ngram) ** 2 / F_scp

def phi_squared(ngram):
    if len(ngram) == 2:
        # not sure if there is a precedence error in slides
        dividend = (N * freq(ngram) - (freq(ngram[0]) * freq(ngram[1])) ) ** 2 
        divisor = freq(ngram[0]) * freq(ngram[1]) * (N - freq(ngram[0])) * (N - freq(ngram[1]))
        return dividend / divisor
    
    avq = 1 / (len(ngram)-1) * _avq(ngram) 
    avd = 1 / (len(ngram)-1) * _avd(ngram)

    return ((N * freq(ngram) - avq) ** 2) / avd

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

# for i in range (3):
#     for j in range (3 ):
#         print("Dice",glue(words_ngrams[i][j], dice))
#         print(words_ngrams[i][j])
# we will need a lot of glue for this!
for n in range(3,8):
    print(f'starting {n}-grams')
    for word in words:
        idx = words.index(word)
        glue_scp = glue(words[idx:idx+n], scp) 
        glue_dice = glue(words[idx:idx+n], dice) 
        glue_phi = glue(words[idx:idx+n], phi_squared)
        if idx %100 == 0:
            print(f'scp {glue_scp}\ndice {glue_dice}\nphi {glue_phi}\n')
        if glue_scp > 1 or glue_dice > 1 or 0>glue_phi>1:
            print('That was a mistake') 
            print(f'{words[idx:idx+n]}') 
            print(glue_dice, glue_scp, glue_phi) 
            raise EnvironmentError('Save the climate, save the world')
print('yay')
