import spell.client
r=client.runs.new(command="random.sh")
r.wait_status(client.runs.COMPLETE)
