import streamlit as st
import json
import os
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Scoreboard Dashboard",
    page_icon="🏆",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
    }
    
    .player-card {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 0.75rem 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.08);
        border: 1px solid #dee2e6;
        margin-bottom: 0.5rem;
        transition: all 0.3s ease;
    }
    
    .player-card:hover {
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.12);
        transform: translateY(-1px);
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
    }
    
    .tag-badge {
        display: inline-block;
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        margin: 0.2rem;
        font-weight: 500;
    }
    
    .score-display {
        font-size: 2rem;
        font-weight: bold;
        color: #667eea;
        text-align: center;
    }
    
    .performer-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        border-left: 4px solid #667eea;
    }
    
    .performer-score {
        font-size: 1.5rem;
        font-weight: bold;
        color: #667eea;
        margin: 0.5rem 0;
    }
    
    .stButton > button {
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.5rem 1.5rem;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(102, 126, 234, 0.3);
    }
    
    .delete-btn {
        background: linear-gradient(45deg, #ff6b6b, #ee5a52) !important;
    }
    
    .reset-btn {
        background: linear-gradient(45deg, #dc3545, #c82333) !important;
    }
    
    /* Custom styling for player rows */
    .player-row {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 0.5rem 0.75rem;
        border-radius: 6px;
        margin-bottom: 0.25rem;
        border: 1px solid #dee2e6;
        transition: all 0.2s ease;
    }
    
    .player-row:hover {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
</style>
""", unsafe_allow_html=True)

# Data file for persistence
DATA_FILE = 'scoreboard_data.json'

def load_data():
    """Load data from JSON file"""
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r') as f:
                return json.load(f)
        except:
            pass
    return {
        'title': 'Game Night Championship',
        'players': [],
        'last_updated': datetime.now().isoformat()
    }

def save_data(data):
    """Save data to JSON file"""
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def get_stats():
    """Calculate statistics"""
    data = load_data()
    players = data.get('players', [])
    total_players = len(players)
    total_score = sum(p.get('score', 0) for p in players)
    avg_score = total_score / total_players if total_players > 0 else 0
    
    return {
        'total_players': total_players,
        'total_score': total_score,
        'avg_score': avg_score,
        'last_updated': data.get('last_updated', datetime.now().isoformat())
    }

def init_state():
    """Initialize session state with data from file"""
    if 'data_loaded' not in st.session_state:
        st.session_state['data_loaded'] = True
        data = load_data()
        st.session_state['scoreboard_title'] = data.get('title', 'Game Night Championship')
        st.session_state['players'] = data.get('players', [])
        st.session_state['last_updated'] = data.get('last_updated', datetime.now().isoformat())

def add_player(name):
    """Add a new player"""
    if not any(p.get('name') == name for p in st.session_state['players']):
        new_player = {
            'name': name,
            'score': 0,
            'tags': [],
            'created_at': datetime.now().isoformat()
        }
        st.session_state['players'].append(new_player)
        st.session_state['last_updated'] = datetime.now().isoformat()
        save_data({
            'title': st.session_state['scoreboard_title'],
            'players': st.session_state['players'],
            'last_updated': st.session_state['last_updated']
        })

def remove_player(name):
    """Remove a player"""
    st.session_state['players'] = [p for p in st.session_state['players'] if p.get('name') != name]
    st.session_state['last_updated'] = datetime.now().isoformat()
    save_data({
        'title': st.session_state['scoreboard_title'],
        'players': st.session_state['players'],
        'last_updated': st.session_state['last_updated']
    })

def update_score(name, score):
    """Update player score"""
    for p in st.session_state['players']:
        if p.get('name') == name:
            p['score'] = score
            st.session_state['last_updated'] = datetime.now().isoformat()
            save_data({
                'title': st.session_state['scoreboard_title'],
                'players': st.session_state['players'],
                'last_updated': st.session_state['last_updated']
            })
            break

def update_tags(name, tags):
    """Update player tags"""
    for p in st.session_state['players']:
        if p.get('name') == name:
            p['tags'] = tags
            st.session_state['last_updated'] = datetime.now().isoformat()
            save_data({
                'title': st.session_state['scoreboard_title'],
                'players': st.session_state['players'],
                'last_updated': st.session_state['last_updated']
            })
            break

def reset_all_data():
    """Reset all data"""
    st.session_state['players'] = []
    st.session_state['scoreboard_title'] = 'Game Night Championship'
    st.session_state['last_updated'] = datetime.now().isoformat()
    save_data({
        'title': st.session_state['scoreboard_title'],
        'players': st.session_state['players'],
        'last_updated': st.session_state['last_updated']
    })

def get_leaderboard():
    """Get sorted leaderboard"""
    return sorted(st.session_state['players'], key=lambda x: x.get('score', 0), reverse=True)

def main():
    init_state()
    
    # Header using native Streamlit
    st.markdown(f"# 🏆 {st.session_state['scoreboard_title']}")
    st.markdown("### Professional Scoreboard Dashboard")
    
    # Sidebar for controls
    with st.sidebar:
        st.markdown("### 🎮 Controls")
        
        # Title editor
        with st.form("title_form", clear_on_submit=True):
            new_title = st.text_input("Edit Dashboard Title", value=st.session_state['scoreboard_title'])
            submitted = st.form_submit_button("Update Title")
            if submitted and new_title.strip():
                st.session_state['scoreboard_title'] = new_title.strip()
                st.session_state['last_updated'] = datetime.now().isoformat()
                save_data({
                    'title': st.session_state['scoreboard_title'],
                    'players': st.session_state['players'],
                    'last_updated': st.session_state['last_updated']
                })
                st.rerun()
        
        st.markdown("---")
        
        # Add player
        with st.form("add_player_form", clear_on_submit=True):
            new_player = st.text_input("Add New Player")
            add_submitted = st.form_submit_button("➕ Add Player")
            if add_submitted and new_player.strip():
                add_player(new_player.strip())
                st.rerun()
        
        st.markdown("---")
        
        # Reset All Data
        st.markdown("### ⚠️ Danger Zone")
        if st.button("🗑️ Reset All Data", use_container_width=True, type="secondary"):
            reset_all_data()
            st.rerun()
        
        st.markdown("---")
        
        # Statistics
        st.markdown("### 📊 Statistics")
        stats = get_stats()
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Players", stats['total_players'])
        with col2:
            st.metric("Total Score", stats['total_score'])
        
        st.metric("Average Score", f"{stats['avg_score']:.1f}")
        
        # Last updated
        last_updated = stats['last_updated']
        if isinstance(last_updated, str):
            try:
                last_updated_dt = datetime.fromisoformat(last_updated)
                st.markdown(f"**Last Updated:** {last_updated_dt.strftime('%H:%M:%S')}")
            except:
                st.markdown(f"**Last Updated:** {last_updated}")
        else:
            st.markdown(f"**Last Updated:** {last_updated.strftime('%H:%M:%S')}")
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 🏅 Leaderboard")
        
        if st.session_state['players']:
            leaderboard = get_leaderboard()
            
            for i, player in enumerate(leaderboard):
                # Create compact single-line player card
                with st.container():
                    # Single line layout: Name | Score | Edit | Delete
                    player_col1, player_col2, player_col3, player_col4 = st.columns([3, 1, 1, 1])
                    
                    with player_col1:
                        # Player name and tags in one line
                        name_with_tags = f"**#{i+1} {player.get('name', '')}**"
                        if player.get('tags'):
                            tags_text = " ".join([f"`{tag}`" for tag in player.get('tags', [])])
                            name_with_tags += f" {tags_text}"
                        st.markdown(name_with_tags)
                    
                    with player_col2:
                        st.markdown(f"**{player.get('score', 0)}**")
                    
                    with player_col3:
                        if st.button("Edit", key=f"edit_{player.get('name', '')}", use_container_width=True):
                            st.session_state[f"editing_{player.get('name', '')}"] = True
                    
                    with player_col4:
                        if st.button("🗑️", key=f"delete_{player.get('name', '')}", help="Delete player", use_container_width=True):
                            remove_player(player.get('name', ''))
                            st.rerun()
                
                # Edit panel
                if st.session_state.get(f"editing_{player.get('name', '')}", False):
                    with st.expander(f"Edit {player.get('name', '')}", expanded=True):
                        edit_col1, edit_col2, edit_col3 = st.columns([1, 2, 1])
                        
                        with edit_col1:
                            new_score = st.number_input(
                                "Score", 
                                min_value=0, 
                                value=player.get('score', 0), 
                                key=f"score_{player.get('name', '')}"
                            )
                            if new_score != player.get('score', 0):
                                update_score(player.get('name', ''), new_score)
                                st.rerun()
                        
                        with edit_col2:
                            TAGS = ['🧠 Mind Reader', '🎭 Master of Mystery', '😶 Poker Face']
                            new_tags = st.multiselect(
                                "Tags",
                                TAGS,
                                default=player.get('tags', []),
                                key=f"tags_{player.get('name', '')}"
                            )
                            if set(new_tags) != set(player.get('tags', [])):
                                update_tags(player.get('name', ''), new_tags)
                                st.rerun()
                        
                        with edit_col3:
                            if st.button("Save", key=f"save_{player.get('name', '')}"):
                                st.session_state[f"editing_{player.get('name', '')}"] = False
                                st.rerun()
                            if st.button("Cancel", key=f"cancel_{player.get('name', '')}"):
                                st.session_state[f"editing_{player.get('name', '')}"] = False
                                st.rerun()
                
                st.markdown("---")
        else:
            st.info("🎯 No players yet. Add some players to get started!")
    
    with col2:
        st.markdown("### 🏆 Top Performers")
        
        if st.session_state['players']:
            leaderboard = get_leaderboard()
            
            # Top 3
            for i, player in enumerate(leaderboard[:3]):
                medal = ["🥇", "🥈", "🥉"][i]
                
                with st.container():
                    st.markdown(f"**{medal} {player.get('name', '')}**")
                    st.markdown(f"### {player.get('score', 0)} pts")
                    
                    # Display tags
                    if player.get('tags'):
                        tag_text = " ".join([f"`{tag}`" for tag in player.get('tags', [])])
                        st.markdown(tag_text)
                    
                    st.markdown("---")
        else:
            st.info("📊 Add players to see top performers!")

if __name__ == "__main__":
    main() 