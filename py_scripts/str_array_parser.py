import os
import re
import glob

OUTPUT_FILENAME = "mod_str_array.toml"

def prefix_sort_key(prefix):
    if not prefix:
        return (0, "", 0, "")
    
    parts = prefix.split('.')
    lang = parts[0] if len(parts) > 1 else ""
    cat = parts[-1]
    
    lang_weight = 0 if not lang else 1
    cat_weight = 0 if cat == "module" else 1 
    
    return (lang_weight, lang, cat_weight, cat)

def merge_str_arrays():
    database = {}
    kv_pattern = re.compile(r'^([a-zA-Z0-9_.]+)\s*=')

    files =[]
    for ext in ("*.toml", "*.txt"):
        files.extend(glob.glob(ext))
        
    excludes = {OUTPUT_FILENAME, "mdata_pv_db.txt"}
    files =[f for f in files if f not in excludes]
    
    print(f"Found files: {len(files)}")
    print("-" * 65)
    print(f"{'FILENAME':<25} | {'ITEMS':<11} | {'CATEGORIES'}")
    print("-" * 65)

    total_items_count = 0 
    global_unique_items = set()

    for file_path in files:
        items_in_file = set()
        categories_in_file = set()
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
                
            pending_lines =[]
            
            for line in lines:
                line_stripped = line.strip()
                
                if not line_stripped or line_stripped.startswith('#'):
                    pending_lines.append(line.rstrip('\n'))
                    continue
                    
                match = kv_pattern.match(line_stripped)
                if match:
                    full_key = match.group(1)
                    line_to_save = line.rstrip('\n')
                    
                    # Fix explicit 'en.' prefix to match the default format
                    if full_key.startswith('en.'):
                        full_key = full_key[3:]
                        line_to_save = re.sub(r'^\s*en\.', '', line_to_save)
                    
                    parts = full_key.split('.')
                    
                    item_id = int(parts[-1]) if parts[-1].isdigit() else parts[-1]
                    category = parts[-2] if len(parts) >= 2 else "root"
                    prefix = '.'.join(parts[:-1])
                        
                    items_in_file.add((category, item_id))
                    global_unique_items.add((category, item_id))
                    categories_in_file.add(category)
                    
                    if prefix not in database:
                        database[prefix] = {}
                        
                    # Overwrite duplicates
                    database[prefix][item_id] = pending_lines + [line_to_save]
                    pending_lines =[]
                else:
                    pending_lines.append(line.rstrip('\n'))
            
            if pending_lines:
                if "" not in database:
                    database[""] = {}
                if "EOF" not in database[""]:
                    database[""]["EOF"] = []
                database[""]["EOF"].extend(pending_lines)
            
            count = len(items_in_file)
            total_items_count += count
            
            cat_str = ", ".join(sorted(categories_in_file))
            if len(cat_str) > 22:
                cat_str = cat_str[:19] + "..."
            if not cat_str:
                cat_str = "None"
                
            print(f"{file_path:<25} | {count:<11} | {cat_str}")

        except Exception as e:
            print(f"Error reading file {file_path}: {e}")

    sorted_prefixes = sorted(database.keys(), key=prefix_sort_key)
    final_unique_items = len(global_unique_items)
    
    print("-" * 65)
    print("STATISTICS:")
    print(f"Total items found:  {total_items_count}")
    print(f"Total unique items: {final_unique_items}")
    
    if total_items_count != final_unique_items:
        print(f"NOTE: {total_items_count - final_unique_items} items were duplicates across files (overwritten).")
    print("-" * 65)

    print(f"Writing to {OUTPUT_FILENAME}...")

    try:
        with open(OUTPUT_FILENAME, 'w', encoding='utf-8') as f:
            for prefix in sorted_prefixes:
                items = database[prefix]
                
                def id_sort_key(k):
                    return (0, k) if isinstance(k, int) else (1, k)
                
                sorted_ids = sorted(items.keys(), key=id_sort_key)
                
                for item_id in sorted_ids:
                    for line in items[item_id]:
                        f.write(line + "\n")
                        
        print("Done.")
        
    except Exception as e:
        print(f"Error writing file: {e}")

if __name__ == "__main__":
    merge_str_arrays()
    input("\nPress Enter to exit...")