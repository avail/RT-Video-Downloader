# The RT Video Downloader
This is a python script I made that allows for easier downloading of videos from <a href="http://roosterteeth.com">roosterteeth.com</a>. It isn't automatic, but makes things a lot less tedious.
<h2>Background</h2>
Videos on the new RoosterTeeth website (20 / 7 / 2015 onwards) are devided up into many 1 seconds long <a href="https://en.wikipedia.org/wiki/MPEG_transport_stream">Mpeg .ts</a> files, which is pretty wierd, and annoying to download manually because there could be thousands of files. Luckily, these are references by <a href="https://en.wikipedia.org/wiki/M3U">m3u8</a> playlist files, which are what this script uses to download videos.
