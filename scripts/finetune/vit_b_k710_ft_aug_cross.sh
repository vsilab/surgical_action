#!/bin/sh
#SBATCH -J ytian08_video                     # Job name, customize as needed
#SBATCH --time=02-00:00:00  #requested time (DD-HH:MM:SS)
#SBATCH -p patralab                     #running on "mpi" partition/queue
#SBATCH -c 43
#SBATCH --gres=gpu:a100:1
#SBATCH -n 1                            # tasks requested
#SBATCH --mem=100g                      # Memory allocation, adjust as necessary
#SBATCH --output=job.%j.out             # Standard output file, customize path/filename as desired
#SBATCH --error=job.%j.err              # Standard error file, customize path/filename as desired
#SBATCH --mail-type=ALL                 # Email notifications, adjust if necessary
#SBATCH --mail-user=Yuchen.Tian@tufts.edu  # Your email for notifications

# Environment setup
#module load python/3.8  # Load Python or any other module required for your project
module av gcc
#module load anaconda/2021.05 cuda/11.0 cudnn/8.0.4-11.0 gcc/5.3.0
module load anaconda/2021.05 cuda/12.2 cudnn/8.0.4-11.0 gcc/7.3.0
source activate /cluster/tufts/patralab/ytian08/condaenv/videomaev2

export OUTPUT_DIR='/cluster/tufts/patralab/ytian08/action/VideoMAEv2/work_dir/vit_g_hybrid_pt_120e_CholecT45_split_aug_crossentropy_ft'
export DATA_PATH='/cluster/tufts/patralab/ytian08/action/data/frames'
export MODEL_PATH='/cluster/tufts/patralab/ytian08/action/VideoMAEv2/model_zoo/vit_g_hybrid_pt_1200e.pth'
export MASTER_PORT=$((12000 + $RANDOM % 20000))
export OMP_NUM_THREADS=1

# Execution command
# python -m torch.distributed.launch VideoMAEv2/run_class_finetuning.py \
#      --model vit_base_patch16_224 \
#      --data_set CholecT45 \
#      --nb_classes 10 \
#      --data_path "${DATA_PATH}" \
#      --finetune "${MODEL_PATH}" \
#      --log_dir "${OUTPUT_DIR}" \
#      --output_dir "${OUTPUT_DIR}" \
#      --batch_size 16 \
#      --input_size 224 \
#      --short_side_size 224 \
#      --save_ckpt_freq 10 \
#      --num_frames 16 \
#      --sampling_rate 4 \
#      --num_sample 2 \
#      --num_workers 10 \
#      --opt adamw \
#      --lr 7e-4 \
#      --drop_path 0.1 \
#      --head_drop_rate 0.0 \
#      --layer_decay 0.75 \
#      --opt_betas 0.9 0.999 \
#      --warmup_epochs 5 \
#      --epochs 90 \
#      --test_num_segment 5 \
#      --test_num_crop 3 \
#      --dist_eval --enable_deepspeed

python ../VideoMAEv2/run_class_finetuning.py \
     --model vit_giant_patch14_224 \
     --data_set CholecT45 \
     --nb_classes 10 \
     --data_path "${DATA_PATH}" \
     --finetune "${MODEL_PATH}" \
     --log_dir "${OUTPUT_DIR}" \
     --output_dir "${OUTPUT_DIR}" \
     --eval \
     --batch_size 3 \
     --input_size 224 \
     --short_side_size 224 \
     --save_ckpt_freq 10 \
     --num_frames 16 \
     --sampling_rate 4 \
     --num_sample 2 \
     --num_workers 10 \
     --opt adamw \
     --lr 7e-4 \
     --drop_path 0.1 \
     --head_drop_rate 0.0 \
     --layer_decay 0.75 \
     --opt_betas 0.9 0.999 \
     --warmup_epochs 5 \
     --epochs 60 \
     --test_num_segment 5 \
     --test_num_crop 3 \
     --dist_eval --enable_deepspeed