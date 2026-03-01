import os

input_file = 'input.txt'
output_file = 'output.txt'

if not os.path.exists(input_file):
    print(f"Error: {input_file} not found!")
else:
    with open(input_file, 'r', encoding='utf-8') as infile, \
         open(output_file, 'w', encoding='utf-8') as outfile:
        
        for line in infile:
            if not line.strip().startswith("Target"):
                outfile.write(line)
                continue
            
            parts = line.split()
            
            if len(parts) > 12:
                prev_link = parts[11]
                next_link = parts[12]

                # Skip sustain tail
                if prev_link != "0" and "." not in prev_link:
                    continue
                
                # Clear W-note flags
                parts[8] = "0"
                parts[9] = "0"

                # Convert sustain head to hold note
                if prev_link == "0" and next_link != "0" and "." not in next_link:
                    parts[5] = "1"
                    parts[11] = "0"
                    parts[12] = "0"

            outfile.write(" ".join(parts) + "\n")

    print(f"Done! Chart fixed and saved to {output_file}")