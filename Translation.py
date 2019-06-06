import spell.client
client=spell.client.from_environment()

LABEL="translation"

r=client.runs.new(command="nmt/scripts/download_iwslt15.sh nmt_data",commit_label=LABEL)
r.wait_status(client.runs.COMPLETE)

r=client.runs.new(attached_resources={"runs/{}/nmt_data".format(r.id):"nmt_data"},
commit_label=LABEL, machine_type="K80",
command="mkdir nmt_model && export PYTHONIOENCODING=UTF-8 && python -m nmt.nmt  --src=vi --tgt=en --vocab_prefix=nmt_data/vocab  --train_prefix=nmt_data/train --dev_prefix=nmt_data/tst2012  --test_prefix=nmt_data/tst2013 --out_dir=nmt_model --num_train_steps=12000 --steps_per_stats=100 --num_layers=2 --num_units=128 --dropout=0.2 --metrics=bleu")
r.wait_status(client.runs.COMPLETE)
