import pandas as pd
import gradio as gr

# Load the CSV file
file_path = './data/iclr2024_reviews_20231110.csv'
df = pd.read_csv(file_path)

# Define a function to filter the DataFrame based on a search query
def search_papers(query=""):
    if query:  # If there is a search query, filter the DataFrame
        filtered_df = df[df.apply(lambda row: row.astype(str).str.contains(query, case=False).any(), axis=1)]
        return filtered_df
    return df  # If no query, return the original DataFrame

with gr.Blocks() as demo:
    gr.Markdown("# ICLR 2024 Paper Review Explorer")
    gr.Markdown("Explore and search through the paper reviews for ICLR 2024. The papers are ranked based on their average score and standard deviation. More data and analysis at [GitHub Repository](https://github.com/ranpox/iclr2024-openreview-submissions)")
    search_bar = gr.Textbox(placeholder="Enter search terms here...", label="Search Reviews")
    
    # Initialize the reviews table with all the data
    reviews_table = gr.Dataframe(df)

    # When the search bar changes, update the reviews table with the filtered results
    search_bar.change(
        fn=search_papers,
        inputs=search_bar,
        outputs=reviews_table
    )

demo.launch()
