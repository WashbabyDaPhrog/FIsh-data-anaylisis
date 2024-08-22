#----Modules----#
import pandas as pd
import matplotlib.pyplot as plt

#----Global Variables----#
quit_program = False

#----Setup dataframe and query it here prior to creating visualisation and UI functions----#
def load_data():
    global original_df, fish_data_df

    # Load the original data
    original_df = pd.read_csv(r'C:\Users\kelvin.guo\Documents\Fishy_data.csv')
    
    # Load and clean the fish data
    fish_data_df = pd.read_csv(r'\Fish\Fish_data.csv', header=None, names=['Name', 'Code', 'Year', 'Weight'])
    
    # Clean the fish data
    clean_data()

def clean_data():
    global fish_data_df
    
    # Display initial data
    print("Initial Data:")
    print(fish_data_df.head())

    # 1. Handle Missing Values
    print("\nMissing Values:")
    print(fish_data_df.isnull().sum())

    # Fill missing 'Weight' with the mean of the column
    fish_data_df['Weight'].fillna(fish_data_df['Weight'].mean(), inplace=True)

    # 2. Remove Duplicate Rows
    print("\nDuplicate Rows:")
    print(fish_data_df.duplicated().sum())
    fish_data_df.drop_duplicates(inplace=True)

    # 3. Correct Data Types
    print("\nData Types:")
    print(fish_data_df.dtypes)
    fish_data_df['Year'] = pd.to_numeric(fish_data_df['Year'], errors='coerce').fillna(0).astype(int)

    # 4. Clean Column Names
    fish_data_df.columns = fish_data_df.columns.str.strip().str.lower()

    # 5. Handle Outliers
    fish_data_df['Weight'] = fish_data_df['Weight'].clip(upper=200)

    # Display cleaned data
    print("\nCleaned Data:")
    print(fish_data_df.head())

def showOriginalData():
    print(original_df)

def showUpdatedData():
    print(fish_data_df)

def showCharts():
    # Check if the necessary columns exist
    if 'Country' in fish_data_df.columns and 'AUD' in fish_data_df.columns:
        fish_data_df.plot(
            kind='bar',
            x='Country',
            y='AUD',
            color='blue',
            alpha=0.3,
            title='Tonnes of Fish Caught by Countries'
        )
        plt.xlabel('Country')
        plt.ylabel('AUD')
        plt.show()
    else:
        print('Required columns are not present in the updated data frame.')

def userOptions():
    global quit_program

    print(""" Fish Data Analysis
          
    Please select an option:
    1 - Show the original dataset
    2 - Show the updated Data Frame
    3 - Visualize the data
    4 - Quit Program
    """)
    
    try:
        choice = int(input('Enter Selection: '))

        if choice == 1:
            showOriginalData() 
        elif choice == 2:
            showUpdatedData()
        elif choice == 3:
            showCharts()
        elif choice == 4:
            quit_program = True
        else:
            print('Please select a number between 1 and 4.')

    except ValueError:
        print('Invalid input. Please enter a number.')

#----Main program----#
load_data()  # Load and clean data before starting the main loop
while not quit_program:
    userOptions()