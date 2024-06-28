import os
import pandas as pd
import re

inputFolderPath = r'C:\InternCSVs\GIS_Web_Services'   # path for input folder
outputFolderPath = r'C:\InternCSVs\GIS_Web_Services\output'  # path for output folder

os.makedirs(outputFolderPath, exist_ok=True)  # create the output folder at the path defined above

# tags list defined below. Can always add more if needed.
tags = ["environment", "leases", "blocks", "licenses", "bathymetry", "wells", "gas wells", "pipeline", "pipelines",
        "infrastructure", "imagery", "weather", "geology", "seismic", "emissions", "topography", "parcel", "parcels",
        "renewables", "renewable", "solar", "wind", "biodiversity", "oil", "gas", "energy", "contour", "contours"]

# **** keywords that could possibly be taken out of this list -
# survey
irrelevantKeywords = ["school", "schools", "park", "parks", "miscellaneous", "addresses", "cemetaries",
                      "building", "buildings", "condo", "condos", "municipalities", "landslides", "bus", "route",
                      "county", "fire", "medical", "hospital", "hospitals", "police", "education", "voter", "vote", "voting",
                      "canoe", "cave", "housing", "curb", "sewer", "ems", "pictometry", "law", "hydrants", "libraries",
                      "health", "care", "polling", "townhalls", "subdivisions", "elections", "sidewalk", "lights",
                      "moratorium", "drugs", "marijuana", "crime", "shop", "cityworks", "safety", "forestry",
                      "recycling", "hunt", "animal", "hydrant", "ditch", "timber", "culvert", "greenway", "tax",
                      "child", "disease", "mortality", "infant", "cancer", "census", "gender", "calls", "food",
                      "council", "shelter", "retail", "pedestrian", "income", "mortality", "sports", "subway",
                      "athletics", "historic", "monument", "headstone", "residential", "neighborhoods", "covid19",
                      "poverty", "bike", "reading", "math"]

tagsSet = set(tags)  # converting list to a set for faster lookup
irrelevantKeywordsSet = set(irrelevantKeywords)


def containsRelevantTags(text):
    if pd.isnull(text):    # for reference https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.isnull.html#pandas.DataFrame.isnull
        return False
    text = text.lower()   # make sure text is all lowercase to avoid problems.
    for keyword in tagsSet:
        if re.search(r'\b{}\b'.format(keyword), text):  # finds whole words. "b" is a boundary that matches
                                                        # the position at the start or end of a word while {}
                                                        # are placeholders for the keyword.
            return True
    return False


def containsExcludeKeywords(text):
    if pd.isnull(text):
        return False
    text = text.lower()
    for keyword in irrelevantKeywordsSet:
        if re.search(r'\b{}\b'.format(keyword), text):
            return True
    return False


for filename in os.listdir(inputFolderPath):  # iterate through all CSVs in the input folder
    if filename.endswith('.csv'):  # endswith is a pd function to test if the end of a string matches a pattern
        csvFilePath = os.path.join(inputFolderPath, filename)  # variable for the csvFilePath for the individual CSVs

        dataFrame = pd.read_csv(csvFilePath)  # using pandas to read the individual CSVs

        relevantRowsList = []  # create a list to store the relevant rows

        #start looping through the dataframe
        for index, row in dataFrame.iterrows():
            if 'description' in dataFrame.columns:
                dataFrame['description'].fillna('No description', inplace=True) # add a "no description first since we
                # want to avoid checking null values for description below

            # checking to see if row is relevant
            if (containsRelevantTags(row['tags']) or containsRelevantTags(row['url']) or containsRelevantTags(row['title']) or containsRelevantTags(row['description'])) \
                    and not (containsExcludeKeywords(row['tags']) or containsExcludeKeywords(row['url']) or containsExcludeKeywords(row['title']) or containsExcludeKeywords(row['description'])):
                relevantRowsList.append(row)  # if it's relevant add it to the list

        # Convert the list of relevant rows to a DataFrame
        relevantRows = pd.DataFrame(relevantRowsList)

        outputCSVFilePath = os.path.join(outputFolderPath, filename)
        relevantRows.to_csv(outputCSVFilePath, index=False)

        print(f"Filtered DataFrame for {filename}:")
        print(relevantRows)
