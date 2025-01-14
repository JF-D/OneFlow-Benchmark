rm -rf core.*
rm -rf ./output/snapshots/*

if [ -n "$1" ]; then
    NUM_EPOCH=$1
else
    NUM_EPOCH=50
fi
echo NUM_EPOCH=$NUM_EPOCH

# training with imagenet
if [ -n "$2" ]; then
    DATA_ROOT=$2
else
    DATA_ROOT=data/mini-imagenet/ofrecord
fi
echo DATA_ROOT=$DATA_ROOT

LOG_FOLDER=../logs
mkdir -p $LOG_FOLDER
LOGFILE=$LOG_FOLDER/alexnet_training.log

# python3 of_cnn_train_val.py \
#      --num_nodes=1 \
#      --gpu_num_per_node=1 \
#      --optimizer="sgd" \
#      --momentum=0.875 \
#      --label_smoothing=0.1 \
#      --learning_rate=1.024 \
#      --loss_print_every_n_iter=100 \
#      --batch_size_per_device=128 \
#      --val_batch_size_per_device=50 \
#      --num_epoch=$NUM_EPOCH \
#      --model="alexnet" #2>&1 | tee ${LOGFILE}

python3 of_cnn_train_val.py \
     --num_examples=25600 \
     --train_data_dir=$DATA_ROOT/train \
     --train_data_part_num=1 \
     --val_data_dir=$DATA_ROOT/validation \
     --val_data_part_num=4 \
     --num_nodes=1 \
     --gpu_num_per_node=1 \
     --optimizer="sgd" \
     --momentum=0.875 \
     --label_smoothing=0.1 \
     --learning_rate=1.024 \
     --loss_print_every_n_iter=100 \
     --batch_size_per_device=128 \
     --val_batch_size_per_device=50 \
     --num_epoch=$NUM_EPOCH \
     --model="alexnet" #2>&1 | tee ${LOGFILE}

echo "Writting log to ${LOGFILE}"
