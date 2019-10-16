#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RAW TEXT CLEANER
STA 586 Project
---------------------------------------------------
Formats raw text input and outputs file for use in 
training natural language recommendation model.

use: $> python cleaner.py [options] <inputPath> <outputPath>
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
import sys, os 

#######################################################
#######################################################

#### global options ####
directory = 0          # 
min_len = 3            # 
dl_punkt = 0           #
########################

options = sys.argv[1:-2]
valid_lens = ["1","2","3","4","5","6", "7", "8", "9", "10"]

for arg in options:
    if arg in ("-b", "--batch"):
        directory = 1
        print("Continuing in batch mode...")
    if arg in ("-p", "--punkt", "-d", "--download"):
        dl_punkt = 1
    if arg in valid_lens:
        min_len = int(arg)
        print("Minimum sentence length set to %s..." % arg)


if (len(sys.argv) <= 3):
    sys.exit("Usage: cleaner.py [options] <inputPath> <outputPath>")

if dl_punkt:
    dl('punkt')

input_file_path = sys.argv[-2]
output_file_name = sys.argv[-1]
output_stream = open(output_file_name, "w+")

def scrub_file(input_file, output_file):
    input_stream = open(input_file)
    full_input_text = input_stream.read()
    raw_sentence_array = tok.sent_tokenize(full_input_text)
    
    for sent in raw_sentence_array:
        words = tok.word_tokenize(sent)
        words = [w.lower() for w in words if w.isalpha()]
        if (len(words) >= min_len):
            final_string = ((' '.join(words)) + "\n")
            output_file.write(final_string)
            
print("\nScrubbing...\n")

if directory:
    try:
        for entry in os.listdir(input_file_path):
            if os.path.isfile(os.path.join(input_file_path, entry)):
                scrub_file(os.path.join(input_file_path, entry), output_stream)
    except:
        sys.exit("Error walking directory.")
if not directory:
    try:
        scrub_file(input_file_path, output_stream)
    except:
        sys.exit("Error scrubbing file.")
    
output_stream.close()
print("Spick and span.\n\nOutput:", output_file_name,"\n")
