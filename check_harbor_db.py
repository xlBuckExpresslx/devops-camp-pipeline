import requests, sys, json, getopt

## Arguments needed from user ##
argList = sys.argv[1:]

## Modified to add -h option ##
options = 'c:i:p:r:h:'

arguments, values = getopt.getopt(argList, options)
for currentArgument, currentValue in arguments:
    if currentArgument in ("-c"):
        username, password = currentValue.split(':')
    elif currentArgument in ("-i"):
        imageName = currentValue
    elif currentArgument in ("-p"):
        projectName = currentValue
    elif currentArgument in ("-r"):
        registry = currentValue

    ## Added argument for DB_HASH ##
    elif currentArgument in ("-h"):
        pipelineDbHash = currentValue

## Added exception handling when image doesn't exist in harbor ##
try:
    ## Grab sha256 digest from Harbor project repository ##
    urlArtifact = 'https://' + registry + '/api/v2.0/projects/' + projectName + '/repositories/' + imageName + '/artifacts/'
    digestResp = requests.get(urlArtifact, auth=(username, password))
    artifactReference = digestResp.json()[0]['digest']

    ## Check harbor DB commit hash in image tag ##
    urlArtifactHashTag = urlArtifact + artifactReference + '/tags'
    hashTagResp = requests.get(urlArtifactHashTag, auth=(username, password))
    hashTag = hashTagResp.json()[0]['name']
    harborDbHash, harborPipelineHash = hashTag.split('-')

    if harborDbHash != pipelineDbHash:
        print('true')
    else:
        print('false')

## Build DB when image doesn't exist or something goes wrong ##
except:
    print('true')
