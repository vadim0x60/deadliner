import openai
import numpy as np
import os
import sys
import re

openai.api_key = os.environ['OPENAI']
openai_engine = 'text-similarity-babbage-001'

def _openai_embed_text(text):
    return np.array(openai.Embedding.create(input=text, engine=openai_engine)['data'][0]['embedding'])

def embed(*texts):
    return np.mean([_openai_embed_text(text.strip()) for text in texts], axis=0)

if __name__ == '__main__':
    input_path = sys.argv[1]
    output_path = re.sub('\..+$', '', input_path)
    with open(input_path, 'r') as f:
        np.save(output_path, embed(*f.readlines()))