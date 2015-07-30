def roosterTeethDownloader():
    menuOptions = {'d' : 'to enter in a .m3u8 playlist and download a video',\
                   'm' : 'to use MkvToolNix to mux downloaded files into a mkv',\
                   'x' : 'to exit'}
    looping = True
    
    while (looping):
        response = validInput('Pick an option:', menuOptions)
        
        if response == 'd':
            videoName = cleanVideoName(input('\nEnter the name of the video you want to download:\n'))
            url = input('\nEnter the url of the index.m3u8 file:\n')

            getLinks(videoName, url)
            
        elif response == 'm':
            
            mkvMuxer(chooseFolder())
            
        elif response == 'x':
            
            looping = False

        print('')

def getLinks(videoName, url):
    resolutions = {}
    files = []
    createFile = ''
    
    if not url.endswith('/index.m3u8'):
        print('There was an error in the url.\nPlease try again.\n')
        return
    
    if not url.startswith('http://'):
        url = 'http://' + url
        
    rootUrl = url.replace('index.m3u8', '')
    print('\nDownloading index.m3u8 from ' + rootUrl + '...\n')
    index = readUrl(url)
    print(index)

    resolutions = dictionarify(removeComments(index), 'P.m3u8')

    chosenRes = validInput('Which resolution would you like to download?\nAvaliable resolutions:', resolutions)
    videoTitle = videoName + '_-_' + chosenRes
    url = rootUrl + chosenRes + 'P.m3u8'

    print('\nDownloading ' + chosenRes + ' from ' + rootUrl + '...\n')
    resolutionPlaylist = readUrl(url)
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

    print('')

def mkvMuxer(folder):
    import subprocess

    writeOptionsFile(folder)
    
    print("\nMuxing 'downloads/" + folder + ".mkv'...")
    subprocess.call('mkvmerge @downloads/' + folder + '/optionsFile.txt')
    print("\nVideo 'downloads/" + folder + ".mkv' created.\n")

def dictionarify(aList, remove):
    dictionary = {}
    for item in aList:
        dictionary[item.replace(remove, '')] = ''
    return dictionary

def readUrl(url):
    import urllib.request
    
    return urllib.request.urlopen(url).read().decode('utf-8')

def cleanVideoName(name):
    newName = name
    
    bannedChars = ['\\', '/', '*', '?', '"', '<', '>', '|']

    for char in bannedChars:
        newName = newName.replace(char, '')

    newName = newName.replace(':', ' -').replace(' ', '_')

    if not name == newName:
        name = newName
        print('\nVideo renamed to ' + name + ' for compatability.')
    return name

def chooseFolder():
    import os

    checkFolder('downloads')
    
    folders = os.listdir('downloads')
    if folders == []:
        print("There are no folders in 'downloads'. Please download a video or add a folder to that location.")
        return
    
    print("\nChoose the id of the folder in 'downloads' that contains the .ts files you want assembled:") 
    for folderName in range(0, len(folders)):
        if validFolder('downloads/' + folders[folderName]):
            print(str(folderName + 1) + ': ' + folders[folderName])
    return folders[int(input()) - 1]

def removeComments(playlist):
    playlist = playlist.split('\n')
    goodLines = []
    
    for line in playlist:
        if not line.startswith('#') and not line == '':
            goodLines.append(line)
            
    return goodLines

def writeOptionsFile(folder):
    import os
    
    videos = os.listdir('downloads/' + folder)
    options = 'downloads/' + folder + '/optionsFile.txt'
    print("\nWriting file '" + options + "'....")
    file = open(options, 'w')

    file.write('--output\ndownloads/' + folder + '.mkv\n--language\n0\ceng\n--language\n1\cund\n(\n')
    for video in videos:
        if video.endswith('.ts'):
            file.write('downloads/' + folder + '/' + video + '\n')
    file.write(')\n--track-order\n0\c0,0\c1')

    file.close()

def writeLinksFile(rootUrl, files, videoTitle):
    checkFolder('links')
        
    fileName = 'links/' + videoTitle + '.txt'

    file = open(fileName, 'w')
    for singularFile in files:
        file.write(rootUrl + singularFile + '\n')
    file.close()
    
    print("\n'" + fileName + "' created.\n")

def download(rootUrl, files, videoTitle):
    import urllib.request

    checkFolder('downloads')
    
    directory = 'downloads/' + videoTitle

    checkFolder(directory)

    print('')
    
    for file in range(0, len(files)):
        print('Downloading ' + files[file] + ' (' + str(file + 1) + '/' + str(len(files)) + ')...')
        urllib.request.urlretrieve(rootUrl + files[file], directory + '/' + files[file])
    print('\nVideo downloading completed.\n')

    downloadOptions = {'a' : 'to assemble the files into a mkv with mkvmerge.',\
                       'x' : 'to exit'}
    looping = True
    
    while (looping):
        response = validInput('Pick an option:', downloadOptions)
            
        if response == 'a':
            mkvMuxer(videoTitle)
        elif response == 'x':
            looping = False

def checkFolder(folder):
    import os
    
    if not os.path.exists(folder):
        os.makedirs(folder)
        print("\nFolder '" + folder + "' created.")

def validFolder(folder):
    import os
    
    try:
        os.listdir(folder)
        return True
    except NotADirectoryError:
        return False

def validInput(prompt, options):
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
        
roosterTeethDownloader()
