##----Modules----#
import pandas as pd
import matplotlib.pyplot as plt

#----Global Variables----#
quit = False
fish_data_df = pd.DataFrame()  
top_10_countries = pd.Series()  

# Define credentials
USERNAME = 'Kelvin'
PASSWORD = 'Skibidi'

#----Setup dataframe----#
def load_data():
    global original_df, fish_data_df, top_10_countries
    original_df = pd.read_csv('/Fish/FIsh-data-anaylisis/Fish_data.csv')
    fish_data_df = pd.read_csv(r'/Fish/FIsh-data-anaylisis/Fish_data.csv',
                               header=None,
                               names=['Entity', 'Code', 'Year', 'Fish and seafood'])
    
    # Clean the data
    fish_data_df = clean_data(fish_data_df)
    
    # Calculate top 10 seafood harvest countries
    country_totals = fish_data_df.groupby('Entity')['Fish and seafood'].sum()
    top_countries = country_totals.sort_values(ascending=False)
    top_10_countries = top_countries.head(10)

def clean_data(df):
    # Convert 'Fish and seafood' and 'Year' to numeric
    df['Fish and seafood'] = pd.to_numeric(df['Fish and seafood'], errors='coerce').fillna(0)
    df['Year'] = pd.to_numeric(df['Year'], errors='coerce').fillna(0)
    
    # Drop duplicate rows
    df.drop_duplicates(inplace=True)
    return df

#----Define Functions Below----#
def showOriginalData():
    print(original_df)

def avg_harvest():
    fish_data_df['Fish and seafood'] = pd.to_numeric(fish_data_df['Fish and seafood'], errors='coerce')
    average_harvest = fish_data_df['Fish and seafood'].mean()
    print(f"The average seafood harvest is {average_harvest:,.2f} tonnes")

def showUpdatedData():
    df = fish_data_df.copy()
    df = clean_data(df)
    print(df)
    print("\nMissing Values:")
    print(df.isnull().sum())

def showCharts():
    fish_data_df.plot(
        kind='scatter',
        x='Entity',
        y='Fish and seafood',
        color='blue',
        alpha=0.5,
        title='Tonnes of Seafood Caught by Country'
    )
    plt.show()

fish_data_df.to_csv("/Fish/FIsh-data-anaylisis/new_fish_data.csv", index = False)

def isolate_country_data(df, country_name):
   
    #Isolate and analyze data for a specific country
    
    country_data = df[df['Entity'] == country_name]
    total_harvest = country_data['Fish and seafood'].sum()
    yearly_data = country_data.groupby('Year')['Fish and seafood'].sum().reset_index()
    return total_harvest, yearly_data

def userOptions():
    global quit

    print("""
    Fish Data Analysis

    Please select an option:
    1 - Show the original dataset
    2 - Show the updated Data Frame
    3 - Visualize the Tonnes of Seafood Caught by Country
    4 - Average Harvest
    5 - Top 10 Seafood Harvest
    6 - Isolate Country (total harvest)
    7 - Isolate Country (yearly harvest)
    8 - Quit Program
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
            avg_harvest()
        elif choice == 5:
            print("\nTop 10 Seafood Harvest Countries:")
            print(top_10_countries)
        elif choice == 6:
            country_name = input('Enter the name of the country: ')
            total_harvest = isolate_country_data(fish_data_df, country_name)[0]
            print(f"Total Seafood Harvest for {country_name}: {total_harvest:,.2f} tonnes")
        elif choice == 7:
            country_name = input('Enter the name of the country: ')
            _, yearly_data = isolate_country_data(fish_data_df, country_name)
            print(f"\nYearly Seafood Harvest Data for {country_name}:")
            print(yearly_data)
        elif choice == 8:
            quit = True
        else:
            print('Please enter a number between 1 and 8.')

    except ValueError:
        print('Invalid input. Please enter a number.')

def authenticate_user():
    """Authenticate user based on username and password."""
    print("Please login:")
    username = input("Username: ")
    password = input("Password: ")

    if username == USERNAME and password == PASSWORD:
        print("Login successful!")
        return True
    else:
        print("Invalid username or password.")
        return False

#----Main program----#
if authenticate_user():
    load_data()  # Load and clean data before starting the main loop
    while not quit:
        userOptions()