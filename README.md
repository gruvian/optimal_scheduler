# optimal_scheduler
![](https://github.com/gruvian/optimalScheduler/blob/main/logoLight.png) <br />
Icon source:
<a href="https://www.flaticon.com/free-icons/schedule" title="schedule icons">Schedule icons created by Senapedia - Flaticon</a>
<br /> Optimal Scheduler is a simple productivity project developed for creating an optimal weekly schedule that maximizes productivity by automatically creating a work and study schedule. This project was created as a personal project. <br /> <br />
## Installation on Debian distros

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
Greedy algorithm solution per <a href="https://en.wikipedia.org/wiki/Activity_selection_problem">Activity selection problem</a> <br />
Weight adjustion per self-reported difficulty of task and past perfromance on similar tasks <br />
Data stored in JSON
