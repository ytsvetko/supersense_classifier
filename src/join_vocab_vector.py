#!/usr/bin/env python2.7

import argparse
import itertools

parser = argparse.ArgumentParser()

parser.add_argument("--vocab", required=True)
parser.add_argument("--vectors", required=True)
parser.add_argument("--out_file", required=True)

args = parser.parse_args()

def main():
  out_file = open(args.out_file, "w")
  for word, features in itertools.izip(open(args.vocab), open(args.vectors)):
    word = word.strip()
    out_file.write("{} {}".format(word, features))
    
if __name__ == '__main__':
  main()


