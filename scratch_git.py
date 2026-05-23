import subprocess

def run():
    print("=== GIT STATUS ===")
    res_status = subprocess.run(["git", "status"], capture_output=True, text=True)
    print(res_status.stdout)
    print(res_status.stderr)

    print("\n=== GIT LOG ===")
    res_log = subprocess.run(["git", "log", "-n", "5", "--oneline"], capture_output=True, text=True)
    print(res_log.stdout)
    print(res_log.stderr)

if __name__ == '__main__':
    run()
