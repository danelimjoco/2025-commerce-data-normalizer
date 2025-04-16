import sys
import json
from normalizer.normalizer import normalize

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python main.py <platform> <data_file>")
        sys.exit(1)

    platform = sys.argv[1]
    filepath = sys.argv[2]

    try:
        unified = normalize(platform, filepath)
        print(json.dumps(unified, indent=2))
    except Exception as e:
        print(f"Error: {e}")