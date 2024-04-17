from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
    # Read the CSV file
    df = pd.read_csv('/Users/david2katsu/Desktop/baseball_model/final_table.csv')
    
    # Convert the DataFrame to an HTML table
    table_html = df.to_html(index=False)
    
    # Render the template with the table
    return render_template('index.html', table=table_html)

if __name__ == '__main__':
    app.run(debug=True)