import argparse
import spell.client
import threading

def colorizer_run(client, photo_path):
    print("Starting Colorzation demo")
    ppackages = ["scikit-image","numpy","matplotlib","scipy"]
    apackages = ["python-tk"]

    r1=client.runs.new(commit_label="colorizer",command="colorization/models/fetch_release_models.sh")
    print("fetching colorzation model in run {}".format(r1.id))
    r1.wait_status(client.runs.COMPLETE)


    r2=client.runs.new(commit_label="colorizer",pip_packages=ppackages, apt_packages=apackages,attached_resources={"runs/{}/models".format(r1.id):"/mnt/models"},framework="caffe",
    machine_type="K80",
    command="python colorization/colorize.py -img_in {} -img_out ./output.png --caffemodel /mnt/models/colorization_release_v2.caffemodel".format(photo_path))
    print("Colorizing photo in run {}".format(r2.id))
    r2.wait_status(client.runs.COMPLETE)
    r2.cp("output.png", "tutorial_outputs/colorizer")

def p2p_runs(client):
    print("Starting Pix2Pix Tutorial Demo")

    r1=client.runs.new(commit_label="p2p",command="python tools/download-dataset.py facades")
    print("Downloading P2P datasets {} to complete".format(r1.id))
    r1.wait_status(client.runs.COMPLETE)

    r2=client.runs.new(attached_resources={"runs/{}/facades".format(r1.id):"/datasets/facades"},
    command="python pix2pix.py --mode train --output_dir facades_train --max_epochs 200 --input_dir /datasets/facades/train --which_direction BtoA",
    machine_type="K80",commit_label="p2p")
    print("training P2P in run {}".format(r2.id))
    r2.wait_status(client.runs.COMPLETE)

    r3=client.runs.new(attached_resources={"runs/{}".format(r1.id):"/datasets", "runs/{}".format(r2.id):"/model"},
    command="python pix2pix.py --mode test --output_dir facades_test --input_dir /datasets/facades/val --checkpoint /model/facades_train",
    commit_label="p2p")
    print("testing P2P in run {}".format(r3.id))
    r3.wait_status(client.runs.COMPLETE)
    r3.cp("facades_test", "tutorial_outputs/p2p")

def recognition_runs(client):
    print("Starting number recognition demo")
    LABEL="number-recognition"

    r1=client.runs.new(machine_type="K80", commit_label="main", command="python fetch_data.py")
    r1.wait_status(client.runs.COMPLETE)

    r2=client.runs.new(machine_type="K80", command="python mnist/main.py", commit_label=LABEL)
    print("waiting for run {} to finish".format(r1.id))
    r2.wait_status(client.runs.COMPLETE)

    r=client.runs.new(machine_type="K80", command="python main.py",cwd="vae",
    attached_resources={"runs/{}/data".format(r1.id):None}, commit_label=LABEL)
    r.wait_status(client.runs.COMPLETE)
    r2.cp("vae", "tutorial_outputs/number_recognition")

def translation_runs(client):
    print("Starting translation demo")
    LABEL="translation"

    r=client.runs.new(command="nmt/scripts/download_iwslt15.sh nmt_data",commit_label=LABEL)
    r.wait_status(client.runs.COMPLETE)

    r2=client.runs.new(attached_resources={"runs/{}/nmt_data".format(r.id):"nmt_data"},
    commit_label=LABEL, machine_type="K80",
    command="mkdir nmt_model && export PYTHONIOENCODING=UTF-8 && python -m nmt.nmt  --src=vi --tgt=en --vocab_prefix=nmt_data/vocab  --train_prefix=nmt_data/train --dev_prefix=nmt_data/tst2012  --test_prefix=nmt_data/tst2013 --out_dir=nmt_model --num_train_steps=12000 --steps_per_stats=100 --num_layers=2 --num_units=128 --dropout=0.2 --metrics=bleu")
    r2.wait_status(client.runs.COMPLETE)

    r3=client.runs.new(attached_resources={"runs/{}/nmt_data".format(r.id):"nmt_data","runs/{}/nmt_model".format(r2.id):"nmt_model_tmp"},
    commit_label=LABEL,
    command="tail -n10 nmt_data nmt_data/tst2013.vi > my_infer_file.vi && cp -r nmt_model_tmp nmt_model && python -m nmt.nmt  --out_dir=nmt_model --inference_input_file=my_infer_file.vi --inference_output_file=output_infer && cat output_infer")
    r3.wait_status(client.runs.COMPLETE)
    r3.cp("output_infer", "tutorial_outputs/translation")

    r4=client.runs.new(attached_resources={"runs/{}/nmt_data".format(r.id):"nmt_data"},
    commit_label=LABEL,
    command="mkdir nmt_model && export PYTHONIOENCODING=UTF-8 && python -m nmt.nmt  --attention=scaled_luong --src=vi --tgt=en --vocab_prefix=nmt_data/vocab  --train_prefix=nmt_data/train --dev_prefix=nmt_data/tst2012  --test_prefix=nmt_data/tst2013 --out_dir=nmt_attention_model --num_train_steps=12000 --steps_per_stats=100 --num_layers=2 --num_units=128 --dropout=0.2 --metrics=bleu")
    r4.wait_status(client.runs.COMPLETE)

    r5=client.runs.new(attached_resources={"runs/{}/nmt_data".format(r.id):"nmt_data","runs/{}/nmt_model".format(r4.id):"nmt_model_tmp"},
    commit_label=LABEL,
    command="tail -n10 nmt_data nmt_data/tst2013.vi > my_infer_file.vi && cp -r nmt_model_tmp nmt_model && python -m nmt.nmt  --out_dir=nmt_model --inference_input_file=my_infer_file.vi --inference_output_file=output_infer && cat output_infer")
    r5.wait_status(client.runs.COMPLETE)
    r5.cp("output_infer", "tutorial_outputs/translation")

DEFAULT_COLORIZER_PHOTO = "ansel_adams3.jpg"

p = argparse.ArgumentParser()
p.add_argument("--photo", default=DEFAULT_COLORIZER_PHOTO, help="Name of input photo (must be comitted to colorization/demo/images)")

args = p.parse_args()
client=spell.client.from_environment()
t1 = threading.Thread(target = colorizer_run, args=(client, "./demo/imgs/"+args.photo))
t2= threading.Thread(target=p2p_runs, args=(client,))
t3 = threading.Thread(target= recognition_runs, args =(client,))
t4 = threading.Thread(target=translation_runs, args = (client,))

t1.start()
t2.start()
t3.start()
t4.start()

t1.join()
t3.join()
t4.join()
t2.join()
