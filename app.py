from flask import Flask, render_template
from flask import request, redirect, url_for
import pandas as pd

import csv

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
TEAM_FILE="data/teams.csv"
PLAYERS_FILE="data/alpine0.csv"

def format_indian(amount):
    """
    Format a given amount in Indian numbering format.
    :param amount: The amount to format.
    :return: The formatted amount as a string.
    """
    amount = str(amount)
    if '.' in amount:
        rupees, paisa = amount.split('.')
        paisa = '.' + paisa
    else:
        rupees = amount
        paisa = ''
    
    # Reverse the rupees part for easier processing
    rupees = rupees[::-1]
    
    # Process the first 3 digits
    formatted_rupees = rupees[:3]
    
    # Process remaining digits with a comma after every 2 digits
    for i in range(3, len(rupees), 2):
        formatted_rupees += ',' + rupees[i:i+2]
    
    # Reverse back to the original order and append paisa part
    return formatted_rupees[::-1] + paisa

def read_teams():
    teams = []
    with open(TEAM_FILE, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            teams.append(row)
    return teams

def read_players():
    players = []
    with open(PLAYERS_FILE, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            players.append(row)
    return players

def read_players_filter(filter):
    players = []
    with open(PLAYERS_FILE, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['status'] == filter:
                players.append(row)
    return players

def get_players_for_team(team_id):
    players = []
    with open(PLAYERS_FILE, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['team'] == str(team_id):
                players.append(row)
    return players

def get_player_by_id(player_id):
    with open(PLAYERS_FILE, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if int(row['id']) == player_id:
                return row
    return None

def get_team_by_id(team_id):
    with open(TEAM_FILE, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if int(row['id']) == team_id:
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
        with open(PLAYERS_FILE, mode='w', newline='') as file:
            fieldnames = ['name','age','role','flat','base_price','image_path','status','sold_price','team','id']  # Add or remove fieldnames based on your CSV structure
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(players)

def update_team_field(team_id, used_budget):
    # Correctly calling the read_players function to get the current players data
    teams = read_teams()
    updated = False

    # Update the status in memory
    for team in teams:
        if int(team['id']) == team_id:
            team['used_budget'] = str(int(team['used_budget']) + int(used_budget))
            updated = True
            break

    # Write the updated data back to the CSV file if a player was updated
    if updated:
        with open(TEAM_FILE, mode='w', newline='') as file:
            fieldnames = ['id','name','image_path','starting_budget','used_budget','players']  # Add or remove fieldnames based on your CSV structure
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(teams)


@app.route('/')
def home():
    players = read_players()
    teams = read_teams()
    return render_template('home.html', players=players, teams=teams, format_indian=format_indian)

@app.route('/teams')
def teams():
    teams = read_teams()
    return render_template('teams.html', teams=teams, get_players_for_team=get_players_for_team, format_indian=format_indian)

@app.route('/unsold_players')
def unsold_players():
    players = read_players_filter('Unsold')
    teams = read_teams()
    return render_template('home.html', players=players, teams=teams, format_indian=format_indian)

@app.route('/sold_players')
def sold_players():
    players = read_players_filter('Sold')
    teams = read_teams()
    return render_template('home.html', players=players, teams=teams, format_indian=format_indian)

@app.route('/random_player')
def random_player():
    df = pd.read_csv(PLAYERS_FILE)
    unsold_players = df[df['status'] == 'Unsold']
    random_player = unsold_players.sample(n=1).iloc[0]
    player = random_player.to_dict()
    teams = read_teams()
    return render_template('player_info.html', player=player, teams=teams, get_team_by_id=get_team_by_id, format_indian=format_indian)


@app.route('/player/<int:player_id>')
def player_info(player_id):
    ip_address = request.remote_addr
    # Assuming you have a function to get a player by ID
    player = get_player_by_id(player_id)
    teams = read_teams()
    if player:
        return render_template('player_info.html', player=player, teams=teams, ip_address=ip_address, get_team_by_id=get_team_by_id, format_indian=format_indian)
    else:
        return "Player not found", 404
    
@app.route('/team/<int:team_id>')
def team_info(team_id):
    # Assuming you have a function to get a player by ID
    ip_address = str(request.remote_addr)
    team = get_team_by_id(team_id)
    players = get_players_for_team(team_id)
    teams = read_teams()
    if team:
        return render_template('team_info.html', team=team, players=players, ip_address=ip_address, teams=teams, get_players_for_team=get_players_for_team, format_indian=format_indian)
    else:
        return "Team not found", 404
    
@app.route('/update_team_budget/<int:team_id>', methods=['POST'])
def update_team_budget(team_id):
    used_budget = request.form['used_budget']
    # Assuming you have a function to update the player's status
    update_team_field(team_id, used_budget)
    return redirect(url_for('team_info', team_id=team_id))

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