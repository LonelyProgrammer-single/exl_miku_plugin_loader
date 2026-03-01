import os
import re
import glob

OUTPUT_FILENAME = "mdata_pv_db.txt"

def merge_pv_databases_lexicographical():
    database = {}
    
    pv_id_pattern = re.compile(r'^pv_(\d+)')

    files = glob.glob("*.txt")
    
    print(f"Found files: {len(files)}")
    print("-" * 65)
    print(f"{'FILENAME':<25} | {'SONGS (IDs)':<11} | {'RANGE (Min - Max)'}")
    print("-" * 65)

    total_songs_count = 0 
    all_seen_ids = set()

    for file_path in files:
        if file_path == OUTPUT_FILENAME:
            continue
            

        unique_ids_in_file = set() 
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
                
            pending_lines = []
            
            for line in lines:
                if not line.endswith('\n'):
                    line += '\n'

                match = pv_id_pattern.match(line)
                
                if match:
                    pv_id_str = match.group(1)
                    
                    unique_ids_in_file.add(int(pv_id_str))
                    all_seen_ids.add(int(pv_id_str))
                    
                    if pending_lines:
                        if pv_id_str not in database:
                            database[pv_id_str] = []
                        database[pv_id_str].extend(pending_lines)
                        pending_lines = []
                    
                    if pv_id_str not in database:
                        database[pv_id_str] = []
                    database[pv_id_str].append(line)
                else:
                    pending_lines.append(line)
            
            # Статистика по текущему файлу
            count = len(unique_ids_in_file)
            total_songs_count += count
            
            if count > 0:
                min_id = min(unique_ids_in_file)
                max_id = max(unique_ids_in_file)
                range_str = f"{min_id} - {max_id}"
            else:
                range_str = "No IDs"
                
            print(f"{file_path:<25} | {count:<11} | {range_str}")

        except Exception as e:
            print(f"Error reading file {file_path}: {e}")

    sorted_ids = sorted(database.keys())
    final_unique_count = len(sorted_ids)
    
    print("-" * 65)
    print(f"STATISTICS:")
    print(f"Total songs found (sum):  {total_songs_count}")
    print(f"Total unique songs saved: {final_unique_count}")
    
    if total_songs_count != final_unique_count:
        print(f"NOTE: {total_songs_count - final_unique_count} songs were duplicates across files (merged).")
    print("-" * 65)

    print(f"Writing to {OUTPUT_FILENAME}...")

    try:
        with open(OUTPUT_FILENAME, 'w', encoding='utf-8') as f:
            for pv_id in sorted_ids:
                for line in database[pv_id]:
                    f.write(line)
        print("Done.")
        
    except Exception as e:
        print(f"Error writing file: {e}")

if __name__ == "__main__":
    merge_pv_databases_lexicographical()
    input("\nPress Enter to exit...")