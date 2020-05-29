rm -rf core.* 
rm -rf ./output/snapshots/*
#DATA_ROOT=/DATA/disk1/of_imagenet_example
#DATA_ROOT=/DATA/disk1/ImageNet/ofrecord
DATA_ROOT=/dataset/ImageNet/ofrecord
#DATA_ROOT=/dataset/imagenet-mxnet
  #python3 cnn_benchmark/of_cnn_train_val.py \
#nvprof -f -o resnet.nvvp \
#gdb --args \
  python3 cnn_e2e/of_cnn_train_val.py \
    --train_data_dir=$DATA_ROOT/train \
    --train_data_part_num=256 \
    --val_data_dir=$DATA_ROOT/validation \
    --val_data_part_num=256 \
    --num_nodes=1 \
    --node_ips='11.11.1.12,11.11.1.14' \
    --gpu_num_per_node=4 \
    --optimizer="momentum-cosine-decay" \
    --learning_rate=0.256 \
    --loss_print_every_n_iter=20 \
    --batch_size_per_device=56 \
    --val_batch_size_per_device=125 \
    --use_boxing_v2=True \
    --use_new_dataloader=True \
    --model="resnet50" 
    # --train_data_dir=$DATA_ROOT/train \
    # --train_data_part_num=256 \
    # --val_data_dir=$DATA_ROOT/validation \
    # --val_data_part_num=256 \
    #--use_fp16 true \
    #--weight_l2=3.0517578125e-05 \
    #--num_examples=1024 \
    #--optimizer="momentum-decay" \
    #--data_dir="/mnt/13_nfs/xuan/ImageNet/ofrecord/train"
    #--data_dir="/mnt/dataset/xuan/ImageNet/ofrecord/train"
    #--warmup_iter_num=10000 \
