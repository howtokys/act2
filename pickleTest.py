import pickle
from typing import Optional
from reading import Reading

errors = 0

def read_pickled_objects(file_name: str) -> int:
    count = 0
    try:
        with open(file_name, "rb") as f:
            while True:
                try:
                    data = pickle.load(f)
                    for item in data:
                        print(item)
                        count += 1
                except EOFError:
                    global errors
                    errors += 1
                    break
    except FileNotFoundError:
        print(f"File {file_name} not found.")
    except Exception as e:
        print(f"Error: {e}")
    return count

def main() -> None:
    total_count = 0
    for i in range(1, 4):
        file_name = f"inventory{i}.pickle"
        print(f"Reading from {file_name}:")
        count = read_pickled_objects(file_name)
        print(f"Number of objects in {file_name}: {count}\n")
        total_count += count

    print(f"Total number of objects: {total_count} and errors: {errors}")

if __name__ == "__main__":
    main()