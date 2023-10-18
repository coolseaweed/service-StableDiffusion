import sys

sys.path.append("../")
from source.core import stable_diffusion, s3

print(sys.path)
prompt = "a surfer is riding a horse on the beach"


grid = stable_diffusion.create_image(prompt)
grid.save("temp.png")
