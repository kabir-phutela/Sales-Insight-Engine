# main_pipeline.py

import subprocess
import sys
import os

def run_script(script_path):
    """
    Helper function to execute a Python script in a subprocess.
    """
    print(f"\n🚀 Running script: {script_path}")
    result = subprocess.run(
        [sys.executable, script_path],
        capture_output=True,
        text=True
    )
    print(result.stdout)
    if result.stderr:
        print(f"⚠️ Errors:\n{result.stderr}")

if __name__ == "__main__":
    print("🔹 Starting Stock Management Data Pipeline...")

    # Paths to your pipeline scripts
    pipeline_dir = os.path.join("pipeline")

    weather_script = os.path.join(pipeline_dir, "weather_collector.py")
    holiday_script = os.path.join(pipeline_dir, "holiday_collector.py")
    trend_script = os.path.join(pipeline_dir, "trend_collector.py")
    merge_script = os.path.join(pipeline_dir, "merge_features.py")

    # 1. Fetch Weather Data
    run_script(weather_script)

    # 2. Fetch Holiday Data
    run_script(holiday_script)

    # 3. Fetch Trend Data
    run_script(trend_script)

    # 4. Merge Data
    run_script(merge_script)

    print("\n✅ All pipeline steps completed successfully.")
