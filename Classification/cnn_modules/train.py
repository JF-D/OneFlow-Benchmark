import oneflow as flow
import oneflow_api

import numpy as np
import cv2
import time
import argparse
from PIL import Image
import torch

from models.resnet50 import resnet50
from utils.imagenet1000_clsidx_to_labels import clsidx_2_labels
from oneflow.python.framework.function_util import global_function_or_identity

def _parse_args():
    parser = argparse.ArgumentParser("flags for save style transform model")
    parser.add_argument(
        "--model_path", type=str, default="./resnet50-19c8e357.pth", help="model path"
    )
    parser.add_argument(
        "--image_path", type=str, default="./data/fish.jpg", help="input image path"
    )
    return parser.parse_args()

def load_image(image_path='data/tiger.jpg'):
    rgb_mean = [123.68, 116.779, 103.939]
    rgb_std = [58.393, 57.12, 57.375]
    im = Image.open(image_path)
    im = im.resize((224, 224))
    im = im.convert('RGB')  # 有的图像是单通道的，不加转换会报错
    im = np.array(im).astype('float32')
    im = (im - rgb_mean) / rgb_std
    im = np.transpose(im, (2, 0, 1))
    im = np.expand_dims(im, axis=0)
    return np.ascontiguousarray(im, 'float32')

def main(args):
    flow.env.init()
    flow.enable_eager_execution()

    start_t = time.time()
    res50_module = resnet50()
    dic = res50_module.state_dict()
    end_t = time.time()
    print('init time : {}'.format(end_t - start_t))

    # start_t = time.time()
    # torch_params = torch.load(args.model_path)
    # torch_keys = torch_params.keys()

    # for k in dic.keys():
    #     if k in torch_keys:
    #         dic[k] = torch_params[k].detach().numpy()
    # res50_module.load_state_dict(dic)
    # end_t = time.time()
    # print('load params time : {}'.format(end_t - start_t))

    start_t = time.time()
    image = load_image(args.image_path)
    image = flow.Tensor(image)

    label = flow.Tensor([1], dtype=flow.int32, requires_grad=False)

    corss_entropy = flow.nn.CrossEntropyLoss()
    logits = res50_module(image)
    
    # TODO
    # loss = corss_entropy(logits, label)
    
    # TODO
    # grad = flow.Tensor(1, 1000)
    # grad.determine()
    # logits.backward(grad)

    predictions = logits.softmax()
    
    predictions = predictions.numpy()
    end_t = time.time()
    print('infer time : {}'.format(end_t - start_t))
    clsidx = np.argmax(predictions)
    print("loss: %f, predict prob: %f, class name: %s" % (loss.numpy(), np.max(predictions), clsidx_2_labels[clsidx]))

if __name__ == "__main__":
    args = _parse_args()
    main(args)





















# train_batch_size = 1
# train_record_reader = flow.nn.OfrecordReader("./ofrecord_224/train",
#                         batch_size=train_batch_size,
#                         data_part_num=1,
#                         part_name_suffix_length=5,
#                         random_shuffle=False,
#                         shuffle_after_epoch=False)
# record_label_decoder = flow.nn.OfrecordRawDecoder("class/label", shape=(), dtype=flow.int32)
# color_space = 'RGB'
# height = 224
# width = 224
# channels = 3
# record_image_decoder = flow.nn.OfrecordRawDecoder("encoded", shape=(height, width, channels), dtype=flow.uint8)
# flip = flow.nn.CoinFlip(batch_size=train_batch_size)
# rgb_mean = [123.68, 116.779, 103.939]
# rgb_std = [58.393, 57.12, 57.375]
# crop_mirror_norm = flow.nn.CropMirrorNormalize(color_space=color_space, output_layout="NCHW",
#                                             mean=rgb_mean, std=rgb_std, output_dtype=flow.float)
# rng = flip()

# images = []
# for i in range(10):
#     start = time.time()
#     train_record = train_record_reader()
#     label = record_label_decoder(train_record)
#     image_raw_buffer = record_image_decoder(train_record)
#     image = crop_mirror_norm(image_raw_buffer, rng)
#     print(image.shape, time.time() - start)

#     # recover images
#     image_np = image.numpy()
#     images.append(image_np.copy())
#     image_np = np.squeeze(image_np)
#     image_np = np.transpose(image_np, (1, 2, 0))
#     image_np = image_np * rgb_std + rgb_mean
#     image_np = cv2.cvtColor(np.float32(image_np), cv2.COLOR_RGB2BGR)
#     image_np = image_np.astype(np.uint8)
#     print(image_np.shape)
#     cv2.imwrite("recover_image%d.jpg" % i, image_np)

# for i in range(1, 10):
#     print(np.allclose(images[0], images[i]))




