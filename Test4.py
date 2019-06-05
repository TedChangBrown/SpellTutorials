import spell.client
r=client.runs.new(command="testfiles/random.sh")
r.wait_status(client.runs.COMPLETE)
