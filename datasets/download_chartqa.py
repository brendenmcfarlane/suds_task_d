from pathlib import Path
from datasets import load_dataset

dataset = load_dataset("HuggingFaceM4/ChartQA")

output_dir = Path("selected_charts")
output_dir.mkdir(exist_ok=True)

indices = [i for i in range(6)]

for i in indices:
    example = dataset["train"][i]
    example["image"].save(output_dir / f"chart_{i}.png")