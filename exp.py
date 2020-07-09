# ---
# jupyter:
#   jupytext:
#     formats: notebooks//ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.4.1
#   kernelspec:
#     display_name: NLP
#     language: python
#     name: nlp
# ---

# %% [markdown]
# # Pathway
#
# ## Naive
#
# ### String Matching
# + Single word
# + Two words
# + Regular expression
#
# ### Vector Matching
# + Single word
# + Two words
# + Multi words
#
# ### Attribute Matching
# + Single word
#     + Related noun
#     + Related verb
#     + Related adjective
# + Two words
#     + related phrase
# + Multi words
#     + related phrase
#     + related clause
# + Multi Sentence
#     + related content
#     + related next sentence (future)
#     + related previous sentence (history)
#     + related topic
#     + related sentiment
#     + related style
#     + related source

# %% [markdown]
# # Tech
#
# ## Indexing
#
# ### String
# + Words
# + Phrases
# + Sentences
#
# ### Vector
# + Words
# + Phrases
# + Sentences
#
# ## Ranking Search Space
#
# + Frequent Search
# + Categories
#
# ## Cache Result

# %%
import spacy

# %%
import ngtpy

# %%
import numpy as np

# %%

dim = 10
objects = []
# for i in range(0, 100) :
#     vector = random.sample(range(100), dim)
#     objects.append(vector)

objects = np.random.randint(0,100,(100,10))

query = np.random.randint(0,100,(10,))

ngtpy.create(b"tmp", dim)
index = ngtpy.Index(b"tmp")
index.batch_insert(objects)
index.save()

result = index.search(query, 3)

for i, o in enumerate(result) :
    print(str(i) + ": " + str(o[0]) + ", " + str(o[1]))
    object = index.get_object(o[0])
    print(object)

# %%
