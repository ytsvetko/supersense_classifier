#!/bin/bash

LABELS=data/labeled_taxonomies/germanet/perception_labels.txt

OUT_DIR=./taxonomies/Perception
CREG_BIN=/usr0/home/ytsvetko/tools/creg/dist/bin/creg

VOCAB=data/vectors/adjectives.vocab
WORD_VECTORS=data/vectors/adjectives.vectors
BROWN_CLUSTERS=data/brown/en-c600

mkdir -p ${OUT_DIR}

echo "Expand by WN synonyms and antonyms"
if [ ! -f ${OUT_DIR}/train_expanded.txt ]; then
  src/expand_labeled_data.py --labeled_data ${LABELS} \
      --out_file ${OUT_DIR}/train_expanded.txt #--expand 
fi

echo "Build training sets"
if [ ! -f ${OUT_DIR}/train.feat ]; then
src/build_training_sets.py --in_file ${OUT_DIR}/train_expanded.txt \
    --out_dir ${OUT_DIR} --vocab ${VOCAB} --vectors ${WORD_VECTORS} \
    --brown_clusters ${BROWN_CLUSTERS}
fi

echo "Run multi-way classifier. " #Default - Random Forest with 300 trees
src/classify.py --train_features ${OUT_DIR}/train.feat \
    --train_labels ${OUT_DIR}/train.labels \
    --test_features ${OUT_DIR}/test.feat \
    --test_predicted_labels_out ${OUT_DIR}/test.predicted \
    --num_cross_validation_folds 5 #--priors balanced --classifier "SVM"

#${CREG_BIN} -x ${OUT_DIR}/train.feat -y ${OUT_DIR}/train.labels --l1 1.0 \
#     --tx ${OUT_DIR}/test.feat -D -W > ${OUT_DIR}/test.predicted.creg

#TODO Active learning
echo "Update training sets"
