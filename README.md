# The RT Video Downloader
This is a python script I made that allows for easier downloading of videos from <a href="http://roosterteeth.com">roosterteeth.com</a>. To be able to use this script, you'll need <a href="https://www.python.org/">python</a> 3.4.3.
<h2>Background</h2>
Videos on the new RoosterTeeth website (20 / 7 / 2015 onwards) are divided up into many 1 seconds long <a href="https://en.wikipedia.org/wiki/MPEG_transport_stream">Mpeg .ts</a> files, which is pretty weird, and annoying to download manually because there could be thousands of files. Luckily, these are references by <a href="https://en.wikipedia.org/wiki/M3U">m3u8</a> playlist files, which are what this script uses to download videos.
<h2>Usage</h2>
To download a video, run the script and press 'D' (or 'd', lowercase is fine) on the options menu, and enter in the url of the page of the video. The program will scan the contents of this page for a link to an aforementioned index.m3u8 file and download it. It should then print out the contents of this index playlist:

![the interface](https://cloud.githubusercontent.com/assets/13566135/9007141/86a35d86-37e2-11e5-886f-8fb73491d2c4.png)

You can now enter in which resolution playlist you want to load. It then fetches the download links and gives you the options to download the files with python and create a text file of the links (it will create a folder called 'links' for this) in case you want to download them with a download manager. Either way, once the .ts files have been downloaded into a folder in 'downloads', the files can be concatenated together by pressting 'M'.

<h2>Notes</h2>

<ul>
<li>If you want to download a video that is subscribers-only, don't worry. You'll need someone who has access to the video to send the url of the index file to you, after which you can download the files by pressing 'i' on the main menu.
<li>This is probably common sense, but this only works for videos that use jwplayer. If theres a video that you see using the youtube interface, it's hosted there and this script won't download it.</li>
<li>Despite the fact that they are called 480p in the playlist files, the videos assigned as being 480p are actually 360p.</li>
</ul>
