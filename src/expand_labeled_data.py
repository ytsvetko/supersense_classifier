#!/usr/bin/env python2.7

import sys, os
import collections
import argparse
from nltk.corpus import wordnet as wn

#TODO filter out proposals to expand the set that contradict with other training sets. 

parser = argparse.ArgumentParser()

parser.add_argument("--labeled_data", required=True)
parser.add_argument("--out_file", required=True)
parser.add_argument("--expand", action='store_true', default=False)

args = parser.parse_args()

def FindRelated(word):
  related = set()
  word = word.lower().strip()
  synsets = wn.synsets(word, wn.ADJ)
  for w in synsets:
    for synonym in w.lemmas:  
      related.add( (synonym.name, "synonym") )
      for hypernym in w.hypernyms():  
        related.add( (hypernym.name, "hypernym") )
      for antonym in synonym.antonyms():
        related.add( (antonym.name, "antonym") )
  related_through_nouns = set()
  for w, relation in related:
    related_through_nouns.update(ExpandThroughNouns(w))
  #related.update(related_through_nouns)
  return related

def ExpandThroughNouns(word):
  nouns = set()
  for w in wn.synsets(word, wn.NOUN):
    for synonym in w.lemmas:  
      nouns.add( (synonym.name, "synonym_noun") )
      for hypernym in w.hypernyms():  
        nouns.add( (hypernym.name, "hypernym_noun") )
      for antonym in synonym.antonyms():
        nouns.add( (antonym.name, "antonym_noun") )
  noun_related = set()
  for (w, relation) in nouns:
    synsets = wn.synsets(w, wn.ADJ)
    for s in synsets:
      noun_related.add( (w, relation) )
  return noun_related

def LoadAndExpandSeed(filename, expand):
  word_dict = collections.defaultdict(list)
  for line in open(filename):
    if line.strip() == "" : 
      continue
    if len(line.strip().lower().split()) != 2:
      print line
    word, label = line.strip().lower().split()
    word_dict[word].append((label, "seed"))
    if expand:
      for related, relation in FindRelated(word):
        word_dict[related].append( (label, relation) )
  return word_dict

def main(argv):
  word_dict = LoadAndExpandSeed(args.labeled_data, args.expand)
  out_file = open(args.out_file, "w")
  for word, variants in word_dict.iteritems():
    labels = {}
    for label, relation in variants:
      if label not in labels or relation == "seed":
        labels[label] = relation
    if len(labels) > 1:
      labels = { label:relation for label, relation in variants if not relation.endswith("_noun") }
    if len(labels) > 1:
      labels = { label:relation for label, relation in variants if relation == "seed" }
    for label, relation in labels.iteritems():
      out_file.write("{}\t{}\t{}\n".format(word, label, relation))

if __name__ == '__main__':
  main(sys.argv)

