import ivtmetrics # install using: pip install ivtmetrics

# for PyTorch
import dataloader_pth as dataloader
from torch.utils.data import DataLoader

# for TensorFlow v1 & v2
import tensorflow as tf
import dataloader_tf as dataloader

metrics = ivtmetrics.Recognition()

# initialize dataset: 
dataset = dataloader.CholecT50( 
          dataset_dir="../CholecT45/CholecT45", 
          dataset_variant="cholect45-crossval",
          test_fold=1,
          augmentation_list=['original', 'vflip', 'hflip', 'contrast', 'rot90'],
          )

# build dataset
train_dataset, val_dataset, test_dataset = dataset.build()

# train and val data loaders
train_dataloader = train_dataset.shuffle(20).batch(32).prefetch(5) # see tf.data.Dataset for more options
val_dataloader   = val_dataset.batch(32)

# test data set is built per video, so load differently
test_dataloaders = []
for video_dataset in test_dataset:
  test_dataloader = video_dataset.batch(32).prefetch(5)
  test_dataloaders.append(test_dataloader)

print('123')
print(train_dataset)