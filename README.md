# Catmux

## About
Catmux is a little helper to run a tmux session with multiple windows and panes with just one
command. It is inspired and functionally very similar to
[tmuxinator](https://github.com/tmuxinator/tmuxinator), but without the project management feature
which is in my opinion kind of an overhead.

Session configs can be stored anywhere and have to given as an argument.

## DISCLAIMER - Early package
This package is currently in development phase. It's interface might completely change and/or
functionality might be moved around or even removed without notice. Use it at your own risks and
report issues and problems :)

However, by now it has been used productively in four different projects by different people without
problems, so I would consider it 'working'.

If you try out catmux and you find anything you're missing, anything that doesn't work as expected,
or is clearly a bug, please create an issue here, I'll be happy to answer to them. Of course, merge
requests are always welcome, as well :)

## Motivation
In most of our ROS projects at work we use shell output for almost all nodes to get log information
during runtime. Having all this in one window where you start your "Start it all"-launchfile makes
it very hard to follow the log of a specific node. Starting everything in separate windows is quite
a lot of work and requires documentation overhead in sense of documenting which launchfiles or nodes
have to be started.

At a conference I caught the idea to use tmux scripting to orchestrate all this in one tmux session.
However, quickly I noticed that creating these scripts is a daunting task as you'll have to type in
a lot of commands over and over again and as soon as you wanted to do things a little different such
as not starting a particular launchfile if a certain parameter was set, things got complicated.

I liked the yaml-syntax of [tmuxinator](https://github.com/tmuxinator/tmuxinator), but that tool
didn't quite hit the spot. I wanted to have something that can be easily integrated into a ROS
project and I definitely wanted something that saves the config per project and not all configs at
one central spot on a particular machine.

## Installation
As catmux is designed as a catkin package, simply clone it into your catkin-workspace, build it and
you're done.

## Usage
Currently, there is no full-blown documentation, but the example config file in
`etc/example_session.yaml` gives a detailed insight on possible commands.

### Running the example the most simple way
to simply run the example, type
```
rosrun catmux create_session package://catmux/etc/example_session.yaml
```

To see further options, simply run it with argument `-h`:
```
$ rosrun catmux create_session -h
usage: create_session [-h] [-n SESSION_NAME] [-t TMUX_CONFIG] [-d]
                      [--overwrite OVERWRITE]
                      session_config

Create a new catmux session

positional arguments:
  session_config        Session configuration. Should be a yaml-file.

optional arguments:
  -h, --help            show this help message and exit
  -n SESSION_NAME, --session_name SESSION_NAME
                        Name used for the tmux session
  -t TMUX_CONFIG, --tmux_config TMUX_CONFIG
                        This config will be used for the tmux session
  -d, --detach          Start session in detached mode
  --overwrite OVERWRITE
                        Overwrite a parameter from the session config.
                        Parameters can be specified using a comma-separated
                        list such as '--overwrite param_a=1,param_b=2'.
```

### Full blown example
To make use of all catmux features, run the following example command:
```
rosrun catmux create_session package://catmux/etc/example_session.yaml --tmux_config package://catmux/etc/tmux_default.conf --session_name example_session --overwrite show_layouts=True,replacement_param="new catmux user"
```

### Killing a catmux session
If you are not that familiar with tmux: To kill a session, simply type `tmux kill-session` in any
terminal window. In the `etc/tmux_default.conf` there is a key-binding for that, see
`etc/readme_tmux.txt` for details.

## Usage ROS2
Only available in the ros2 branch of this repository!

### Installation
Very similar to ROS1: simply clone the package into your ROS2-workspace, build it and
you're done.

### Usage (full blown example)
In case you are not in the base directory of your ROS2 workspace while running this command, don't forget to set correct paths!
```
ros2 run catmux create_session $PWD/src/catmux/etc/example_session.yaml --tmux_config $PWD/src/catmux/etc/tmux_default.conf --session_name example_session --overwrite show_layouts=True,replacement_param="new catmux user"
```