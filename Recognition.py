import spell.client
client = spell.client.from_environment()


LABEL="number-recognition"

r=client.runs.new(machine_type="K80", command="python mnist/main.py", commit_label=LABEL)
print("waiting for run {} to finish".format(r.id))
r.wait_status(client.runs.COMPLETE)

# r=client.runs.new(machine_type="K80", command="python vae/main.py",
# attached_resources={"runs/{}/data":"".format(r.id)}, commit_label=LABEL)
