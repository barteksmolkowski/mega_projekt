import os
import sys

from preprocessing import ImageDataPreprocessing


def check_dependencies():
    needed = {"numpy": "numpy", "PIL": "pillow", "matplotlib": "matplotlib"}
    missing = [pip_name for imp_name, pip_name in needed.items() if not __import_check(imp_name)]
    if missing:
        print(f"\n[!!!] BRAK: {', '.join(missing)} | Komenda: pip install {' '.join(missing)}")
        sys.exit(1)

def __import_check(name):
    try:
        __import__(name)
        return True
    except ImportError:
        return False

def main():
    input_path = "data/input_images"
    
    if not os.path.exists(input_path):
        os.makedirs(input_path)
        print(f"[*] Stworzono folder: {input_path}. Wrzuć tam zdjęcia!")

    preprocessor = ImageDataPreprocessing()

    if len(sys.argv) > 1:
        image_path = sys.argv[1]
        preprocessor.preprocess(image_path)
    else:
        print("[INFO] Brak pliku wejściowego. Uruchamiam test integracyjny...")
        preprocessor.preprocess("dry_run_test", test_mode=True)

if __name__ == "__main__":
    check_dependencies()
    main()