#!/usr/bin/env python2.7

import sys, os
import collections
import argparse
from nltk.corpus import wordnet as wn


def IsAlphaSS(ss):
  for x in ss.lemma_names:
    if x.isalpha():
      return True
  return False

def IsSingleSynset(lemma):
  return len(wn.synsets(lemma, wn.ADJ)) == 1

def LemmaHasNoun(lemma):
  return len(wn.lemmas(lemma, wn.NOUN)) > 0

def IsNounSingleLexName(lemma):
  noun_synsets = wn.synsets(lemma, wn.NOUN)
  lex_names = { x.lexname for x in noun_synsets }
  return len(lex_names) == 1

def LoadHuang():
  filename = "/home/ytsvetko/projects/supersense_classifier/data/vectors/huang/joined.txt"
  result = set()
  for line in open(filename):
    result.add(line.strip().split()[0].lower())
  return result

def LoadManaal():
  filename = "/home/ytsvetko/projects/supersense_classifier/data/vectors/manaal/en-640.txt"
  result = set()
  for line in open(filename):
    result.add(line.strip().split()[0].lower())
  return result
  
def LoadBrown():
  filename = "/home/ytsvetko/projects/supersense_classifier/data/brown/en-c600"
  result = set()
  for line in open(filename):
    result.add(line.strip().split("\t")[1].lower())
  return result

def main(argv):
  huang_vocab = LoadHuang()
  manaal_vocab = LoadManaal()
  brown_vocab = LoadBrown()

  all_lemmas = {x.lower() for x in wn.all_lemma_names(pos=wn.ADJ)}
  all_alpha_lemmas = {x for x in all_lemmas if x.isalpha()}
  all_synsets = set(wn.all_synsets(pos=wn.ADJ))
  all_alpha_synsets = {x for x in all_synsets if IsAlphaSS(x)}
  all_lemmas_with_single_synset = {x for x in all_lemmas if IsSingleSynset(x)}
  all_lemmas_ambig_synset = {x for x in all_lemmas if not IsSingleSynset(x)}
  all_lemmas_with_single_synset_alpha = {x for x in all_lemmas_with_single_synset if x.isalpha()}
  all_lemmas_ambig_synset_alpha = {x for x in all_lemmas_ambig_synset if x.isalpha()}
  all_alpha_lemmas_has_noun = {x for x in all_alpha_lemmas if LemmaHasNoun(x)}
  all_alpha_lemmas_has_noun_single_lexname = {x for x in all_alpha_lemmas_has_noun if IsNounSingleLexName(x) }
  print "all_lemmas:", len(all_lemmas)
  print "all_alpha_lemmas:", len(all_alpha_lemmas)
  print "all_synsets:", len(all_synsets)
  print "all_alpha_synsets:", len(all_alpha_synsets)
  print "all_lemmas_with_single_synset:", len(all_lemmas_with_single_synset)
  print "all_lemmas_ambig_synset:", len(all_lemmas_ambig_synset)
  print "all_lemmas_with_single_synset_alpha", len(all_lemmas_with_single_synset_alpha)
  print "all_lemmas_ambig_synset_alpha", len(all_lemmas_ambig_synset_alpha)
  print "all_alpha_lemmas_has_noun", len(all_alpha_lemmas_has_noun)
  print "all_alpha_lemmas_has_noun_single_lexname", len(all_alpha_lemmas_has_noun_single_lexname)
  print "huang.intersect(all_alpha_lemmas)", len(huang_vocab.intersection(all_alpha_lemmas))
  print "manaal.intersect(all_alpha_lemmas)", len(manaal_vocab.intersection(all_alpha_lemmas))
  print "brown.intersect(all_alpha_lemmas)", len(brown_vocab.intersection(all_alpha_lemmas))
  print "huang*manaal*brown*all_alpha_lemmas", len(huang_vocab.intersection(all_alpha_lemmas, manaal_vocab, brown_vocab))
  print "huang.intersect(all_lemmas_with_single_synset_alpha)", len(huang_vocab.intersection(all_lemmas_with_single_synset_alpha))
  print "manaal.intersect(all_lemmas_with_single_synset_alpha)", len(manaal_vocab.intersection(all_lemmas_with_single_synset_alpha))
  print "brown.intersect(all_lemmas_with_single_synset_alpha)", len(brown_vocab.intersection(all_lemmas_with_single_synset_alpha))
  print "huang*manaal*brown*all_lemmas_with_single_synset_alpha", len(huang_vocab.intersection(all_lemmas_with_single_synset_alpha, manaal_vocab, brown_vocab))
  # print all_alpha_lemmas - huang_vocab.union(manaal_vocab)

if __name__ == '__main__':
  main(sys.argv)

