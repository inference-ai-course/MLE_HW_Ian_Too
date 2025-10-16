# Architecture and Training of Large Language Models

- What is the transformer architecture and the attention mechanism?
- What is next token prediction and hallucination?
- What is LLM pre-training and how do we do it?
- Supervised fine tuning? (SFT)
- What are the different alignment techniques? PPO vs DPO
- Data requirements, cost and challenges?
- Time scaling 01 , 03
- Hands on project introduction


### Transformer Architecture : Components

The transformer architecture has the following key components:

1. Multi-head self attention



2. Feed forward neural network

- this basically means taking time to process information from other tokens.

3. Positional encoding

--



4. Later normalization (what does this mean?)



## Don't Mind me

Transformers understand relationships within sequences. Uses self attention mechanisms.

Importance in relation to the other elements. Certain words hold more context and meaning of the sentence
Each word/token pays attention to other words and pay attention to their relative importance.


Self attention within transformers:
 
 For example we have an input sequences divided into tokens

 Each token is associated with three vectors: query, key, value



 # Input processing

 Each input is first converted into a vector using an embedding layer.
 Positional embeddings are added to mainain order of the sequence. 