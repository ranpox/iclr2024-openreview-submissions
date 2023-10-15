from nomic import atlas
import pandas as pd

# run `nomic login` in the terminal to authenticate

df = pd.read_csv('../data/paperlist.csv')
df = df.drop(columns=['tldr']) # drop the tldr column since it's not compatible with atlas
project = atlas.map_text(
    data=df.to_dict('records'),
    indexed_field='title',
    name='ICLR 2024 Submission',
    colorable_fields=["primary_area"],
    reset_project_if_exists=True
)