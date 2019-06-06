import spell.client
client = spell.client.from_environment()


LABEL="number-recognition"

# r1=client.runs.new(machine_type="K80", commit_label="main", command="python fetch_data.py")
# r1.wait_status(client.runs.COMPLETE)
# r2=client.runs.new(machine_type="K80", command="python mnist/main.py", commit_label=LABEL)
# print("waiting for run {} to finish".format(r1.id))
# r2.wait_status(client.runs.COMPLETE)

r=client.runs.new(machine_type="K80", command="python vae/main.py",
attached_resources={"runs/291/data", commit_label=LABEL)
