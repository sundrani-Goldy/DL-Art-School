transcriptions = ""
dataset_path = "/home/ubuntu/Testing/DL-Art-School/datasets"

for stage in ["train", "eval"]:
    with open(f'{dataset_path}/{stage}.txt') as f:
        for line in f.readlines():
            transcriptions += ' ' + line.split("|")[1].strip()

with open("transcriptions.txt", "w") as f:
  f.write(transcriptions.strip())