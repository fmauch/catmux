Hello there,

you just started the catmux example. This launched a tmux shell with a lot of open windows.
If you know your way around tmux, have fun :)
If you dont know tmux very well, have a look at this tutorial:
In this tmux config mouse mode is enabled, so you should be able to scroll with the mouse and select splits and tabs with the mouse. The tabbar is at the bottom, btw.
For your convenience, we defined a couple of key mappings:

    ALT-<Arrow-keys>         navigate around splits (Called panes in tmux)
    CTRL-<PageUp/PageDown>   toggle through tabs (Called windows in tmux)
    CTRL-b, d                detach from current session (this keeps everything running)
                             (Press CTRL-b, release both and then press d)
    CTRL-b, SHIFT-k          Kill the complete session
