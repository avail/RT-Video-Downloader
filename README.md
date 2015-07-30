# The RT Video Downloader
This is a python script I made that allows for easier downloading of videos from <a href="http://roosterteeth.com">roosterteeth.com</a>. It isn't automatic, but makes things a lot less tedious. To be able to use this script, you'll need <a href="https://www.python.org/">python</a> 3.4.3.
<h2>Background</h2>
Videos on the new RoosterTeeth website (20 / 7 / 2015 onwards) are devided up into many 1 seconds long <a href="https://en.wikipedia.org/wiki/MPEG_transport_stream">Mpeg .ts</a> files, which is pretty wierd, and annoying to download manually because there could be thousands of files. Luckily, these are references by <a href="https://en.wikipedia.org/wiki/M3U">m3u8</a> playlist files, which are what this script uses to download videos.
<h2>Usage</h2>
As I said, this isn't automatic. First you'll need to navigate to the video you want to download, and open up your browsers (preferably Chrome or Firefox) Developer Tools and get to the Network Inspector. When the video loads, you should see some files pop up:

![the network inspector in firefox](https://cloud.githubusercontent.com/assets/13566135/8977294/dca8a832-36eb-11e5-8634-393ca670a0bc.png)

As you can see, it loads an index.m3u8 file, more playlists for each video resolution and .ts files for the current resolution. To download the video, you need to open up the python file in the shell, press 'd' for download files and enter the video name and url of the index.m3u8 file by right-clicking it and copying it. If you opened the Network Inspector too late, don't worry, just edit the url of a .ts file. It should then print out the contents of this index playlist:

![the index.m3u8 in python](https://cloud.githubusercontent.com/assets/13566135/8977656/3068e8ee-36ef-11e5-9411-331119d0365d.png)

You can now enter in which resolution playlist you want to load. It then fetches the download links and gives you the options to download the files with python and create a text file of the links (it will create a folder called 'links' for this) in case you want to download them with a download manager. Either way, once the .ts files have been downloaded into a folder in 'downloads', <a href="https://www.bunkus.org/videotools/mkvtoolnix/">mkvmerge</a> can be used to mux them all into a .mkv file by pressing 'm' on the main menu:

![mkvmerge running in command prompt](https://cloud.githubusercontent.com/assets/13566135/8977947/ca7e3194-36f1-11e5-937c-861846592bcc.png)

<h2>To-Do</h2>

The things I have planned are:

<ul>
<li>To get some way of getting the index.m3u8 playlist from the main html file, so people can just input the page url. This seems really hard to do as I'd have to get the player that uses (JW Player) to play nice.</li>
<li>To clean-up the code (which I can't be bothered doing right now).</li>
<li>To get python to download the .ts files in parallel (so its atleast comparable to a download manager).</li>
</ul>
