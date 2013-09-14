#!/usr/bin/env python2.7

import sys, os
import collections
import codecs
import argparse
from itertools import izip
import json 

parser = argparse.ArgumentParser()

parser.add_argument("--in_file", required=True)
parser.add_argument("--out_dir", required=True)

parser.add_argument("--vocab")
parser.add_argument("--vectors")
parser.add_argument("--brown_clusters")

args = parser.parse_args()

def LoadVectors(vocab_filename, vectors_filename):
  feature_vectors = {}
  for word, features in izip(open(vocab_filename), open(vectors_filename)):
    word = word.strip()
    if not word.isalpha():
      continue
    features_dict = { "V_"+str(ind) : float(str_feat) for ind, str_feat in enumerate(features.split()) }
    feature_vectors[word] = features_dict
  return feature_vectors

def LoadBrownClusters(brown_filename, vocab):
  for line in codecs.open(brown_filename, "r", "utf-8"):
    # 111111101010	love	265727
    cluster, word, score = line.split('\t')
    if word not in vocab:
      continue
    feature_dict = { "B_"+cluster:1 }
    vocab[word].update(feature_dict)

def main(argv):
  vectors = LoadVectors(args.vocab, args.vectors)
  LoadBrownClusters(args.brown_clusters, vectors)

  out_features = open(os.path.join(args.out_dir, "train.feat"), "w")
  out_labels = open(os.path.join(args.out_dir, "train.labels"), "w")
  seen_in_training = set()
  for line in open(args.in_file):
    word, label, relation = line.strip().split("\t")
    if word not in vectors:
      continue
    seen_in_training.add(word)
    features_str = json.dumps(vectors[word], sort_keys=True)
    out_features.write("{}_{}_{}\t{}\n".format(word, label, relation, features_str))
    out_labels.write("{}_{}_{}\t{}\n".format(word, label, relation, label.upper()))
  test_features_file = open(os.path.join(args.out_dir, "test.feat"), "w")
  for word, features in sorted(vectors.iteritems()):
    if word in seen_in_training:
      continue
    features_str = json.dumps(features, sort_keys=True)
    test_features_file.write("{}_vocab\t{}\n".format(word, features_str))


if __name__ == '__main__':
  main(sys.argv)

