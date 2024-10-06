# optimal_scheduler
![](https://github.com/gruvian/optimalScheduler/blob/main/logoLight.png) <br />
Icon source:
<a href="https://www.flaticon.com/free-icons/schedule" title="schedule icons">Schedule icons created by Senapedia - Flaticon</a>
<br /> Optimal Scheduler is a GUI application for automated creation of an optimal weekly work and study schedule. <br /> <br />
## Installation on Linux

If you want to run the tool as a desktop application, clone the git repository and run ./install.sh. 

```shell
git clone https://github.com/gruvian/optimal_scheduler
cd optimal_scheduler
chmod +x "install.sh"
./install.sh
```

For uninstalling, run ./uninstall.sh.

```shell
cd optimal_scheduler
chmod +x "uninstall.sh"
./uninstall.sh
```

### Built in
Python

### Prerequisites
python3, PyQt5, matplotlib

### Implementation
Greedy algorithm solution <br />
Weight adjustion per self-reported difficulty of task and past perfromance on similar tasks <br />
Dynamic data storage in JSON
