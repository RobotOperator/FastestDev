# FastestDev
This repository contains the POC example code for the demonstrations from my talk at Objective by the Sea v9.0 "Fastest Dev: Racing to Steal Credentials". It demonstrates the race condition of a third party process consuming password characters from a TTY device before the intended binary, /usr/bin/sudo. 

The `poc_js_runner.py` is the code that was bundled in RedRacer.app. Link to the presentation and more details pending.

## Dependencies
* Python 3 >= 3.9
* psutil Python module

## Usage
### poc_local_shell.py
1. `python3 ./poc_local_shell.py`
2. In another terminal, type `sudo whoami`
3. Enter your administrator user password
4. View where the POC was run and see that an interactive elevated shell was spawned

### poc_js_runner.py
1. Create a JXA file, `./OBTS_demoScript.js`, you want to be executed with elevated privileges in the same directory as the poc
2. Add a header to the script `#!/usr/bin/osascript -l JavaScript`
3. Set it to executable `chmod +x ./OBTS_demoScript.js`
4. Execute the poc `python3 ./poc_js_runner.py`
5. In another terminal, type `sudo whoami`
6. Enter your administrator user password
7. View the results of execution of `./OBTS_demoScript.js`

### Troubleshooting
If the desired result is not immediately observed, try typing your password a second time in the `sudo` interface and hitting enter. Since this is a race condition, some times `sudo` does consume the first character/get to it first.

If the desired result is still not observed, use `ctrl+c` to stop the POC and `sudo` process, then restart the POC and then re-run `sudo whoami`.

## Additional Info
Try changing the binary to be monitored for in the poc code from `sudo` to `su` or `ssh` and run those commands to switch users or access a remote system in another application with a TTY like XCode or VSCode.
