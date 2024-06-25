import json
import os

def generate_txt_files_from_json(json_file_path, output_dir):
    print(f"Opening JSON file: {json_file_path}")
    with open(json_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        print(f"Loaded data from JSON file: {data}")
    
    if not os.path.exists(output_dir):
        print(f"Output directory does not exist. Creating directory: {output_dir}")
        os.makedirs(output_dir)
    else:
        print(f"Output directory already exists: {output_dir}")
    
    for category in ['ATC', 'EXP']:
        print(f"Processing category: {category}")
        for item in data[category]:
            # Extract the numeric part of the id
            numeric_id = int(item['id'].split('_')[1])
            file_name = f"{category}_{numeric_id:03d}.txt"
            file_path = os.path.join(output_dir, file_name)
            print(f"Creating file: {file_path}")
            with open(file_path, 'w', encoding='utf-8') as txt_file:
                for line in item['conversation']:
                    txt_file.write(line + '\n')
                    print(f"Writing line to {file_name}: {line}")

if __name__ == "__main__":
    json_file_path = 'examples/examples.json'
    output_dir = 'examples'
    print(f"Starting the generation of text files from JSON. JSON file path: {json_file_path}, Output directory: {output_dir}")
    generate_txt_files_from_json(json_file_path, output_dir)
    print("Finished generating text files from JSON.")
