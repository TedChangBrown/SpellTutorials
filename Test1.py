import spell.client
client = spell.client.from_environment()

print("Starting Pix2Pix Tutorial Demo")

r1=client.runs.new(commit_label="p2p",command="python tools/download-dataset.py facades")
print("waiting for run {} to complete".format(r1.id))
r1.wait_status(client.runs.COMPLETE)

r2=client.runs.new(attached_resources={"runs/{}/facades".format(r1.id):"/datasets/facades"},
command="python pix2pix.py --mode train --output_dir facades_train --max_epochs 200 --input_dir /datasets/facades/train --which_direction BtoA",
machine_type="K80",
github_url="https://github.com/affinelayer/pix2pix-tensorflow",commit_label="p2p")
print("training in run {}".format(r2.id))
r2.wait_status(client.runs.COMPLETE)

r3=client.runs.new(attached_resources={"runs/{}".format(r1.id):"/datasets", "runs/{}".format(r2.id):"/model"},
command="python pix2pix.py --mode test --output_dir facades_test --input_dir /datasets/facades/val --checkpoint /model/facades_train",
commit_label="p2p")
print("testing in run {}".format(r3.id))
r3.wait_status(client.runs.COMPLETE)
for line in r3.logs():
    print(line)

print("Starting Recolorization Demo")
