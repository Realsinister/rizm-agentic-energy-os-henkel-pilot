"""
Master Automated Pipeline Orchestrator for Sample Energy OS.
Executes data generation, validation, optimization, sensitivity sweeps, unit tests, and audit logging.
"""

import sys
import subprocess
import os

# Set UTF-8 encoding for stdout on Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

def run_command(command: str) -> bool:
    print(f"\n[PIPELINE EXECUTOR] Running: {command}")
    env = os.environ.copy()
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    sys_path = r"C:\Users\yashg\AppData\Roaming\Python\Python314\site-packages"
    env["PYTHONPATH"] = f"{root_dir};{sys_path}"
    result = subprocess.run(command, shell=True, env=env)
    return result.returncode == 0

def main():
    print("==================================================================")
    print("SAMPLE ENERGY OS -- FULL AUTOMATED PIPELINE EXECUTION")
    print("==================================================================")
    
    # Step 1: Run Unit Test Verification Suite
    print("\n---> STEP 1: Running Automated Pytest Verification Suite")
    if not run_command("python -m pytest tests/test_suite.py -v"):
        print("PIPELINE FAILED AT STEP 1 (Unit Tests Failed)")
        sys.exit(1)
        
    # Step 2: Run Reusable CLI Pipeline with Sensitivity Sweep
    print("\n---> STEP 2: Running Sample Energy OS CLI Site Pipeline & Sensitivity Engine")
    if not run_command("python -m src.sample_energy_os --config site_config.json --run-sensitivity"):
        print("PIPELINE FAILED AT STEP 2 (CLI Execution Failed)")
        sys.exit(1)
        
    print("\n==================================================================")
    print("ALL PIPELINE CHECKS PASSED PERFECTLY. SYSTEM READY.")
    print("==================================================================")

if __name__ == "__main__":
    main()
