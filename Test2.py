import argparse
import spell.client

DEFAULT_PHOTO = "./demo/imgs/ansel_adams3.jpg"
p = argparse.ArgumentParser()
p.add_argument("--photo", default=DEFAULT_PHOTO, help="Path to input photo (must be comitted)")
args = p.parse_args()

photo_path = args.photo

client = spell.client.from_environment()

ppackages = ["scikit-image","numpy","matplotlib","scipy"]
apackages = ["python-tk"]

r1=client.runs.new(commit_label="colorizer",command="colorization/models/fetch_release_models.sh")
r1.wait_status(client.runs.COMPLETE)

if photo_path == DEFAULT_PHOTO:
    commit_label = "colorizer"
else:
    commit_label = "main"

r2=client.runs.new(commit_label=commit_label,pip_packages=ppackages, apt_packages=apackages,attached_resources={"runs/{}/models".format(r1.id):"/mnt/models"},framework="caffe",
machine_type="K80",
command="python colorization/colorize.py -img_in {} -img_out ./output.png --caffemodel /mnt/models/colorization_release_v2.caffemodel".format(photo_path))
r2.wait_status(client.runs.COMPLETE)
