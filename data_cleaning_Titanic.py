## Importing the library that will be used for the task
import pandas as pd


##### INPUT #####

### Reading the raw file and combining the three sheets into one dataframe ###
## Creating the function that returns a dataframe from an excel sheet
def excel_to_dataframe(file_url,sheetname):
    """
    
    Parameters
    ----------
    file_url : Excel file path
    
    sheetname : string with the name of the sheet

    Returns
    -------
    sheet_df : Excel sheet as a dataframe

    """
    sheet_df = pd.read_excel(
        file_url,
        sheet_name=sheetname,
        engine='openpyxl'
        )
    return sheet_df

## Creating the variables we need to read the excel file
excel_url = 'C:/Files/Titanic-raw.xlsx'
sheets_list = (['Cherbourg','Queenstown','Southampton'])

## Creating an iterator for the sheet list
sheetlist_iterator = iter(sheets_list)

## Reading the Excel file and combining the dataframes
titanic_df = excel_to_dataframe(
    excel_url,
    next(sheetlist_iterator)
    ).append(excel_to_dataframe(
        excel_url,
        next(sheetlist_iterator)
        )).append(excel_to_dataframe(
            excel_url,
            next(sheetlist_iterator)
            ))
     

### Cleaning Process ###

## Checking duplicates
titanic_data_duplicates = titanic_df.duplicated()
print('Number of duplicate entries is/are {}'.format(
    titanic_data_duplicates.sum()))

## Changing column 'Survived', '1' to 'Yes' and '0' to 'No'
titanic_df['Survived'] = titanic_df['Survived'].replace(
    to_replace=[1,0],value=['Yes','No'])

## Changing column 'Pclass'
titanic_df['Pclass'] = titanic_df['Pclass'].replace(
    to_replace=[1,2,3],value=['First Class','Second Class','Third Class'])

## Changing column 'Embarked'
titanic_df['Embarked'] = titanic_df['Embarked'].replace(
    to_replace=['C','Q','S'],value=['Cherbourg','Queenstown','Southampton'])

## Summing values of columns 'SibSp' and 'Pach' to get a new one.
titanic_df['Family Members'] = titanic_df['SibSp'] + titanic_df['Parch']

## Getting Gender and Sex data together in 'Gender' column.
titanic_subset = titanic_df[['Sex','Gender']]
titanic_subset = titanic_subset.fillna(
    method='ffill',
    axis=1
    )
titanic_df['Gender'] = titanic_subset['Gender']

## Dropping unnecessary columns
titanic_df.drop(
    ['Sex','SibSp','Parch','Cabin'],
    axis=1,
    inplace=True
    )

## Getting rid of rows with nan values
titanic_df = titanic_df.dropna(subset=['Age','Embarked'])

## Changing columns order
titanic_df = titanic_df[['PassengerId','Name','Age','Gender','Family Members', \
                         'Pclass','Embarked','Ticket','Fare','Survived']]


##### OUTPUT #####
    
### Exporting to a new clean excel file ###
## Creating writer variable to save the file
clean_excel_url = 'C:/Files/Titanic-clean.xlsx'
writer = pd.ExcelWriter(
    clean_excel_url
    )

## Exporting and saving the file
titanic_df.to_excel(
    writer,
    sheet_name='Titanic_Clean',
    index=False,
    engine='xlsxwriter'
    )
writer.save()

###################################################################