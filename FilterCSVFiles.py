import os
import pandas as pd


inputFolderPath = r'C:\InternCSVs\GIS_Web_Services'   # path for input folder
outputFolderPath = r'C:\InternCSVs\GIS_Web_Services\output'  # path for output folder

os.makedirs(outputFolderPath, exist_ok=True)  # create the output folder at the path defined above

# tags list defined below. Can always add more if needed.
tags = ["environment", "leases", "blocks", "licenses", "bathymetry", "wells", "gas wells", "pipeline", "pipelines",
        "infrastructure", "imagery", "weather", "geology", "seismic", "emissions", "topography", "parcel", "parcels",
        "renewables", "renewable", "solar", "wind", "biodiversity", "oil", "gas", "energy", "contour", "contours"]

# **** keywords that could possibly be taken out of this list -
# survey
irrelevantKeywords = ["school", "schools", "park", "parks", "wildlife", "miscellaneous", "addresses", "cemetaries",
                      "building", "buildings", "condo", "condos", "municipalities", "landslides", "bus", "route",
                      "county", "fire", "medical", "hospital", "hospitals", "police", "education", "voter", "vote", "voting",
                      "canoe", "cave", "housing", "curb", "sewer", "ems", "pictometry", "law", "hydrants", "libraries",
                      "health", "care", "polling", "townhalls", "subdivisions", "elections", "sidewalk", "lights",
                      "moratorium", "drugs", "marijuana", "crime", "shop", "cityworks", "safety", "forest", "forestry",
                      "recycling", "hunt", "animal", "hydrant", "ditch", "timber", "culvert", "greenway", "tax",
                      "child", "disease", "mortality", "infant", "cancer", "census", "gender", "calls", "food",
                      "council", "shelter", "retail", "pedestrian", "income", "mortality", "sports", "subway",
                      "athletics", "historic", "monument", "headstone", "residential", "neighborhoods", "covid19",
                      "poverty", "bike", "reading", "math", "treatment", "airport"]


tagsSet = set(tags)  # converting list to a set for faster lookup

irrelevantKeywordsSet = set(irrelevantKeywords)


#https://pandas.pydata.org/docs/getting_started/comparison/comparison_with_sas.html#dataframe
# Define a function to check if any of the tags are present in a string
def containsRelevantTags(text):
    if pd.isnull(text):   # for reference https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.isnull.html#pandas.DataFrame.isnull
                            # basically checking to see if the value 'text' is there or missing.
        return False      # returns a bool in documentation so return False if null/no value
    text = text.lower()   # make sure text is all lowercase to avoid problems. https://pandas.pydata.org/docs/reference/api/pandas.Series.str.lower.html#pandas.Series.str.lower

    for tag in tagsSet:   #loop through each tag in the set
        if tag in text:     # if a tag is present iin the text, return True bool.
            return True
    return False            # False otherwise


# Function to check if any exclude keywords are present in a string
def containsExcludeKeywords(text):
    if pd.isnull(text):
        return False
    text = text.lower()
    for keyword in irrelevantKeywordsSet:
        if keyword in text:
            return True
    return False


for filename in os.listdir(inputFolderPath):   # iterate through all CSVs in the input folder
    if filename.endswith('.csv'):     # endswith is a pd fucntion to test if the end of a string matches a pattern https://pandas.pydata.org/docs/reference/api/pandas.Series.str.endswith.html#pandas.Series.str.endswith
        csvFilePath = os.path.join(inputFolderPath, filename)  # variable for the csvFilePath for the individual CSVs (uses os.path.join to combine inputFolderPath with the csv filename.

        dataFrame = pd.read_csv(csvFilePath)   #using pandas to read the indivisual CSVs

        relevantRowsList = []  # create a list to store the relevant rows

        #iterate over each row in the dataFrame https://pandas.pydata.org/docs/getting_started/comparison/comparison_with_sas.html#dataframe
        for index, row in dataFrame.iterrows():
            if (containsRelevantTags(row['tags']) or containsRelevantTags(row['title']) or containsRelevantTags(row['url'])) \
                    and not (containsExcludeKeywords(row['tags']) or containsExcludeKeywords(row['title']) or containsExcludeKeywords(row['url'])):   #calling the containsRelevantTags function on the tags and titles of each entry
                relevantRowsList.append(row)     # if it's relevant add it to the list

        relevantRows = pd.DataFrame(relevantRowsList) #convert the list of relevant rows to a DataFrame with DataFrame function

        if 'description' in relevantRows.columns:
            relevantRows['description'].fillna('No description', inplace=True)

        outputCSVFilePath = os.path.join(outputFolderPath, filename)  #save the filtered dataFrame to a new csv in the output folder
        relevantRows.to_csv(outputCSVFilePath, index=False)  #convert the data frame to a csv

        print(f"Filtered DataFrame for {filename}:")   # print the results
        print(relevantRows)
