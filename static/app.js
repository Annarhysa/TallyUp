const TAGS = [
    '🧠 Mind Reader',
    '🎭 Master of Mystery',
    '🧊 Poker Face'
];

function fetchScoreboard() {
    fetch('/api/scoreboard')
        .then(res => res.json())
        .then(data => renderScoreboard(data));
}

function renderScoreboard(data) {
    document.getElementById('scoreboard-title').textContent = data.title;
    const tbody = document.querySelector('#scoreboard-table tbody');
    tbody.innerHTML = '';
    data.players.forEach(player => {
        const tr = document.createElement('tr');
        // Player name and tags
        const nameTd = document.createElement('td');
        nameTd.innerHTML = `${player.tags.map(t => `<span class='tag'>${t}</span>`).join(' ')} <b>${player.name}</b>`;
        tr.appendChild(nameTd);
        // Score (editable)
        const scoreTd = document.createElement('td');
        scoreTd.innerHTML = `<input type='number' class='score-input' value='${player.score}' min='0' style='width:60px;'>`;
        scoreTd.querySelector('input').addEventListener('change', (e) => {
            updateScore(player.name, parseInt(e.target.value, 10));
        });
        tr.appendChild(scoreTd);
        // Tags (select)
        const tagsTd = document.createElement('td');
        TAGS.forEach(tag => {
            const label = document.createElement('label');
            label.style.marginRight = '6px';
            const checkbox = document.createElement('input');
            checkbox.type = 'checkbox';
            checkbox.className = 'tag-select';
            checkbox.checked = player.tags.includes(tag);
            checkbox.addEventListener('change', () => {
                let newTags = [...player.tags];
                if (checkbox.checked) {
                    if (!newTags.includes(tag)) newTags.push(tag);
                } else {
                    newTags = newTags.filter(t => t !== tag);
                }
                updateTags(player.name, newTags);
            });
            label.appendChild(checkbox);
            label.appendChild(document.createTextNode(tag));
            tagsTd.appendChild(label);
        });
        tr.appendChild(tagsTd);
        // Actions
        const actionsTd = document.createElement('td');
        const delBtn = document.createElement('button');
        delBtn.textContent = 'Delete';
        delBtn.className = 'action-btn';
        delBtn.onclick = () => deletePlayer(player.name);
        actionsTd.appendChild(delBtn);
        tr.appendChild(actionsTd);
        tbody.appendChild(tr);
    });
}

function addPlayer(name) {
    fetch('/api/scoreboard/player', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name })
    }).then(res => res.json()).then(fetchScoreboard);
}

function updateScore(name, score) {
    fetch(`/api/scoreboard/player/${encodeURIComponent(name)}/score`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ score })
    }).then(res => res.json()).then(fetchScoreboard);
}

function updateTags(name, tags) {
    fetch(`/api/scoreboard/player/${encodeURIComponent(name)}/tags`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ tags })
    }).then(res => res.json()).then(fetchScoreboard);
}

function deletePlayer(name) {
    fetch(`/api/scoreboard/player/${encodeURIComponent(name)}`, {
        method: 'DELETE'
    }).then(res => res.json()).then(fetchScoreboard);
}

function setTitle(title) {
    fetch('/api/scoreboard/title', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title })
    }).then(res => res.json()).then(fetchScoreboard);
}

document.getElementById('add-player-form').addEventListener('submit', function(e) {
    e.preventDefault();
    const name = document.getElementById('player-name').value.trim();
    if (name) {
        addPlayer(name);
        document.getElementById('player-name').value = '';
    }
});

document.getElementById('title-form').addEventListener('submit', function(e) {
    e.preventDefault();
    const title = document.getElementById('title-input').value.trim();
    if (title) {
        setTitle(title);
        document.getElementById('title-input').value = '';
    }
});

// Initial load
fetchScoreboard(); 