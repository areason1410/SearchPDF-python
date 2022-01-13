import csv
import os
import textract


# checks if a string of text contains a word
def textContains(text, word):
        return f' {word.lower()} ' in f' {text.lower()} '

# given a .csv file, take all links in a certain row and save it to a download-list        
def readLinksFromCSV(file, rowIndex):
    
    # open file for reading
    wgetList = open("download-list", "w")
    
    with open(file) as csvFile:

        # read file as csv file 
        csvReader = csv.reader(csvFile)

        # iterate over the rows and wstore them in the download-list file
        for row in csvReader:
            wgetList.write(f"{row[rowIndex]}\n")

    # finished, close the file
    wgetList.close()


# search all files in the files folder for text
def filesContainText(searchTerm):
    foundFiles = []
    
    #iterate over the files
    for file in os.listdir("./files"):

        # open the pdf and read the contents
        pageContent = textract.process(f"./files/{file}")

        print("Searching: " + file)

        # if found, append it to the list of files that contain it
        if(textContains(pageContent, searchTerm)):
            foundFiles.append(file)

    # if we found files then output them and write them to a file
    if len(foundFiles) != 0:
        print("\n")
        resultsFile = open("results.txt", "a")
        resultsFile.write(f"Search Term: {searchTerm}\n\n")

        for i in range (0, len(foundFiles)):
            resultsFile.write(foundFiles[i]+ "\n")
            print("Found In: " + foundFiles[i])

        resultsFile.write("\n\n")
        resultsFile.close()
        print("\nResults also in results.txt file")
        print("\n\n-----------------------------\n\n")

    
    else:
        print("Not Found") # didn't find anything


if __name__ == "__main__":

    # create vars for later use
    shouldCreateDownloadList, shouldDownload  = ' ', ' '

    #check if there is a download-list file, if not ask if they want one
    if not "download-list" in os.listdir():
        shouldCreateDownloadList = input("Download list doesn't exist. Do you want to create one? Y/n: ")

    # if answer is yes, ask which .csv file to read from and the row index of the links 
    # then call the readLinksFromCSV function
    if(shouldCreateDownloadList == '' or shouldDownload.lower() == 'y'):
        fileName = input("File to read from: ")

        if(not fileName in os.listdir()):
            print("File doesn't exist")
            exit()

        rowIndex = int(input("Links row index: "))

        readLinksFromCSV(fileName, rowIndex)


    # if files folder isnt empty or doesn't exist, ask to download the files
    if not os.path.isdir("./files") or not os.listdir("./files"):
        shouldDownload = input("Files folder is empty or doesn't exist. Do you want to download files in download-list? Y/n: ")

    
    # if we should download then download the files in the download-list
    if(shouldDownload == '' or shouldDownload.lower() == 'y'):
        os.system("wget -P ./files -i download-list")
        print("\n\n-----------------------------\n\n")

    # loop for consecutive searches
    while(True):
        searchTerm = input("Search term: ")

        if(searchTerm == ''):
            exit()

        print("Begining Search: ")
        filesContainText(searchTerm)
