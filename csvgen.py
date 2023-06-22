import csv
import json

header = ["filename", "cell_type", "xmin", "xmax", "ymin", "ymax"]
filename = "test.csv"

with open(filename, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(header)


filename = "astra-fass/training/info.labels"

with open(filename, "r") as file:
    data = json.load(file)

paths = []
for file_data in data["files"]:
    path = file_data["path"]
    paths.append(path)

bboxes = []
for file_data in data["files"]:
    bbox = file_data["boundingBoxes"]
    bboxes.append(bbox)

# Print the extracted paths
for path in paths:
    print(path)

for box in bboxes:
    print(box)
    print(len(box))

print("\n\n\n\n\n")

print(len(paths))
print(len(bboxes))






filename = "test.csv"

new_lines = []

for i in range(len(paths)):
    for j in bboxes[i]:

    #for j in range(len(bboxes[i])):
        tmp=[]
        tmp.append(paths[int(i)])
        tmp.append(j["label"])
        tmp.append(j["x"])
        tmp.append(j["x"]+j["width"])
        tmp.append(j["y"])
        tmp.append(j["y"]+j["height"])


        new_lines.append(tmp)

# Open the CSV file in append mode
with open(filename, 'a', newline='') as file:
    writer = csv.writer(file)
    # Write each new line to the file
    for line in new_lines:
        writer.writerow(line)