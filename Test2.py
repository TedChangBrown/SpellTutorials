import spell.client
client = spell.client.from_environment()

ppackages = ["scikit-image","numpy","matplotlib","scipy"]
apackages = ["python-tk"]

r1=client.runs.new(github_url="https://github.com/richzhang/colorization", command="colorization/models/fetch_release_models.sh")
r1.wait_status(client.runs.COMPLETE)

r2=client.runs.new(github_url="https://github.com/richzhang/colorization",
pip_packages=ppackages, apt_packages=apackages,attached_resources={"runs/{}/models".format(r1.id):"/mnt/models"},framework="caffe",
machine_type="K80",
command="python colorization/colorize.py -img_in ./demo/imgs/ansel_adams3.jpg -img_out ./output.png --caffemodel /mnt/models/colorization_release_v2.caffemodel")
r2.wait_status(client.runs.COMPLETE)
r2.cp(source_path="output.png", destination_directory=None)
r3=client.run.new(command="cp output.png ./tutorial_outputs")
