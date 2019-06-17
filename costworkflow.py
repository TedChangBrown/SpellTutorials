import spell.client
client = spell.client.from_environment()

r=client.runs.new(command="echo hello", machine_type="K80")
r.wait_status(client.runs.COMPLETE)
r=client.runs.new(command="echo goodbye", machine_type="V100")
r.wait_status(client.runs.COMPLETE)
