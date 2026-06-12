# main_pipeline.py

import subprocess
import sys
import os

def run_script(script_path):
    """
    Run a Python script and print stdout/stderr.
    """
    print(f"\nRunning script: {script_path}")
    result = subprocess.run([sys.executable, script_path], capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print(f"Errors:\n{result.stderr}")

if __name__ == "__main__":
    print("Starting Stock Management Retraining Pipeline...")

    # -----------------------------
    # Absolute path handling
    # -----------------------------
    script_dir = os.path.dirname(os.path.abspath(__file__))  # directory of main_pipeline.py
    pipeline_dir = os.path.join(script_dir, "pipeline")
    retrain_script = os.path.join(pipeline_dir, "retraining_model.py")

    print("Looking for retraining script at:", retrain_script)

    if not os.path.exists(retrain_script):
        raise FileNotFoundError(f"Retraining script not found at {retrain_script}")

    # -----------------------------
    # Run retraining
    # -----------------------------
    run_script(retrain_script)

    print("\nModel retraining completed successfully.")
