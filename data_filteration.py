import pandas as pd

class DataFilteration:

    def __init__(self):
        self.data = pd.read_csv('House_Rent_Dataset.csv')

    def extract_floor(self, s):

        nums = s.split()
        if nums[0] == 'Ground':
            return (0, int(nums[-1]))
        elif nums[0] == 'Upper':
            return (-1, int(nums[-1]))
        elif nums[0] == 'Lower':
            return (-2, int(nums[-1]))
        else:
            return (int(nums[0]), int(nums[-1]))

    def prepare_data(self):
        
        #removing unwanted columns
        self.data = self.data.drop('Posted On', axis=1)
        self.data = self.data.drop('Point of Contact', axis=1)

        #updating categorical values to the binary values
        self.data['Area Type'] = self.data['Area Type'].replace(['Super Area', 'Carpet Area'] , [0, 1])

        #encoding 'Furnishing Status' using one-hot encoding
        self.data = pd.get_dummies(self.data, columns= ['Furnishing Status'], dtype=int)
        self.data = pd.get_dummies(self.data, columns= ['Tenant Preferred'], dtype=int)

        #removing Tenant Preferred_bachlor/family as it is redundant
        self.data = self.data.drop('Tenant Preferred_Bachelors/Family', axis=1)

        mask = (self.data['Tenant Preferred_Bachelors'] == 0) & (self.data['Tenant Preferred_Family'] == 0)

        self.data.loc[mask, ['Tenant Preferred_Bachelors', 'Tenant Preferred_Family']] = 1

        #extracting numberics from string like values from the column
        self.data[['Floor','Total Floors']] = self.data['Floor'].apply(lambda x: pd.Series(self.extract_floor(x)))
        
        print(self.data)



data_filt = DataFilteration()