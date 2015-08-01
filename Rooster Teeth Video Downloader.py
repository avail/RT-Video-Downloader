def roosterTeethDownloader():
    # This is the main function. It basically just acts as a menu for other functions
    menuOptions = {'d' : 'to enter in the url of a video and download it.',\
                   'i' : 'to manually enter in a index.m3u8 playlist and download a video. This is useful for downloading subscriber-only videos.',\
                   'm' : 'to use MkvToolNix to mux downloaded files into a mkv.',\
                   'x' : 'to exit.'}
    looping = True
    
    while (looping): # Loops the options until it is told to quit.
        response = validInput('Pick an option:', menuOptions)

        if response == 'd':
            url = input('\nEnter the url of the video:\n')
            
            indexFile, videoName = getIndexFile(url)
            
            if indexFile == '':
                print('An index.m3u8 file was not found. Please check that you have entered the correct url.')
                return

            print('\nIndex file found at:\n' + indexFile + '\n')
            
            if videoName == '':
                videoName = input('No video name found. Please enter one manually:\n')

            videoName = cleanVideoName(videoName) # Cleans up the video name to make sure it doesn't contain spaces etc.
            
            getLinks(videoName, indexFile)
    
        elif response == 'i':
            videoName = cleanVideoName(input('\nEnter the name of the video you want to download:\n'))
            url = input('\nEnter the url of the index.m3u8 file:\n')

            getLinks(videoName, url)
            
        elif response == 'm':
            
            mkvMuxer(chooseFolder())
            
        elif response == 'x':
            
            looping = False

        print('') # Prints out a blank line at the end because it looks better.

def getLinks(videoName, url):
    # This function takes the name of a video and a url and gets to work fetching links.
    resolutions = {}
    files = []
    createFile = ''
    
    if not url.endswith('/index.m3u8'): # Makes sure that the url links to an index playlist.
        print('There was an error in the url.\nPlease try again.\n')
        return
    
    if not url.startswith('http://'): # Makes sure that if you copy-paste a url from a browser that doesn't display the 'http://' part it puts it in.
        url = 'http://' + url
        
    rootUrl = url.replace('index.m3u8', '') # Sets rootUrl to be the root 'folder' where all of the files are.
    print('\nDownloading index.m3u8 from ' + rootUrl + '...\n')
    index = readUrl(url) # Loads index as the contents of the url.
    print(index)

    resolutions = dictionarify(removeComments(index), 'P.m3u8') # Sets resolutions to an empty dictionary with the keys being each resolution (minus the P.m3u8 part).

    chosenRes = validInput('Which resolution would you like to download?\nAvaliable resolutions:', resolutions) # Makes sure the input is only of the featured resolutions.
    videoTitle = videoName + '_-_' + chosenRes
    url = rootUrl + chosenRes + 'P.m3u8'

    print('\nDownloading ' + chosenRes + 'P.m3u8 from ' + rootUrl + '...\n')
    resolutionPlaylist = readUrl(url) # Sets resolution playlist to the contents of the chosen resoluton .m3u8 playlist.
    print(resolutionPlaylist)

    for file in removeComments(resolutionPlaylist):
        files.append(file)
        
    print(str(len(files)) + ' files found (it begins with ' + files[0] + ').\n')

    downloadOptions = {'d' : 'to download the files with python. This may be slower than using a download manager.',\
                       't' : 'to create a text file of the download links.',\
                        'x' : 'to exit'}
    looping = True
    
    while (looping):
        response = validInput('Pick an option:', downloadOptions)
            
        if response == 'd':
            download(rootUrl, files, videoTitle)
        elif response == 't':
            writeLinksFile(rootUrl, files, videoTitle)
        elif response == 'x':
            looping = False

def mkvMuxer(folder):
    # This function takes a folder and merges all the videos in it.
    import subprocess

    writeOptionsFile(folder) # Creates a mkvmerge-valid options file that it tells mkvmerge to access (I ran out of bytes to call the whole thing with).
    
    print("\nMuxing 'downloads/" + folder + ".mkv'...")
    subprocess.call('mkvmerge @downloads/' + folder + '/optionsFile.txt') # Calls mkvmerge and points it to the optionsFile.
    print("\nVideo 'downloads/" + folder + ".mkv' created.")

def dictionarify(aList, remove):
    # This function takes a list and a string of characters to remove and turns it into a dictionary.
    dictionary = {}
    for item in aList:
        dictionary[item.replace(remove, '')] = ''
    return dictionary

def readUrl(url):
    # This function requests a url (with firefox headers, roosterteeth.com rejects the default python headers) and returns its contents, decoded into utf-8.
    import urllib.request

    headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:39.0) Gecko/20100101 Firefox/39.0"}
    urlRequest = urllib.request.Request(url, headers = headers)
    return urllib.request.urlopen(urlRequest).read().decode('utf-8')

def cleanVideoName(name):
    # This function cleans up the video name using a list of banned characters.
    newName = name
    
    for char in ['\\', '/', '*', '?', '"', '<', '>', '|']:
        newName = newName.replace(char, '')

    newName = newName.replace(':', ' -').replace(' ', '_')

    if not name == newName:
        name = newName
        print('\nVideo renamed to ' + name + ' for compatability.')
    return name

def chooseFolder():
    # This function allows the user to select a folder in 'downloads'.
    import os

    checkFolder('downloads')
    
    folders = os.listdir('downloads')
    if folders == []:
        print("There are no folders in 'downloads'. Please download a video or add a folder to that location.")
        return
    
    print("\nChoose the id of the folder in 'downloads' that contains the .ts files you want assembled:") 
    for folderName in range(0, len(folders)):
        if validFolder('downloads/' + folders[folderName]):
            print(str(folderName + 1) + ': ' + folders[folderName]) # This is a pretty bad system, because if theres an item in 'downloads' that isn't a folder (such as a .mkv file), it'll skip an id, which is pretty wierd. Will fix up soon(tm).
    return folders[int(input()) - 1]

def removeComments(playlist):
    # This function takes a raw playlist and returns it as a list, removing lines that are empty and start with a hash.
    playlist = playlist.split('\n')
    goodLines = []
    
    for line in playlist:
        if not line.startswith('#') and not line == '':
            goodLines.append(line)
            
    return goodLines

def writeOptionsFile(folder):
    # This function takes a folder and writes a mkvmerge options file for it.
    import os
    
    videos = os.listdir('downloads/' + folder) # I should probably validate this so it checks if each item is a .ts file.
    options = 'downloads/' + folder + '/optionsFile.txt'
    print("\nWriting file '" + options + "'....")
    file = open(options, 'w')

    file.write('--output\ndownloads/' + folder + '.mkv\n--language\n0\ceng\n--language\n1\cund\n(\n') # Eutgh that syntax :/ .
    for video in videos:
        if video.endswith('.ts'):
            file.write('downloads/' + folder + '/' + video + '\n')
    file.write(')\n--track-order\n0\c0,0\c1')

    file.close()

def writeLinksFile(rootUrl, files, videoTitle):
    # This function creates a .txt file in 'links' that contains the links of a video.
    checkFolder('links')
        
    fileName = 'links/' + videoTitle + '.txt'

    file = open(fileName, 'w')
    for singularFile in files:
        file.write(rootUrl + singularFile + '\n')
    file.close()
    
    print("\n'" + fileName + "' created.\n")

def download(rootUrl, files, videoTitle):
    # This function requests and downloads the .ts files.
    import urllib.request

    checkFolder('downloads')
    
    directory = 'downloads/' + videoTitle

    checkFolder(directory)

    print('')
    
    for file in range(0, len(files)):
        print('Downloading ' + files[file] + ' (' + str(file + 1) + '/' + str(len(files)) + ')...')
        urllib.request.urlretrieve(rootUrl + files[file], directory + '/' + files[file])
    print('\nVideo downloading completed.\n')

    downloadOptions = {'m' : 'to mux the files into a mkv with mkvmerge.',\
                       'x' : 'to exit'}
    looping = True
    
    while (looping):
        response = validInput('Pick an option:', downloadOptions)
            
        if response == 'm':
            mkvMuxer(videoTitle)
            print('')
        elif response == 'x':
            looping = False

    print('') # Again, I print out a blank space so that it looks nicer.

def checkFolder(folder):
    # This is a function I like a lot, it checks if a folder exists, and if it doesn't, it creates it and tells the user about it.
    import os
    
    if not os.path.exists(folder):
        os.makedirs(folder)
        print("\nFolder '" + folder + "' created.")

def validFolder(folder):
    # I also like this one a lot. It uses try to check if an item is indeed a folder but listing its contents. I could have had it check for extensions, but that wouldn't have work if a file didn't have one.
    import os
    
    try:
        os.listdir(folder)
        return True
    except NotADirectoryError:
        return False

def validInput(prompt, options):
    # This function takes a prompt and a dictionary of options and validates the input.
    goodInput = False
    string = prompt + '\n'

    for option in sorted(options):
        string = string + option + ' ' + options[option] + '\n'
        
    while not goodInput:
        userInput = input(string)

        for option in options:
            if userInput == option:
                goodInput = True
                break
            
    return userInput.lower()

def getIndexFile(url):
    # This function takes the url of a video page and returns the url of the index file and the name of the video.
    videoPage = readUrl(url).split('\n')
    indexFile = ''
    videoName = ''

    for line in videoPage: # Sets indexFile and videoName to items in a jwplayer <script> tag in the html.
        if line.startswith('                                    manifest: '):
            indexFile = line.replace('                                    manifest: ', '')[1:-2]
        elif line.startswith('                                videoTitle: '):
            videoName = line.replace('                                videoTitle: ', '')[1:-2]
            
    return indexFile, videoName

roosterTeethDownloader() # This starts the script.
