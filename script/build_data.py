import pandas as pd

df = pd.read_csv('data/response.csv')
substring = 'Alpine Champions League '
filtered_df = df[df['Choose the games you want to participate?( Maximum 5 games can be chosen)'].str.contains(substring, na=False)]

new_df = pd.DataFrame()

new_df['name'] = filtered_df.iloc[:, 1]
new_df['age'] = filtered_df.iloc[:, 3]
new_df['role'] = filtered_df.iloc[:, 7]
new_df['flat'] = filtered_df.iloc[:, 5]
new_df['base_price'] = "2000000"
new_df['image_path'] = "images/user_profile.png"
new_df['status'] = "Unsold"
new_df['sold_price'] = 0
new_df['team'] = 0
new_df['id'] = range(1, len(filtered_df) + 1)
new_df.to_csv('data/alpine0.csv', index=False)

print(new_df)
