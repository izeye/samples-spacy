import spacy
print spacy

nlp = spacy.load('en')
print nlp

doc = nlp(u'Hello, world. Here are two sentences.')
print doc

texts = [u'One document.', u'...', u'Lots of documents']
print texts

iter_texts = (texts[i % 3] for i in xrange(100000000))
print iter_texts

for i, document in enumerate(nlp.pipe(iter_texts)):
    print i, document
    assert document.is_parsed
    if (i == 100):
        break

token = doc[0]
print token

iterator = doc.sents
print iterator

sentence = next(iterator)
print sentence

assert token is sentence[0]
assert sentence.text == 'Hello, world.'

sentence = next(iterator)
print sentence

hello_id = nlp.vocab.strings['Hello']
print hello_id

hello_str = nlp.vocab.strings[hello_id]
print hello_str

assert token.orth == hello_id == 3125
assert token.orth_ == hello_str == 'Hello'

print token.shape_
assert token.shape_ == 'Xxxxx'

for lexeme in nlp.vocab:
    if lexeme.is_alpha:
        lexeme.shape_ = u'W'
    elif lexeme.is_digit:
        lexeme.shape_ = u'D'
    elif lexeme.is_punct:
        lexeme.shape_ = u'P'
    else:
        lexeme.shape_ = u'M'

print token.shape_
assert token.shape_ == 'W'

from spacy.attrs import ORTH, LIKE_URL, IS_OOV

attr_ids = [ORTH, LIKE_URL, IS_OOV]
print attr_ids

doc_array = doc.to_array(attr_ids)
print doc_array

assert doc_array.shape == (len(doc), len(attr_ids))
assert doc[0].orth == doc_array[0, 0]
assert doc[1].orth == doc_array[1, 0]
assert doc[0].like_url == doc_array[0, 1]
assert list(doc_array[:, 1]) == [t.like_url for t in doc]

doc = nlp(u"Apples and oranges are similar. Boots and hippos aren't.")

apples = doc[0]
oranges = doc[2]
boots = doc[6]
hippos = doc[8]

similarity_between_apples_and_oranges = apples.similarity(oranges)
print similarity_between_apples_and_oranges

similarity_between_boots_and_hippos = boots.similarity(hippos)
print similarity_between_boots_and_hippos

assert similarity_between_apples_and_oranges > similarity_between_boots_and_hippos

from spacy.parts_of_speech import ADV

def is_adverb(token):
    return token.pos == spacy.parts_of_speech.ADV

NNS = nlp.vocab.strings['NNS']
print NNS

NNPS = nlp.vocab.strings['NNPS']
print NNPS

def is_plural_noun(token):
    return token.tag == NNS or token.tag == NNPS

def print_coarse_pos(token):
    print(token.pos_)

def print_fine_pos(token):
    print(token.tag_)

doc = nlp(u"I ate two apples and a banana. So I'm full now.")
print doc

for sentence in doc.sents:
    for token in sentence:
        print token
        print is_adverb(token)
        print is_plural_noun(token)
        print_coarse_pos(token)
        print_fine_pos(token)

def dependency_labels_to_root(token):
    dep_labels = []
    while token.head is not token:
        dep_labels.append(token.dep)
        token = token.head
    return dep_labels

for sentence in doc.sents:
    for token in sentence:
        print token
        print token.orth
        dep_labels = dependency_labels_to_root(token)
        print dep_labels
        for dep_label in dep_labels:
            print nlp.vocab.strings[dep_label]

doc = nlp(u"Mr. Best flew to New York on Saturday morning.")

for ent in doc.ents:
    print ent, ent.label_, ent.orth_
    print ent.root, ent.root.head, ent.root.head.pos, nlp.vocab.strings[ent.root.head.pos], ent.root.head.lemma_

from spacy.tokens.doc import Doc

byte_string = doc.to_bytes()
open('moby_dick.bin', 'wb').write(byte_string)

doc = Doc(nlp.vocab)
for byte_string in Doc.read_bytes(open('moby_dick.bin', 'rb')):
    doc.from_bytes(byte_string)
print doc
