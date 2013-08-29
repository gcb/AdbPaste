AdbPaste
========

uses the Android adb tool to send input. StdIn will be massaged to go trhu all the hops adb uses unchanged. Require python, but after that, it's as cross-platform as it goes, while using adb directly, you will have problems like not being able to send spaces in windows.

![screenshot1](https://raw.github.com/gcb/AdbPaste/master/screenshot1.png "screenshot 1")

Usage
=====

Note: command line flags must be in order, or feel free to fix :)

--fast Ignores the workaround of breaking up the longer strings into small batches. Works fine for simple inputs. Will fail if used on emulator with fields that do network lookup.

--notab Changes tabs into single spaces

-s Serial number of the device adb should use. Analogous to -s flag of adb (use `adb devices` to see a list). Only needed if more than one device are available.

--file Next argument must be a filename. Content will be sent.

If --file is not used, all the next arguments will be sent


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

Common solution to use a SMS and copy/paste is faster on an actual device, but less practical for running automated tests in the emulator. On automated tests it is easier to wait a few seconds than to deal with application switching and copy paste.

Solution
========

Converts espaces to its keycode. Escape bash keywords. Break longer strings in smaller groups.




