import spell.client
client = spell.client.from_environment()
#r=client.runs.new(command="ls")
r=client.runs.new(command="python ./print.py")
