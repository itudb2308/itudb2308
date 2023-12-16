import os
import autopep8


def format_python_files(directory="./src"):
    for root, dirs, files in os.walk(directory):
        if 'env' not in root:
            for file in files:
                if file.endswith(".py"):
                    file_path = os.path.join(root, file)
                    print(f"Formatting: {file_path}")
                    with open(file_path, "r", encoding="utf-8") as f:
                        code = f.read()
                    formatted_code = autopep8.fix_code(code, options={"max_line_length": 10000000})
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(formatted_code)


if __name__ == "__main__":
    format_python_files()
