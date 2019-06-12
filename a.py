import spell.client

client = spell.client.from_environment()

r=client.runs.new(commit_label="test", command="echo hello world")
