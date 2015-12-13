# The RT Video Downloader
This is a python script that allows for easier downloading of videos from RT. To be able to use this script, you'll need <a href="https://www.python.org/">python 3+</a>

Multithreaded downloading method:

WIFI (110 .ts files, 706 MB total)

1 thread : 4.81 min
2 threads: 4.50 min
4 threads: 4.53 min

ETHERNET (same 110 files)

1 thread : 18 sec
2 threads: 13 sec
4 threads: 11 sec

Initial tests prove method works, however the speed increase is minimal at best. The bottleneck of download speeds with this tool is definitely the network.
