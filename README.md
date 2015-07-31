# The RT Video Downloader
This is a python script I made that allows for easier downloading of videos from <a href="http://roosterteeth.com">roosterteeth.com</a>. To be able to use this script, you'll need <a href="https://www.python.org/">python</a> 3.4.3.
<h2>Background</h2>
Videos on the new RoosterTeeth website (20 / 7 / 2015 onwards) are devided up into many 1 seconds long <a href="https://en.wikipedia.org/wiki/MPEG_transport_stream">Mpeg .ts</a> files, which is pretty wierd, and annoying to download manually because there could be thousands of files. Luckily, these are references by <a href="https://en.wikipedia.org/wiki/M3U">m3u8</a> playlist files, which are what this script uses to download videos.
<h2>Usage</h2>
To download a video, press 'd' on the options menu, and enter in the url of the page of the video. The program will scan the contents of this page for a link to an aforementioned index.m3u8 file and download it. It should then print out the contents of this index playlist:

![the index.m3u8 in python](https://cloud.githubusercontent.com/assets/13566135/8977656/3068e8ee-36ef-11e5-9411-331119d0365d.png)

You can now enter in which resolution playlist you want to load. It then fetches the download links and gives you the options to download the files with python and create a text file of the links (it will create a folder called 'links' for this) in case you want to download them with a download manager. Either way, once the .ts files have been downloaded into a folder in 'downloads', <a href="https://www.bunkus.org/videotools/mkvtoolnix/">mkvmerge</a> can be used to mux them all into a .mkv file by pressing 'm' on the main menu:

![mkvmerge running in command prompt](https://cloud.githubusercontent.com/assets/13566135/8977947/ca7e3194-36f1-11e5-937c-861846592bcc.png)

If you want to download a video that is subscribers-only, don't worry. You'll need someone who has access to the video to send the url of the index file to you, after which you can download the files by pressing 'i' on the main menu.

<h2>To-Do</h2>

The things I have planned are:

<ul>
<li>To get python to download the .ts files in parallel (so its atleast comparable to a download manager).</li>
<li>To create a nice looking GUI and stand-alone executables for each platform.</li>
</ul>
