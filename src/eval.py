#!/usr/bin/env python2.7

import sys
import json
import argparse
import collections


parser = argparse.ArgumentParser()

parser.add_argument("--predicted_results", required=True)
parser.add_argument("--held_out_seed", required=True)
parser.add_argument("--out_file", default=None)

args = parser.parse_args()

def CollectResults(predicted_results, seed, out_file):
  hist = collections.Counter()
  for line in open(predicted_results):
    instance, label, posteriors_str = line.strip().split("\t")
    posteriors = json.loads(posteriors_str)
    sorted_posteriors = sorted(posteriors.iteritems(), key=lambda x: x[1], reverse=True)
    sorted_labels = [k.lower() for k,v in sorted_posteriors]
    # covert_substance_antonym
    word = instance.split("_")[0].lower()
    if word in seed:
      min_pos = 100000
      for label in seed[word]:
        min_pos = min(min_pos, sorted_labels.index(label))
      hist[min_pos] += 1
  print hist

def LoadSeed(seed_filename):
  result = collections.defaultdict(set)
  for line in open(seed_filename):
    line = line.strip()
    if len(line) == 0:
      continue
    word, label = line.split("\t")
    result[word.lower()].add(label.lower())
  return result

def main():
  if args.out_file is not None:
    out_file = open(args.out_file, "a")
  else:
    out_file = sys.stdout

  seed = LoadSeed(args.held_out_seed)
  CollectResults(args.predicted_results, seed, out_file)
 
if __name__ == '__main__':
  main()


