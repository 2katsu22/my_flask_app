from flask import Flask, render_template
from flask import Flask, request, jsonify, abort
import pandas as pd
import json

app = Flask(__name__)
csv_file_path = 'output.csv'

# home 
@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')

# read
# @app.route('/data', methods=['GET'])
# def get_data():
#     df = pd.read_csv(csv_file_path)
#     data_json = df.to_json(orient='records')
#     return jsonify(json.loads(data_json))
@app.route('/data')
def get_data():
    df = pd.read_csv(csv_file_path)
    # Pass the DataFrame to the template
    return render_template('data.html', data=df.to_dict(orient='records'))

@app.route('/data/<string:team_name>', methods=['GET'])
def get_data_by_team_name(team_name):
    df = pd.read_csv(csv_file_path)
    record = df[df['team_name'] == team_name]
    if record.empty:
        abort(404)
    return jsonify(json.loads(record.to_json(orient='records')))

@app.route('/search')
def search_data():
    team_name = request.args.get('team_name', '')
    if team_name:
        df = pd.read_csv(csv_file_path)
        record = df[df['team_name'] == team_name]
        if record.empty:
            return render_template('data.html', data=[], message="No records found for the given team name.")
        return render_template('data.html', data=record.to_dict(orient='records'))
    else:
        # If no search term provided, render the data.html template with the entire dataset
        df = pd.read_csv(csv_file_path)
        return render_template('data.html', data=df.to_dict(orient='records'))


# needs to TEST: 
# Create
@app.route('/data', methods=['POST'])
def create_data():
    if not request.json:
        abort(400)
    new_data = request.json
    df = pd.read_csv(csv_file_path)
    if new_data['team_name'] in df['team_name'].values:
        abort(409, description="Record with this team_name already exists.")
    df = df.append(new_data, ignore_index=True)
    df.to_csv(csv_file_path, index=False)
    return jsonify(new_data), 201

# update
@app.route('/data/<string:team_name>', methods=['PUT'])
def update_data(team_name):
    if not request.json:
        abort(400)
    df = pd.read_csv(csv_file_path)
    if team_name not in df['team_name'].values:
        abort(404)
    updated_data = request.json
    df.loc[df['team_name'] == team_name, :] = updated_data
    df.to_csv(csv_file_path, index=False)
    return jsonify(updated_data)

# delete
@app.route('/data/<string:team_name>', methods=['DELETE'])
def delete_data(team_name):
    df = pd.read_csv(csv_file_path)
    if team_name not in df['team_name'].values:
        abort(404)
    df = df[df['team_name'] != team_name]
    df.to_csv(csv_file_path, index=False)
    return jsonify({'result': True})

if __name__ == '__main__':
    app.run(debug=True)