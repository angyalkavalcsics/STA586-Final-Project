from gensim.test.utils import common_texts, get_tmpfile
from gensim.models import Word2Vec
import gensim
import numpy as np
# pip install -U gensim

sentences = [["I", "love", "rain"], 
             ["rain", "rain", "go", "away"],
             ["I", "am", "away"],
             ["It", "is", "raining", "in", "Portland"],
             ["Tomorrow", "there", "is", "rain", "in", "the", "forecast"],
             ["When", "I", "am", "away", "I", "will", "leave", "my", "umbrella", "at", "home"]]
sentLen = len(sentences)
# Flatten sentence list
flat_sent = [y for x in sentences for y in x]
flat_sentLen = len(flat_sent)
# Create dictionary of unique words.
dictionary = np.unique(flat_sent)
dictLen = len(dictionary)
# Parse the sentences. For each word in the sentence,
# add a 1 in the place of the word in the dictionary.

newSent = []
for i in range(sentLen): 
    z = np.zeros(dictLen)
    for k in range(len(sentences[i])):
        for j in range(dictLen):
            if sentences[i][k] == dictionary[j]:
                z[j] += 1
                break
    newSent.append(z)

# Returns all unique words which appear at least 1 times
#vocabulary = word2vec.wv.vocab 
'''
v1 contains the vector representation for the word 'rain'
By default, this is a 100 dim vector
'''

'''
sentences := our corpus
window := how many words around the word will be considered for context
CBOW_mean = 1 for CBOW, 0 else
sg := 1 for skip-gram, otherwise cbow
hs := 1 if hierarchical softmax will be used for training
negative := if >0 then negative sampling is used 
typically between 5-20 for how many noise words should be drawn
ns_exponent := default of 0.75 has proven to be superior in research
alpha := initial learning rate
iter := number of epochs
batch_words := target size in words for batches
compute_loss := true/false
'''
'''
A note on Gensim objects:
Vocabulary: This object represents the vocabulary 
(sometimes called Dictionary in gensim) of the model. 
Besides keeping track of all unique words, this object 
provides extra functionality, such as constructing a huffman tree 
(frequent words are closer to the root), or discarding extremely rare words.
'''

# Create CBOW model with hierarchical softmax
CBOW_model_hs = gensim.models.word2vec.Word2Vec(sentences = sentences, 
                                             window = 4,
                                             hs = 1,
                                             iter = 10,
                                             batch_words = 10,
                                             min_count = 1,
                                             cbow_mean = 1
                                )

# Create CBOW model with negative sampling
CBOW_model_neg = gensim.models.word2vec.Word2Vec(sentences = sentences, 
                                             window = 4,
                                             negative = 10,
                                             iter = 10,
                                             batch_words = 10,
                                             min_count = 1,
                                             cbow_mean =1
                                )

# Create Skip-Gram model with hierarchical softmax
SkipGram_model_hs = gensim.models.word2vec.Word2Vec(sentences = sentences, 
                                             window = 4,
                                             hs = 1,
                                             iter = 10,
                                             batch_words = 10,
                                             min_count = 1,
                                             sg = 1
                                        
                                )

# Create Skip_Gram model with negative sampling
SkipGram_model_neg = gensim.models.word2vec.Word2Vec(sentences = sentences, 
                                             window = 4,
                                             negative = 10,
                                             iter = 10,
                                             batch_words = 10,
                                             min_count = 1
                                )
#Some examples:
v1 = CBOW_model_hs.wv['rain']
# Finds all similar words and provides a similarity index
sim_words1 = CBOW_model_hs.wv.most_similar('away')
#sim_words2 = CBOW_model_neg.wv.most_similar('away')

'''
predict_output_word(context_words_list, topn = 10)
Get the probability distribution of the center word given context words
'''





















