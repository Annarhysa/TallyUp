from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
import os

app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)

# In-memory data store
scoreboard = {
    'title': 'Game Night Scoreboard',
    'players': []  # Each player: { 'name': str, 'score': int, 'tags': [str] }
}

TAGS = [
    '🧠 Mind Reader',
    '🎭 Master of Mystery',
    '😶 Poker Face'
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory(app.static_folder, filename)

@app.route('/api/scoreboard', methods=['GET'])
def get_scoreboard():
    return jsonify(scoreboard)

@app.route('/api/scoreboard/title', methods=['POST'])
def set_title():
    data = request.json
    scoreboard['title'] = data.get('title', scoreboard['title'])
    return jsonify({'success': True, 'title': scoreboard['title']})

@app.route('/api/scoreboard/player', methods=['POST'])
def add_player():
    data = request.json
    name = data.get('name')
    if not name:
        return jsonify({'error': 'Name required'}), 400
    if any(p['name'] == name for p in scoreboard['players']):
        return jsonify({'error': 'Player already exists'}), 400
    scoreboard['players'].append({'name': name, 'score': 0, 'tags': []})
    return jsonify({'success': True, 'players': scoreboard['players']})

@app.route('/api/scoreboard/player/<name>/score', methods=['POST'])
def update_score(name):
    data = request.json
    score = data.get('score')
    for player in scoreboard['players']:
        if player['name'] == name:
            player['score'] = score
            return jsonify({'success': True, 'player': player})
    return jsonify({'error': 'Player not found'}), 404

@app.route('/api/scoreboard/player/<name>/tags', methods=['POST'])
def update_tags(name):
    data = request.json
    tags = data.get('tags', [])
    for player in scoreboard['players']:
        if player['name'] == name:
            # Only allow valid tags
            player['tags'] = [t for t in tags if t in TAGS]
            return jsonify({'success': True, 'player': player})
    return jsonify({'error': 'Player not found'}), 404

@app.route('/api/scoreboard/player/<name>', methods=['DELETE'])
def delete_player(name):
    scoreboard['players'] = [p for p in scoreboard['players'] if p['name'] != name]
    return jsonify({'success': True, 'players': scoreboard['players']})

if __name__ == '__main__':
    app.run(debug=True) 