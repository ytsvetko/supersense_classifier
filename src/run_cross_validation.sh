#!/bin/bash

FEAT_FILE=${1}/train.feat
LABEL_FILE=${1}/train.labels

CREG_BIN=${2}

CROSS_VALIDATION_DIR=${1}/cross_validation
mkdir -p ${CROSS_VALIDATION_DIR}
CROSS_VALIDATION_RESULTS=${CROSS_VALIDATION_DIR}/summary.txt
PREV_WEIGHTS=x
NUM_FOLDS=10

for ((i = 0; i < NUM_FOLDS; i++)); do
  echo "Cross validation, fold: $i"
  OUT_FILE_PREFIX=${CROSS_VALIDATION_DIR}/fold_${i}
  TRAIN_FEAT=${OUT_FILE_PREFIX}.train.feat
  TRAIN_LABEL=${OUT_FILE_PREFIX}.train.label
  TEST_FEAT=${OUT_FILE_PREFIX}.test.feat
  TEST_LABEL=${OUT_FILE_PREFIX}.test.label
  OUT_WEIGHTS=${OUT_FILE_PREFIX}.weights
  if [ "$PREV_WEIGHTS" == "x" ] ; then
    CMD_PREV_WEIGHTS=
  else
    CMD_PREV_WEIGHTS="-w $PREV_WEIGHTS"
  fi
  PREV_WEIGHTS=${OUT_WEIGHTS}
  PREDICTED_LABELS=${OUT_FILE_PREFIX}.test.predicted
  RESULTS=${OUT_FILE_PREFIX}.results.txt
  
  # Since Creg needs two separate files for Features and Labels, we run
  # generate_fold.py once for each of these files.
  src/generate_fold.py --fold_num=$i --total_folds_num=${NUM_FOLDS} \
      --in_data_file=${FEAT_FILE} --out_train_file=${TRAIN_FEAT} --out_test_file=${TEST_FEAT}

  src/generate_fold.py --fold_num=$i --total_folds_num=${NUM_FOLDS} \
      --in_data_file=${LABEL_FILE} --out_train_file=${TRAIN_LABEL} --out_test_file=${TEST_LABEL}

  # Now run Creg and store the results in a file.
  # If it fails, see the ${RESULTS} for error messages.
  ${CREG_BIN} -x ${TRAIN_FEAT} -y ${TRAIN_LABEL} --l2 0.5 --tx ${TEST_FEAT} \
      --ty ${TEST_LABEL} -D --z ${OUT_WEIGHTS} \
          > ${PREDICTED_LABELS} 2> ${RESULTS}


done

# Now parse the results files from all the folds, calculate the Mean, Min and
# Max.
src/collect_results.py \
    --creg_results_file_pattern="${CROSS_VALIDATION_DIR}/fold_?.results.txt" \
    --out_file="${CROSS_VALIDATION_RESULTS}"

cat ${CROSS_VALIDATION_RESULTS}
