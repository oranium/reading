import numpy as np
import nltk
#pls fix
signs_end = {';' : ' ', ':': ' ', '!': ' ', '?': ' ', '<': ' ', '>': ' ', '&': ' ', ')': ' ', ']': ' ', '[': ' ', '.': ' ', '"':' '}
signs_beginning = {'(': ' ', '<': ' ', '>': ' ', '"':' ' }

def freq(ngram):
     return words.count(ngram)

def prob(ngram):
    return freq(ngram) * len(ngram) / len(words)

def F1(ngram, i):
    if i == len(ngram)-1:
        return freq(ngram[0]) + freq(ngram[])
    return F1(ngram[:i+1], i+1) + freq(ngram[i+1:])

def F(ngram):
    return 1/(len(ngram)-1) * np.sum(F1(ngram, 0))

def glue(ngram,t='dice'):
    '''
    type scp, dice, theta2
    '''
    if g=='dice':
        return (2 * freq(ngram)) / F(ngram)


def init_data(which='one'):
    with open('corpus2mw/fil_1', 'r') as txt:
        words = txt.read()
        words = words.replace('\n')
        for k,v in signs_end.items():
            words = words.replace(k, v+k)
        for k,v in signs_beginning.items():
            words = words.replace(k, k+v)
        words = words.split(' ')
        return words

words [['a','b','c']
''' words = init_data()
words_ngrams = [words, [words[i:i+2] for i in range(len(words))],
                [words[i:i+3] for i in range(len(words))],[words[i:i+4] for i in range(len(words))],
                [words[i:i+5] for i in range(len(words))],[words[i:i+6] for i in range(len(words))],
                [words[i:i+7] for i in range(len(words))]]
print(words_ngrams)
'''