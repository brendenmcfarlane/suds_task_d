from pathlib import Path
from datasets import load_dataset
import random
import json

val_dataset = load_dataset("HuggingFaceM4/ChartQA", split="val")

output_dir = Path("datasets/chartqa/tuning_images")
git_hub_path = "https://raw.githubusercontent.com/brendenmcfarlane/suds_task_d/main/"
output_dir.mkdir(exist_ok=True)
json_path = "datasets/chartqa/tuning_questions.json"

random.seed(42)

# Original indices
indices = random.sample(range(len(val_dataset)), 10)

# Select those examples
samples = val_dataset.select(indices)
json_samples = []


for original_idx, sample in zip(indices, samples):
    sample["image"].save(output_dir / f"query_{original_idx}.png")
    question = sample["query"]
    answer = sample["label"][0]
    dataset = "ChartQA Validation split"
    image_url = f"{git_hub_path}{output_dir}/query_{original_idx}.png"
    json_samples.append({"question": question,
                         "answer": answer,
                         "dataset": dataset,
                         "image_url": image_url})

with open(json_path, "w") as f:
    json.dump(json_samples, f, indent=4)
# TODO: write questions to .json



# dataset = load_dataset("HuggingFaceM4/ChartQA")

# output_dir = Path("selected_charts")
# output_dir.mkdir(exist_ok=True)

# indices = [i for i in range(6)]

# for i in indices:
#     example = dataset["train"][i]
#     example["image"].save(output_dir / f"chart_{i}.png")
