import pandas as pd
ALLOWED_EXTENSIONS = {'csv'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def parseCSV(filePath):
    # CVS Column Names
    col_names = ['Title', 'Asin', 'Review']
    # Use Pandas to parse the CSV file
    csvData = pd.read_csv(filePath, names=col_names, header=None)
    # Loop through the Rows
    for i, row in csvData.iterrows():
        print(i, row['Title', 'Asin', 'Review'])
