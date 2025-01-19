import pandas as pd

df = pd.read_csv('data/apl25-response.csv')

new_df = pd.DataFrame()
new_df['name'] = df.iloc[:, 1]
new_df['age'] = ""
new_df['role'] = df.iloc[:, 4]
new_df['flat'] = df.iloc[:, 2]
new_df['crichero'] = df.iloc[:, 7]
new_df['base_price'] = df.iloc[:, 5]
new_df['image_path'] = "images/user_profile.png"
new_df['status'] = "Unsold"
new_df['sold_price'] = 0
new_df['team'] = 0
new_df['id'] = range(1, len(df) + 1)
new_df['availability'] =  df.iloc[:, 6]
new_df['experience'] =  df.iloc[:, 8]

new_df.to_csv('data/apl0.csv', index=False)
print(new_df)
