#!/usr/bin/env python2.7

import sys
import glob
import os
import re
import argparse
import collections


parser = argparse.ArgumentParser()

parser.add_argument("--creg_results_file_pattern", required=True)
parser.add_argument("--out_file")

args = parser.parse_args()

def avg(l):
  return sum(l)/len(l)

def ReadAccuracy(filename):
  line = ""
  try:
    # get last line
    line = open(filename).readlines()[-1]
  except:
    pass  # File is empty
  match = re.match("Held-out accuracy: ([0-9.]+)", line)
  if match is None:
    print "No accuracy in file:", filename
    return None
  else:
    return float(match.group(1))

def CollectResults(creg_results_file_pattern, out_file):
  experiment_stats = []
  for filename in glob.glob(creg_results_file_pattern):
    accuracy = ReadAccuracy(filename)
    if accuracy is not None:
      experiment_stats.append(accuracy)
  if len(experiment_stats) > 0:
    out_file.write("{0}\t[{1}..{2}]\n".format(avg(experiment_stats), 
                   min(experiment_stats), max(experiment_stats)))

def main():
  if args.out_file is not None:
    out_file = open(args.out_file, "a")
  else:
    out_file = sys.stdout

  CollectResults(args.creg_results_file_pattern, out_file)
 
if __name__ == '__main__':
  main()


