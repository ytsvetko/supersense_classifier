#!/bin/bash

LABELS=data/labeled_taxonomies/germanet/germanet_labels.txt

OUT_DIR=./taxonomies/GermaNet
CREG_BIN=/usr0/home/ytsvetko/tools/creg/dist/bin/creg

VOCAB=data/vectors/adjectives.vocab
WORD_VECTORS=data/vectors/adjectives.vectors
BROWN_CLUSTERS=data/brown/en-c600

mkdir -p ${OUT_DIR}

echo "Expand by WN synonyms and antonyms"
src/expand_labeled_data.py --labeled_data ${LABELS} \
    --out_file ${OUT_DIR}/expanded.txt --expand 

src/build_training_sets.py --in_file ${LABELS} \
    --out_feat ${OUT_DIR}/train_seed.feat \
    --out_labels ${OUT_DIR}/train_seed.labels \
    --test_set ${OUT_DIR}/expanded.txt \
    --out_test_feat ${OUT_DIR}/expanded.feat \
    --out_test_labels ${OUT_DIR}/expanded.labels \
    --vocab ${VOCAB} --vectors ${WORD_VECTORS} \
    --brown_clusters ${BROWN_CLUSTERS}

echo "Run multi-way classifier. " #Default - Random Forest with 300 trees
src/classify.py --train_features ${OUT_DIR}/train_seed.feat \
    --train_labels ${OUT_DIR}/train_seed.labels \
    --test_features ${OUT_DIR}/expanded.feat \
    --golden_labels ${OUT_DIR}/expanded.labels \
    --test_predicted_labels_out ${OUT_DIR}/expanded.predicted \
    --priors "{\"RELATIONSHIP\":0.0}" \
    --write_posterior_probabilities \
    --num_cross_validation_folds 5 #--priors balanced --classifier "SVM"

#${CREG_BIN} -x ${OUT_DIR}/train.feat -y ${OUT_DIR}/train.labels --l1 1.0 \
#     --tx ${OUT_DIR}/test.feat -D -W > ${OUT_DIR}/test.predicted.creg


## Iter 2

echo "Selecting best expanded words"
src/filter_expanded.py --predictions ${OUT_DIR}/expanded.predicted \
    --orig_seed ${LABELS} \
    --out_file ${OUT_DIR}/expanded_seed.txt

echo "Expand by WN synonyms and antonyms"
src/expand_labeled_data.py --labeled_data ${OUT_DIR}/expanded_seed.txt \
    --out_file ${OUT_DIR}/expanded.txt --expand 

src/build_training_sets.py --in_file ${OUT_DIR}/expanded_seed.txt \
    --out_feat ${OUT_DIR}/train_seed.feat \
    --out_labels ${OUT_DIR}/train_seed.labels \
    --test_set ${OUT_DIR}/expanded.txt \
    --out_test_feat ${OUT_DIR}/expanded.feat \
    --out_test_labels ${OUT_DIR}/expanded.labels \
    --vocab ${VOCAB} --vectors ${WORD_VECTORS} \
    --brown_clusters ${BROWN_CLUSTERS}

echo "Run multi-way classifier. " #Default - Random Forest with 300 trees
src/classify.py --train_features ${OUT_DIR}/train_seed.feat \
    --train_labels ${OUT_DIR}/train_seed.labels \
    --test_features ${OUT_DIR}/expanded.feat \
    --golden_labels ${OUT_DIR}/expanded.labels \
    --test_predicted_labels_out ${OUT_DIR}/expanded.predicted \
    --priors "{\"RELATIONSHIP\":0.0}" \
    --write_posterior_probabilities \
    --num_cross_validation_folds 5 #--priors balanced --classifier "SVM"


#TODO Active learning
echo "Update training sets"
