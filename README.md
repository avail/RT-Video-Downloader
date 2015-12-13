# The RT Video Downloader
This is a python script that allows for easier downloading of videos from RT. To be able to use this script, you'll need <a href="https://www.python.org/">python 3+</a>

<h1>
Multithreaded Download:
</h1>

<b>
WIFI (110 .ts files, 706 MB total)
</b>
<ul>
<li>1 thread : 4.81 min</li>
<li>2 threads: 4.50 min</li>
<li>4 threads: 4.53 min</li>
</ul>
<b>
ETHERNET (same 110 files)
</b>
<ul>
<li>1 thread : 18 sec</li>
<li>2 threads: 13 sec</li>
<li>4 threads: 11 sec</li>
</ul>
Initial tests prove method works, however the speed increase is minimal at best. The bottleneck of download speeds with this tool is definitely the network.
