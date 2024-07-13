from flask import Flask, render_template
from flask import request, redirect, url_for

import csv

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

def format_indian(number):
    s, *d = str(number).partition(".")
    r = ",".join([s[x-2:x] for x in range(-3, -len(s), -2)][::-1] + [s[:-3]])
    # return "".join([r] + d)
    return number

def read_players():
    players = []
    with open('data/players.csv', mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            players.append(row)
    return players

def read_players_filter(filter):
    players = []
    with open('data/players.csv', mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['status'] == filter:
                players.append(row)
    return players

def get_player_by_id(player_id):
    with open('data/players.csv', mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if int(row['id']) == player_id:
                return row
    return None

def update_field(player_id, field_type, value):
    # Correctly calling the read_players function to get the current players data
    players = read_players()
    updated = False

    # Update the status in memory
    for player in players:
        if int(player['id']) == player_id:
            player[field_type] = value
            updated = True
            break

    # Write the updated data back to the CSV file if a player was updated
    if updated:
        with open('data/players.csv', mode='w', newline='') as file:
            fieldnames = ['id','name','age','role','base_price','image_path','status','sold_price','team']  # Add or remove fieldnames based on your CSV structure
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(players)


@app.route('/')
def home():
    players = read_players()
    return render_template('home.html', players=players, format_indian=format_indian)

@app.route('/unsold_players')
def unsold_players():
    players = read_players_filter('Unsold')
    return render_template('home.html', players=players, format_indian=format_indian)

@app.route('/sold_players')
def sold_players():
    players = read_players_filter('Sold')
    return render_template('home.html', players=players, format_indian=format_indian)

@app.route('/player/<int:player_id>')
def player_info(player_id):
    # Assuming you have a function to get a player by ID
    player = get_player_by_id(player_id)
    if player:
        return render_template('player_info.html', player=player, format_indian=format_indian)
    else:
        return "Player not found", 404
    

@app.route('/update_status/<int:player_id>', methods=['POST'])
def update_player_status(player_id):
    new_status = request.form['status']
    # Assuming you have a function to update the player's status
    update_field(player_id, 'status', new_status)
    return redirect(url_for('player_info', player_id=player_id))

@app.route('/update_team/<int:player_id>', methods=['POST'])
def update_player_team(player_id):
    new_team = request.form['team']
    # Assuming you have a function to update the player's status
    update_field(player_id, 'team', new_team)
    return redirect(url_for('player_info', player_id=player_id))

@app.route('/update_sold_price/<int:player_id>', methods=['POST'])
def update_player_sold_price(player_id):
    sold_price = request.form['sold_price']
    # Assuming you have a function to update the player's status
    update_field(player_id, 'sold_price', sold_price)
    return redirect(url_for('player_info', player_id=player_id))

if __name__ == '__main__':
    app.run(debug=True)