AdbPaste
========

uses the Android adb tool to send input. StdIn will be massaged to go trhu all the hops adb uses unchanged. Require python, but after that, it's as cross-platform as it goes, while using adb directly, you will have problems like not being able to send spaces in windows.

![screenshot1](https://raw.github.com/gcb/AdbPaste/master/screenshot1.py "screenshot 1")

the problem
===========


Can not use spaces in win32. Even with escaping.

```Batchfile
C:\CODE\AdbPaste>adb shell input text "simple test"
Error: Invalid arguments for command: text
usage: input ...
       input text <string>
       input keyevent <key code number or name>
       input [touchscreen|touchpad|touchnavigation] tap <x> <y>
       input [touchscreen|touchpad|touchnavigation] swipe <x1> <y1> <x2> <y2> [d
uration(ms)]
       input trackball press
       input trackball roll <dx> <dy>
```

Can not use bash keywords (i am sure i am using the word wrongly here), without escaping.

```Batchfile
C:\CODE\AdbPaste>adb shell input text "simple("
/system/bin/sh: syntax error: '(' unexpected
```

Can not send a huge string as the emulator timesout and drop much of it.

Solution
========

Converts espaces to its keycode. Escape bash keywords. Break longer strings in smaller groups.




