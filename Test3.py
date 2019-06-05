import spell.client
client = spell.client.from_environment()

r=client.runs.new(command="run mkdir /importantstuff")
#r=client.runs.new(github_url="https://github.com/lengstrom/fast-style-transfer", command="colorization/models/fetch_release_models.sh")
