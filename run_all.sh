#!/bin/bash

LABELS=data/labeled_taxonomies/germanet/germanet_labels.txt
OUT_DIR=./taxonomies/GermaNet
#LABELS=data/labeled_taxonomies/dixon/dixon_labels.txt
#OUT_DIR=./taxonomies/Dixon


CREG_BIN=/usr0/home/ytsvetko/tools/creg/dist/bin/creg

#EMBEDDINGS=data/vectors/huang/joined.txt
EMBEDDINGS=data/vectors/manaal/en-de-16.txt
BROWN_CLUSTERS=data/brown/en-c600

mkdir -p ${OUT_DIR}

echo "Split Test and Train"
src/split_train_test.py --seed_file ${LABELS} \
    --embeddings ${EMBEDDINGS} \
    --out_train ${OUT_DIR}/train_seed.txt \
    --out_test ${OUT_DIR}/test_seed.txt

echo "Expand by WN synonyms and antonyms"
src/expand_labeled_data.py --labeled_data ${OUT_DIR}/train_seed.txt \
    --out_file ${OUT_DIR}/expanded.txt --expand 

src/build_training_sets.py --in_file ${OUT_DIR}/train_seed.txt \
    --out_feat ${OUT_DIR}/train_seed.feat \
    --out_labels ${OUT_DIR}/train_seed.labels \
    --test_set ${OUT_DIR}/expanded.txt \
    --out_test_feat ${OUT_DIR}/expanded.feat \
    --out_test_labels ${OUT_DIR}/expanded.labels \
    --embeddings ${EMBEDDINGS} \
    --brown_clusters ${BROWN_CLUSTERS}

echo "Run multi-way classifier. " #Default - Random Forest with 300 trees
src/classify.py --train_features ${OUT_DIR}/train_seed.feat \
    --train_labels ${OUT_DIR}/train_seed.labels \
    --test_features ${OUT_DIR}/expanded.feat \
    --test_predicted_labels_out ${OUT_DIR}/expanded.predicted \
    --write_posterior_probabilities
    #--golden_labels ${OUT_DIR}/expanded.labels
    #--num_cross_validation_folds 5 #--priors balanced #--classifier "SVM"

#${CREG_BIN} -x ${OUT_DIR}/train.feat -y ${OUT_DIR}/train.labels --l1 1.0 \
#     --tx ${OUT_DIR}/test.feat -D -W > ${OUT_DIR}/test.predicted.creg


## Iter 2

echo "Selecting best expanded words"
src/filter_expanded.py --predictions ${OUT_DIR}/expanded.predicted \
    --orig_seed ${OUT_DIR}/train_seed.txt \
    --out_file ${OUT_DIR}/expanded_seed.txt

echo "Expand by WN synonyms and antonyms"
src/expand_labeled_data.py --labeled_data ${OUT_DIR}/expanded_seed.txt \
    --out_file ${OUT_DIR}/expanded.txt --expand 

src/build_training_sets.py --in_file ${OUT_DIR}/expanded_seed.txt \
    --out_feat ${OUT_DIR}/train_seed.feat \
    --out_labels ${OUT_DIR}/train_seed.labels \
    --out_test_feat ${OUT_DIR}/vocab.feat \
    --embeddings ${EMBEDDINGS} \
    --brown_clusters ${BROWN_CLUSTERS} \
    --include_training

echo "Run multi-way classifier. " #Default - Random Forest with 300 trees
src/classify.py --train_features ${OUT_DIR}/train_seed.feat \
    --train_labels ${OUT_DIR}/train_seed.labels \
    --test_features ${OUT_DIR}/vocab.feat \
    --test_predicted_labels_out ${OUT_DIR}/vocab.predicted \
    --write_posterior_probabilities
    #--num_cross_validation_folds 5 #--priors balanced #--classifier "SVM"

src/eval.py --predicted_results ${OUT_DIR}/vocab.predicted \
    --held_out_seed ${OUT_DIR}/test_seed.txt

