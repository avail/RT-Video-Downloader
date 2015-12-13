import subprocess, os, urllib.request as http, shutil
import threading, time
from glob import iglob

def roosterTeethDownloader(): # This is the main function. It basically just acts as a menu for other functions
    menuOptions = {'D' : 'to enter in the url of a video and download it.',\
                   'I' : 'to manually enter in a index.m3u8 playlist and download a video.',\
                   'J' : 'to concatenate downloaded files into a single file.',\
                   'X' : 'to exit.'}
    looping = True
    
    while (looping): # Loops the options until it is told to quit.
        response = validInput('Pick an option:', menuOptions)

        if response == 'D':
            url = addHttp(input('\nEnter the url of the video:\n'))
            indexFile, videoName = getIndexFile(url)
            
            if indexFile == '':
                print('An index.m3u8 file was not found. Please check that you have entered the correct url and that the video isn\'t on youtube instead.\n')
                return roosterTeethDownloader()

            print('\nIndex file found at:\n' + indexFile + '\n')
            
            if videoName == '':
                videoName = input('No video name found. Please enter one manually:\n')

            videoName = cleanVideoName(videoName) # Cleans up the video name to make sure it doesn't contain spaces etc.
            getLinks(videoName, indexFile)
    
        elif response == 'I':
            videoName = cleanVideoName(input('\nEnter the name of the video you want to download:\n'))
            url = addHttp(input('\nEnter the url of the index.m3u8 file:\n'))

            if not url.endswith('/index.m3u8'): # Makes sure that the url links to an index playlist.
                print('There was an error in the url.\nPlease try again.\n')
                return roosterTeethDownloader()

            getLinks(videoName, url)
            
        elif response == 'J':
            concatenate(chooseFolder())
            
        elif response == 'X':
            looping = False

        print('') # Prints out a blank line at the end because it looks better.

def getLinks(videoName, url): # This function takes the name of a video and a url and gets to work fetching links.
    resolutions, files, createFile = {}, [], ''

    rootUrl = url.strip('index.m3u8') # Sets rootUrl to be the root 'folder' where all of the files are.
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

    downloadOptions = {'D' : 'to download the files with python. This may be slower than using a download manager.',\
                       'T' : 'to create a text file of the download links.',\
                       'X' : 'to exit'}
    looping = True
    
    while (looping):
        response = validInput('Pick an option:', downloadOptions)
            
        if response == 'D':
            download(rootUrl, files, videoTitle)

        elif response == 'T':
            writeLinksFile(rootUrl, files, videoTitle)

        elif response == 'X':
            looping = False

def concatenate(folder): # This function takes a folder and merges all the files in it.
    if folder == '':
        return
    destination = open("downloads/"+folder+".ts", 'wb')
    for filename in sorted(iglob(os.path.join(r'downloads/'+folder, '*.ts'))):
        shutil.copyfileobj(open(filename, 'rb'), destination)
    destination.close()
    print('Concatenation completed.')


def dictionarify(aList, remove): # This function takes a list and a string of characters to remove and turns it into a dictionary.
    dictionary = {}
    
    for item in aList:
        dictionary[item.strip(remove)] = ''

    return dictionary

def readUrl(url): # This function requests a url (with firefox headers, roosterteeth.com rejects the default python headers) and returns its contents, decoded into utf-8.
    headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:39.0) Gecko/20100101 Firefox/39.0"}
    urlRequest = http.Request(url, headers = headers)

    return http.urlopen(urlRequest).read().decode('utf-8')

def cleanVideoName(name): # This function cleans up the video name using a list of banned characters.
    newName = name
    
    for char in ['\\', '/', '*', '?', '"', '<', '>', '|', '&quot;']:
        newName = newName.strip(char)

    newName = newName.replace(':', ' -').replace(' ', '_')

    if not name == newName:
        name = newName
        print('\nVideo renamed to ' + name + ' for compatability.')

    return name

def chooseFolder(): # This function allows the user to select a folder in 'downloads'.
    checkFolder('downloads')   
    folders = os.listdir('downloads')
    validFolders = []
    
    for folderName in folders:
        if validFolder('downloads/' + folderName):
            validFolders = validFolders + [folderName]

    folders = validFolders
    
    if folders == []:
        print("There are no valid folders in 'downloads'. Please download a video or add a folder to that location.")
        return ''

    print("\nChoose the id of the folder in 'downloads' that contains the .ts files you want muxed:") 
        
    for name in range(0, len(folders)):
        print(str(name + 1) + ': ' + folders[name])

    return folders[int(input()) - 1]

def removeComments(playlist): # This function takes a raw playlist and returns it as a list, removing lines that are empty and start with a hash.
    playlist = playlist.split('\n')
    goodLines = []
    
    for line in playlist:
        if not line.startswith('#') and not line == '':
            goodLines.append(line)
            
    return goodLines

def writeLinksFile(rootUrl, files, videoTitle): # This function creates a .txt file in 'links' that contains the links of a video.
    checkFolder('links')
    fileName = 'links/' + videoTitle + '.txt'

    file = open(fileName, 'w')

    for singularFile in files:
        file.write(rootUrl + singularFile + '\n')

    file.close()
    print("\n'" + fileName + "' created.\n")


def isInteger(i): # Checks if "i" is an integer. 

    try:
        int(i)
        return True
    except ValueError:
        return False

def threadDownload(rootUrl, files, directory, a, b):

    for file in range(a, b):
        print('Downloading ' + files[file] + ' (' + str(file + 1) + '/' + str(len(files)) + ')...')
        http.urlretrieve(rootUrl + files[file], directory + '/' + files[file])

def download(rootUrl, files, videoTitle): # This function requests and downloads the .ts files.
    checkFolder('downloads')
    directory = 'downloads/' + videoTitle
    checkFolder(directory)
    print('')

    numThreads = 'NaN'
    while (not isInteger(numThreads)):
        numThreads = input('Give me a number of threads to use:')
    
    numThreads = int(numThreads)
    filesPerThread = len(files) // numThreads # Integer division only.
    remainderFiles = len(files) %  numThreads # Give these to last thread.
    threadArray = []

    start = time.time()    
    for i in range(0, numThreads):
        a = i * filesPerThread
        b = a + filesPerThread
        if i == numThreads - 1:
            b += remainderFiles
        t = threading.Thread(None, threadDownload, 'Spartacus', (rootUrl, files, directory, a, b), {})
        print('Created thread ', i)
        threadArray.append(t)
        t.start()
        print('Thread ', i, ' started.')

    for i in range(0, numThreads):
        threadArray[i].join()
    
    print('\nVideo downloading completed.')
    end = time.time()
    print('Time elapsed: ', end - start, 'sec\n')

    downloadOptions = {'J' : 'to concatenate the files into a single file.',\
                       'X' : 'to exit'}
    looping = True

    while (looping):
        response = validInput('Pick an option:', downloadOptions)
            
        if response == 'J':
            concatenate(videoTitle)
            print('')

        elif response == 'X':
            looping = False

    print('') # Again, I print out a blank space so that it looks nicer.

def checkFolder(folder): # This function checks if a folder exists, and if it doesn't, it creates it and tells the user about it.
    if not os.path.exists(folder):
        os.makedirs(folder)
        print("\nFolder '" + folder + "' created.")

def validFolder(folder): # This function uses try to check if an item is indeed a folder but listing its contents. I could have had it check for extensions, but that wouldn't have work if a file didn't have one.
    try:
        os.listdir(folder)
        return not os.listdir(folder) == []

    except NotADirectoryError:
        return False

def validInput(prompt, options): # This function takes a prompt and a dictionary of options and validates the input.
    goodInput = False
    string = prompt + '\n'

    for option in sorted(options):
        string = string + option + ' ' + options[option] + '\n'
        
    while not goodInput:
        userInput = input(string)

        for option in options:
            if userInput.lower() == option.lower():
                userInput = option
                goodInput = True
                break
            
    return userInput

def addHttp(url): # This function makes sure that if you copy-paste a url from a browser that doesn't display the 'http://' part it puts it in.
    if not (url.startswith('http://') or url.startswith('https://')):
        url = 'http://' + url

    return url

def getIndexFile(url): # This function takes the url of a video page and returns the url of the index file and the name of the video.
    videoPage = readUrl(url).split('\n')
    indexFile, videoName = '', ''

    for line in videoPage: # Sets indexFile and videoName to items in a jwplayer <script> tag in the html.
        for char in line:
            if not char == ' ':
                break

            line = line[1:]

        if line.startswith("file: 'http://wpc"):
            indexFile = line.strip('file: ')[1:-2]

        elif line.startswith('var videoTitle = '):
            videoName = line.strip('var videoTitle = ')[1:-2]

    return indexFile, videoName

roosterTeethDownloader() # This starts the script.
