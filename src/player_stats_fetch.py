import pandas as pd
import time
from nba_api.stats.static import players
from nba_api.stats.endpoints import playercareerstats, commonplayerinfo
import os

def main():
    injury_file_name = "data/injury_stats_clean.csv"
    output_file_name = "data/player_stats.csv"

    player_names = get_unique_players(injury_file_name)

    
    resume_from = "Ronald Dupree"  # Change this to where csv left off
    if resume_from in player_names:
        start_index = player_names.index(resume_from) + 1
        player_names = player_names[start_index:]
        print(f"Resuming from {resume_from} (index {start_index})...")
    else:
        print(f"Player {resume_from} not found — starting from beginning.")

    all_players = []


    existing_df = pd.read_csv(output_file_name)
    all_players.append(existing_df)
    print(f"Loaded {len(existing_df)} existing rows from previous run.")
     

    for i, name in enumerate(player_names, 1):
        player_df = fetch_player_stats(name)
        if player_df is not None:
            all_players.append(player_df)

        if i % 50 == 0:
            print(f"Processed {i}/{len(player_names)} players so far...")

        if i % 50 == 0:
            save_progress(all_players, output_file_name)
            print("💾 Progress saved ({0} players).".format(i))
            time.sleep(500) 

        time.sleep(5.0)

 
    combined = pd.concat(all_players, ignore_index=True)
    combined.to_csv(output_file_name, index=False)



def get_unique_players(injury_file_name):
    df = pd.read_csv(injury_file_name)
    players_list = sorted(df['Player'].dropna().unique().tolist())
    print(f"Found {len(players_list)} unique players.")
    return players_list


def fetch_player_stats(player_name):

    try:
        player_info = players.find_players_by_full_name(player_name)
        if not player_info:
            print(f"Player not found: {player_name}")
            return None

        player_id = player_info[0]['id']

        for attempt in range(1):
            try:
                career = playercareerstats.PlayerCareerStats(player_id=player_id)
                career_df = career.get_data_frames()[0]
                break
            except Exception as e:
                time.sleep(60 * (attempt + 1))
        else:
            print(f"Failed to fetch stats for {player_name} after retries.")
            return None

        career_df['PLAYER_NAME'] = player_name

    
        info = commonplayerinfo.CommonPlayerInfo(player_id=player_id)
        info_df = info.get_data_frames()[0][
            ['PERSON_ID', 'DISPLAY_FIRST_LAST', 'TEAM_NAME', 'HEIGHT', 'WEIGHT', 'BIRTHDATE']
        ]
        info_df.rename(columns={'DISPLAY_FIRST_LAST': 'PLAYER_NAME'}, inplace=True)

        merged = pd.merge(career_df, info_df, left_on='PLAYER_ID', right_on='PERSON_ID', how='left')
        return merged

    except Exception as e:
        print(f"Error fetching stats for {player_name}: {e}")
        return None


def save_progress(all_players, output_file_name):
    """Save progress safely to CSV."""
    try:
        combined = pd.concat(all_players, ignore_index=True)
        combined.to_csv(output_file_name, index=False)
    except Exception as e:
        print(f"Error saving progress: {e}")


if __name__ == "__main__":
    main()
