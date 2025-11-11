import os
import subprocess
import tempfile

print("Welcome to Rust Terminal (Python REPL for Rust)!")
print("Type 'exit' to quit.")
print("Type 'run' to compile and execute your code.")
print("---------------------------------------------")

code_lines = []

while True:
    line = input("Rust> ")
    if line.strip().lower() == "exit":
        break
    elif line.strip().lower() == "run":
        if not code_lines:
            print("⚠️ No code to run!")
            continue
        # Remove any leading prompt accidentally copied
        cleaned_code = [l.replace("Rust> ", "") for l in code_lines]

        with tempfile.NamedTemporaryFile(delete=False, suffix=".rs") as tmp_rs:
            tmp_rs.write("\n".join(cleaned_code).encode("utf-8"))
            tmp_rs_path = tmp_rs.name
        exe_path = tmp_rs_path.replace(".rs", ".exe")

        try:
            compile_proc = subprocess.run(["rustc", tmp_rs_path, "-o", exe_path], capture_output=True, text=True)
            if compile_proc.returncode == 0:
                print("✅ Compilation successful!\nRunning program...\n-------------------------")
                subprocess.run([exe_path])
            else:
                print("❌ Compilation failed:\n")
                print(compile_proc.stderr)
        except FileNotFoundError:
            print("⚠️  rustc not found! Make sure Rust is installed and in PATH.")
        finally:
            os.remove(tmp_rs_path)
            if os.path.exists(exe_path):
                os.remove(exe_path)
        code_lines = []
    else:
        code_lines.append(line)
