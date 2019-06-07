import spell.client
import argparse

DEFAULT_TRANSFER_PHOTO= "images/input/example-style-transfer.jpg"
DEFAULT_TRANSFER_STYLE= "images/input/example-style.jpg"
STYLE_TRANSFER_LABEL="StyleTransfer"
p = argparse.ArgumentParser()
p.add_argument("--transfer_photo", default=DEFAULT_TRANSFER_PHOTO, help="Path to input photo (must be comitted to fast-style-transfer repo)")
p.add_argument("--transfer_style", default=DEFAULT_TRANSFER_STYLE, help="Path to input stylke (must be comitted to fast-style-transfer repo)")
args = p.parse_args()

pip_packages= ["moviepy"]
apt_packages=["ffmpeg"]

client=spell.client.from_environment()

r=client.runs.new(commit_label="StyleTransfer", command="./setup.sh")
r.wait_status(client.runs.COMPLETE)

r=client.runs.new(attached_resources={"runs/{}/data".format(r.id):"datasets"},framework="tensorflow",
pip_packages=pip_packages, apt_packages=apt_packages,machine_type="V100",
command="python style.py --checkpoint-dir ckpt --style {} --style-weight 1.5e2 --train-path datasets/train2014 --vgg-path datasets/imagenet-vgg-verydeep-19.mat".format(args.transfer_style)
