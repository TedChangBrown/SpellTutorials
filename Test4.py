import spell.client
client.spell.client.from_environment()
r=client.runs.new(command="testfiles/random.sh")
r.wait_status(client.runs.COMPLETE)
