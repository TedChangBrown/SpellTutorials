import spell.client
import argparse

DEFAULT_TRANSFER_PHOTO= "images/input/example-style-transfer.jpg"
DEFAULT_TRANSFER_STYLE= "images/input/example-style.jpg"
STYLE_TRANSFER_LABEL="StyleTransfer"
p = argparse.ArgumentParser()
p.add_argument("--transfer-photo", default=DEFAULT_TRANSFER_PHOTO, help="Path to input photo (must be comitted to fast-style-transfer repo)")
p.add_argument("--transfer-style", default=DEFAULT_TRANSFER_STYLE, help="Path to input stylke (must be comitted to fast-style-transfer repo)")
args = p.parse_args()

client=spell.client.from_environment()

r=client.runs.new(commit_label="StyleTransfer", command="ls")
