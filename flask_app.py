from flask import Flask, render_template, request, jsonify, abort, redirect, url_for
import pandas as pd

app = Flask(__name__)
csv_file_path = 'output.csv'

# Home Page
@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')

# CRUD

# Read all data
@app.route('/data')
def get_data():
    df = pd.read_csv(csv_file_path)
    return render_template('data.html', data=df.to_dict(orient='records'))

# Get data by team name API-like
@app.route('/data/<string:team_name>', methods=['GET'])
def get_data_by_team_name(team_name):
    df = pd.read_csv(csv_file_path)
    record = df[df['team_name'] == team_name]
    if record.empty:
        abort(404)
    return jsonify(record.to_dict(orient='records'))

# Search data
@app.route('/search')
def search_data():
    team_name = request.args.get('team_name', '')
    df = pd.read_csv(csv_file_path)
    record = df[df['team_name'] == team_name] if team_name else df
    return render_template('data.html', data=record.to_dict(orient='records'))

# Create data 
@app.route('/data/create', methods=['GET', 'POST'])
def create_data():
    if request.method == 'GET':
        return render_template('create.html')  # You'll need to create this template
    elif request.method == 'POST':
        new_data = request.form.to_dict()
        df = pd.read_csv(csv_file_path)
        if new_data['team_name'] in df['team_name'].values:
            abort(409, description="Record with this team name already exists.")
        new_data_df = pd.DataFrame([new_data])  # Convert new data into a DataFrame
        df = pd.concat([df, new_data_df], ignore_index=True)  # Use concat instead of append
        df.to_csv(csv_file_path, index=False)
        return redirect(url_for('get_data'))

# Update data: bug
@app.route('/data/update/<string:team_name>', methods=['GET', 'POST'])
def update_data(team_name):
    df = pd.read_csv(csv_file_path)
    record = df[df['team_name'] == team_name]
    if record.empty:
        abort(404)
    
    if request.method == 'GET':
        return render_template('update.html', record=record.iloc[0].to_dict())
    elif request.method == 'POST':
        updated_data = request.form.to_dict()
        updated_df = pd.DataFrame([updated_data])
        df.update(updated_df)
        df.to_csv(csv_file_path, index=False)
        return redirect(url_for('get_data'))

# Delete data
@app.route('/data/<string:team_name>', methods=['DELETE'])
def delete_data(team_name):
    df = pd.read_csv(csv_file_path)
    if team_name not in df['team_name'].values:
        abort(404)
    df = df[df['team_name'] != team_name]
    df.to_csv(csv_file_path, index=False)
    return jsonify({'result': True})

# PAGES
@app.route('/about')
def about():
    return render_template('about.html') 

@app.route('/team')
def team():
    return render_template('team.html')  


if __name__ == '__main__':
    app.run(debug=True)