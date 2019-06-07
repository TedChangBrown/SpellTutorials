import argparse
import spell.client

DEFAULT_COLORIZER_PHOTO = "ansel_adams3.jpg"

p = argparse.ArgumentParser()
p.add_argument("--photo", default=DEFAULT_COLORIZER_PHOTO, help="Name of input photo (must be comitted to colorization/demo/images)")

args = p.parse_args()
client=spell.client.from_environment()

colorizer_run(client, "./demo/imgs/"+args.photo)


def colorizer_run(client, photo_path):
    ppackages = ["scikit-image","numpy","matplotlib","scipy"]
    apackages = ["python-tk"]

    r1=client.runs.new(commit_label="colorizer",command="colorization/models/fetch_release_models.sh")
    r1.wait_status(client.runs.COMPLETE)

    r2=client.runs.new(commit_label="colorizer",pip_packages=ppackages, apt_packages=apackages,attached_resources={"runs/{}/models".format(r1.id):"/mnt/models"},framework="caffe",
    machine_type="K80",
    command="python colorization/colorize.py -img_in {} -img_out ./output.png --caffemodel /mnt/models/colorization_release_v2.caffemodel".format(photo_path))
    r2.wait_status(client.runs.COMPLETE)
