#!/usr/bin/env python2.7

import sys
import argparse
import random

"""Generates Test and Training files for a single fold of Cross Validation.
"""

parser = argparse.ArgumentParser()

parser.add_argument("--fold_num", default=0, type=int, help="Current fold number")
parser.add_argument("--total_folds_num", default=10, type=int, help="Number of folds")
parser.add_argument("--in_data_file", required=True, help="Input file in creg format to cut into folds")
parser.add_argument("--out_train_file", required=True, help="Output file in creg format for training") 
parser.add_argument("--out_test_file", required=True, help="Output file in creg format for test")

args = parser.parse_args()

def main(argv):
  random.seed(1234567)
  #print "ARGS:", args
  train_file = open(args.out_train_file, "w")
  test_file = open(args.out_test_file, "w")
  for line in open(args.in_data_file):
    if random.randint(0, args.total_folds_num-1) == args.fold_num:
      test_file.write(line)
    else:
      train_file.write(line)

if __name__ == '__main__':
  main(sys.argv)


