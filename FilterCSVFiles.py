import os
import pandas as pd

#****** THIS IS THE CORRECT UPDATE *******
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
                      "moratorium", "drugs", "marijuana", "crime", "shop", "cityworks", "safety", "forestry",
                      "recycling", "hunt", "animal", "hydrant", "ditch", "timber", "culvert", "greenway", "tax",
                      "child", "disease", "mortality", "infant", "cancer", "census", "gender", "calls", "food",
                      "council", "shelter", "retail", "pedestrian", "income", "mortality", "sports", "subway",
                      "athletics", "historic", "monument", "headstone", "residential", "neighborhoods", "covid19",
                      "poverty", "bike", "reading", "math"]

tagsSet = set(tags)  # converting list to a set for faster lookup
irrelevantKeywordsSet = set(irrelevantKeywords)

#https://pandas.pydata.org/docs/getting_started/comparison/comparison_with_sas.html#dataframe
# Define a function to check if any of the tags are present in a string
def containsRelevantTags(text):
    if pd.isnull(text):    # for reference https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.isnull.html#pandas.DataFrame.isnull
        return False
    text = text.lower()   # make sure text is all lowercase to avoid problems.
    for tag in tagsSet:   #loop through each tag in the set
        if tag in text:     # if a tag is present iin the text, return True bool.
            return True
    return False    # False otherwise


def containsExcludeKeywords(text):   # doing pretty much the same thing for this function as above
    if pd.isnull(text):
        return False
    text = text.lower()
    for keyword in irrelevantKeywordsSet:
        if keyword in text:
            return True


for filename in os.listdir(inputFolderPath):   # iterate through all CSVs in the input folder
    if filename.endswith('.csv'):              # endswith is a pd fucntion to test if the end of a string matches a pattern
        csvFilePath = os.path.join(inputFolderPath, filename)   # variable for the csvFilePath for the individual CSVs

        dataFrame = pd.read_csv(csvFilePath)    #using pandas to read the indivisual CSVs

        relevantRowsList = []                # create a list to store the relevant rows

        # iterate over each row in the dataFrame
        for index, row in dataFrame.iterrows():
            if 'description' in dataFrame.columns:
                dataFrame['description'].fillna('No description',
                                                   inplace=True)

            if (containsRelevantTags(row.get('tags', '')) or containsRelevantTags(row.get('title', '')) or containsRelevantTags(row.get('url', '')) or containsRelevantTags(row.get('description', ''))) \
                    and not (containsExcludeKeywords(row.get('tags', '')) or containsExcludeKeywords(row.get('title', '')) or containsExcludeKeywords(row.get('url', '')) or containsExcludeKeywords(row.get('description', ''))):
                relevantRowsList.append(row)     # if it's relevant add it to the list

        relevantRows = pd.DataFrame(relevantRowsList)     #convert the list of relevant rows to a DataFrame with DataFrame function


        outputCSVFilePath = os.path.join(outputFolderPath, filename)
        relevantRows.to_csv(outputCSVFilePath, index=False)

        print(f"Filtered DataFrame for {filename}:")
        print(relevantRows)

