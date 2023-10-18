import sys

sys.path.append("../")
from source.core import stable_diffusion, s3

text = "/prompt send a horse"
text = text.lower()


check = text.startswith("/prompt")

print(check)
prompt = text.replace("/prompt", "").strip()
print(prompt)
