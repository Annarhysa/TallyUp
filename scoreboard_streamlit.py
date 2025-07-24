import streamlit as st

# Special tags
TAGS = [
    '🧠 Mind Reader',
    '🎭 Master of Mystery',
    '😶 Poker Face'
]

def init_state():
    if 'scoreboard_title' not in st.session_state:
        st.session_state['scoreboard_title'] = 'Game Night Scoreboard'
    if 'players' not in st.session_state:
        st.session_state['players'] = []  # Each: {'name': str, 'score': int, 'tags': [str]}

def add_player(name):
    if not any(p['name'] == name for p in st.session_state['players']):
        st.session_state['players'].append({'name': name, 'score': 0, 'tags': []})

def remove_player(name):
    st.session_state['players'] = [p for p in st.session_state['players'] if p['name'] != name]

def update_score(name, score):
    for p in st.session_state['players']:
        if p['name'] == name:
            p['score'] = score

def update_tags(name, tags):
    for p in st.session_state['players']:
        if p['name'] == name:
            p['tags'] = tags

def main():
    st.set_page_config(page_title="Scoreboard", layout="centered")
    init_state()

    st.title("🏆 " + st.session_state['scoreboard_title'])
    with st.form("title_form", clear_on_submit=True):
        new_title = st.text_input("Edit scoreboard title", value=st.session_state['scoreboard_title'])
        submitted = st.form_submit_button("Update Title")
        if submitted and new_title.strip():
            st.session_state['scoreboard_title'] = new_title.strip()
            st.rerun()

    st.markdown("---")
    with st.form("add_player_form", clear_on_submit=True):
        new_player = st.text_input("Add player name")
        add_submitted = st.form_submit_button("Add Player")
        if add_submitted and new_player.strip():
            add_player(new_player.strip())
            st.rerun()

    if st.session_state['players']:
        st.markdown("### Players")
        for idx, player in enumerate(st.session_state['players']):
            cols = st.columns([2, 1, 3, 1])
            # Name and tags
            tag_str = ' '.join([f"<span style='background:#f3f4f6;padding:2px 8px;border-radius:4px;margin-right:2px;'>{t}</span>" for t in player['tags']])
            cols[0].markdown(f"{tag_str} <b>{player['name']}</b>", unsafe_allow_html=True)
            # Score
            new_score = cols[1].number_input(f"Score for {player['name']}", min_value=0, value=player['score'], key=f"score_{player['name']}")
            if new_score != player['score']:
                update_score(player['name'], new_score)
            # Tags
            new_tags = cols[2].multiselect(
                f"Tags for {player['name']}", TAGS, default=player['tags'], key=f"tags_{player['name']}"
            )
            if set(new_tags) != set(player['tags']):
                update_tags(player['name'], new_tags)
            # Remove
            if cols[3].button("❌", key=f"remove_{player['name']}"):
                remove_player(player['name'])
                st.rerun()
    else:
        st.info("No players yet. Add some!")

if __name__ == "__main__":
    main() 