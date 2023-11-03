import urllib.request
import json
import numpy as np
import math 

#URL from the FEMA Web Declarations endpoint - Dataset URL link 
baseUrl = "https://www.fema.gov/api/open/v2/DisasterDeclarationsSummaries"

#open the url and create request object
request = urllib.request.urlopen(baseUrl + "?$inlinecount=allpages&$select=id&$top=1")

#read the data and rprint the first 500 characters
result = request.read()
#print(result[:500])

#decode and show the first 500 characters, decode 
#so we can easily use / transform the data into a dict.
print(result.decode('utf-8')[:500])

#transform to python dictionary
jsonData = json.loads(result.decode('utf-8'))

#printing to check if works, comment out after 
#print(json.dumps(jsonData, indent = 2))


# example 1 - convert the dictionary to a json file using our json library (make up any filename you want)
# with open("fwdd_file_1.json", "w") as fp1:
#     json.dump(jsonData,fp1)

print(json.dumps(jsonData['metadata'], indent=2))

top = 10000

recCount = jsonData['metadata']['count']
loopNum = math.ceil(recCount / top)

print("For " + str(recCount) + " records we will need to issue " + str(loopNum) + " calls")


#csv file creation
orderby = "?$orderby=id"     # order unimportant to me, so use id field
limit = "&$top=10000"        # needed otherwise the default of 1000 will apply
format = "&$format=csv"      # let's use csv as our output type
other = "&$metadata=off"     # not needed as csv suppresses metadata - including for clarity


# Initialize our file. Only doing this because of the type of file wanted. See the loop below.
#   The root json entity is usually the name of the dataset, but you can use any name.
outFile = open("dds_output.csv", "w")


# Loop and call the API endpoint changing the record start each iteration. The metadata is being
#   suppressed as we no longer need it.
skip = 0
i = 0
while (i < loopNum):
    # issue call, decode the data, and save to a file
    request = urllib.request.urlopen(baseUrl + orderby + limit + format + other + "&$skip=" + str(skip))
    result = request.read()
    csvData = result.decode('utf-8')
    
    # avoid writing the header/fieldnames every time
    if (i == 0):
        # on the first record, so write full output that includes field headers
        outFile.write(csvData)
    else:
        # split off the first row
        outFile.write(csvData.split("\n",1)[1])
    
    # increment the loop counter and skip value
    i+=1
    skip = i * top

    print("Iteration " + str(i) + " done")

outFile.close()



#Json file creation
# orderby = "?$orderby=id"     # order unimportant to me, so use id field
# limit = "&$top=10000"        # needed otherwise the default of 1000 will apply
# format = "&$format=jsona"    # let's use an array of json objects - easier
# other = "&$metadata=off"     # not needed as jsona suppresses metadata - including for clarity


# # Initialize our file. Only doing this because of the type of file wanted. See the loop below.
# #   The root json entity is usually the name of the dataset, but you can use any name.
# outFile = open("dds_output.json", "w")
# outFile.write('{"disasterdeclarationssummaries":[');

# # Loop and call the API endpoint changing the record start each iteration. 
# skip = 0
# i = 0
# while (i < loopNum):
#     # By default, data is returned as a json object, the data set name being the root element. Unless
#     #   you extract records as you process, you will end up with 1 distinct json object for EVERY 
#     #   call/iteration. An alternative is to return the data as jsona (an array of json objects) with 
#     #   no root element - just a bracket at the start and end. This is easier to manipulate.
#     request2 = urllib.request.urlopen(baseUrl + orderby + limit + format + other + "&$skip=" + str(skip))
#     result = request2.read()
    
#     # The data is already returned in a json format. There is no need to decode and load as a JSON object.
#     #   If you want to begin working with and manipulating the json, import the json library and load with
#     #   something like: jsonData = json.loads(result.decode())

#     # Append results to file, trimming off first and last JSONA brackets, adding comma except for last call,
#     #   AND root element terminating array bracket and brace to end unless on last call. The goal here is to 
#     #   create a valid json file that contains ALL the records. This can be done differently.
#     if (i == (loopNum - 1)):
#         # on the last so terminate the single JSON object
#         outFile.write(str(result[1:-1],'utf-8') + "]}")
#     else:
#         outFile.write(str(result[1:-1],'utf-8') + ",")

#     # increment the loop counter and skip value
#     i+=1
#     skip = i * top

#     print("Iteration " + str(i) + " done")

# outFile.close()

# let's re-open the file and see if we got the number of records we expected
# inFile = open("dds_output.json", "r")
# my_data = json.load(inFile)
# print(str(len(my_data['disasterdeclarationssummaries'])) + " records in file")
# inFile.close()

