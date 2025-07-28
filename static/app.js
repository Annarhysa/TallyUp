// Scoreboard JavaScript functionality

// Toggle edit panel for a player
function toggleEdit(playerName) {
    const editPanel = document.getElementById(`edit-${playerName}`);
    if (editPanel.style.display === 'none') {
        editPanel.style.display = 'block';
    } else {
        editPanel.style.display = 'none';
    }
}

// Add a new player
async function addPlayer(event) {
    event.preventDefault();
    const playerName = document.getElementById('new-player-name').value.trim();
    
    if (!playerName) return;
    
    try {
        const response = await fetch('/add_player', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ name: playerName })
        });
        
        if (response.ok) {
            window.location.reload();
                } else {
            alert('Error adding player');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error adding player');
    }
}

// Update player information
async function updatePlayer(event, playerName) {
    event.preventDefault();
    const form = event.target;
    const score = parseInt(form.score.value);
    const tags = Array.from(form.tags.selectedOptions).map(option => option.value);
    
    try {
        const response = await fetch('/update_player', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                name: playerName,
                score: score,
                tags: tags
            })
        });
        
        if (response.ok) {
            window.location.reload();
        } else {
            alert('Error updating player');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error updating player');
    }
}

// Delete a player
async function deletePlayer(playerName) {
    if (!confirm(`Are you sure you want to delete ${playerName}?`)) {
        return;
    }
    
    try {
        const response = await fetch('/delete_player', {
        method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ name: playerName })
        });
        
        if (response.ok) {
            window.location.reload();
        } else {
            alert('Error deleting player');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error deleting player');
    }
}

// Update dashboard title
async function updateTitle(event) {
    event.preventDefault();
    const newTitle = document.getElementById('new-title').value.trim();
    
    if (!newTitle) return;
    
    try {
        const response = await fetch('/update_title', {
        method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ title: newTitle })
        });
        
        if (response.ok) {
            window.location.reload();
        } else {
            alert('Error updating title');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error updating title');
    }
}

// Reset all data
async function resetAll() {
    if (!confirm('Are you sure you want to reset all data? This action cannot be undone.')) {
        return;
    }
    
    try {
        const response = await fetch('/reset_all', {
        method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        });
        
        if (response.ok) {
            window.location.reload();
        } else {
            alert('Error resetting data');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error resetting data');
    }
}

// Auto-refresh statistics every 30 seconds
setInterval(() => {
    fetch('/get_stats')
        .then(response => response.json())
        .then(data => {
            // Update statistics without full page reload
            const statCards = document.querySelectorAll('.stat-value');
            if (statCards.length >= 3) {
                statCards[0].textContent = data.total_players;
                statCards[1].textContent = data.total_score;
                statCards[2].textContent = data.avg_score.toFixed(1);
            }
        })
        .catch(error => console.error('Error updating stats:', error));
}, 30000);

// Initialize tooltips and other UI enhancements
document.addEventListener('DOMContentLoaded', function() {
    // Add smooth scrolling
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });
    
    // Add keyboard shortcuts
    document.addEventListener('keydown', function(e) {
        // Ctrl/Cmd + N to focus on new player input
        if ((e.ctrlKey || e.metaKey) && e.key === 'n') {
    e.preventDefault();
            document.getElementById('new-player-name').focus();
        }
        
        // Escape to close edit panels
        if (e.key === 'Escape') {
            document.querySelectorAll('.edit-panel').forEach(panel => {
                panel.style.display = 'none';
            });
        }
    });
    
    // Auto-focus on new player input when page loads
    const newPlayerInput = document.getElementById('new-player-name');
    if (newPlayerInput) {
        newPlayerInput.focus();
    }
}); 