#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RAW TEXT CLEANER
STA 586 Project
---------------------------------------------------
Formats raw text input and outputs file for use in 
training natural language recommendation model.

use: $> python cleaner.py inputFile outputFileName      
--------------------------------------------------- 
1. import raw .txt
2. tokenize by sentence
3. tokenize each sentence in array by word
4. remove punctuation 
5. reassemble sentence as single string
6. append to output file with \n terminator  
"""

#######################################################
#######################################################

"""
# nltk - natural language toolkit. native on spyder, install othewise.
# punkt package required by nltk for tokenization. 
# nltk has own download method. only needs to be downloaded once. 
"""
from nltk import download as dl, tokenize as tok
import sys
dl('punkt')

#######################################################
#######################################################

if (len(sys.argv) != 3):
    sys.exit("Usage: cleaner inputFile outputFileName")

input_file_path = sys.argv[1]
output_file_name = sys.argv[2]

print("\nReading input file")
input_file = open(input_file_path)
full_text = input_file.read()
print("Creating output file")
output_file = open(output_file_name, "w+")
    
raw_sentence_array = tok.sent_tokenize(full_text)
tok_sentence_array = []

print("\nScrubbing...")
for sent in raw_sentence_array:
    words = tok.word_tokenize(sent)
    words = [w.lower() for w in words if w.isalpha()]
    final_string = ((' '.join(words)) + "\n")
    output_file.write(final_string)

output_file.close()
print("Spick and span.\nOutput:", output_file_name,"\n")