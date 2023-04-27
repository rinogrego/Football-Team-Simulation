document.addEventListener("DOMContentLoaded", () => {

    // generate form

    // fetch available players
    localStorage.removeItem("availablePlayers");
    fetch("api/database/players/")
    .then(response => response.json())
    .then(data => {
        localStorage.setItem("availablePlayers", JSON.stringify(data))
    })

    // fetch available players based on chosen team
    localStorage.removeItem("availablePlayersByTeam");
    fetch("api/database/teams/")
    .then(response => response.json())
    .then(data => {
        localStorage.setItem("availablePlayersByTeam", JSON.stringify(data))
    })
    
    // fetch available positions
    localStorage.removeItem("availablePositions");
    fetch("api/database/positions/")
    .then(response => response.json())
    .then(data => {
        localStorage.setItem("availablePositions", JSON.stringify(data));
    })
  
    // fetch available positions by formations
    localStorage.removeItem("availablePositions");
    fetch("api/database/formations/")
    .then(response => response.json())
    .then(data => {
        localStorage.setItem("availablePositionsByFormation", JSON.stringify(data));
    })
  
})


function generatePlayerSelection(id){
    const select_tag = document.querySelector(`#${id}`);

    // to prevent repeated creation of displayPlayerOptions
    var current_options = select_tag.children;
    var array_current_options = Array.from(current_options);
    var available_options = [];
    array_current_options.forEach(e => {
        if (e.value !== "") {
            available_options.push(e.value)
        }
    })

    const displayPlayerOptions = async () => {
        const players = JSON.parse(localStorage.getItem("availablePlayers"));
        players.forEach(player => {
            if (available_options.includes(player) === false) {
                const player_option = document.createElement('option');
                player_option.value = `${player}`;
                player_option.innerHTML = `${player.replace('-', ' ')}`;
                select_tag.appendChild(player_option);
            }
        })
    }

    displayPlayerOptions();
}


function generatePositionSelection(id){
    const select_tag = document.querySelector(`#${id}`);
    
    // to prevent repeated creation of displayPositionOptions
    var current_options = select_tag.children;
    var array_current_options = Array.from(current_options);
    var available_options = [];
    array_current_options.forEach(e => {
        if (e.value !== "") {
            available_options.push(e.value)
        }
    })

    const displayPositionOptions = async () => {
        const options = JSON.parse(localStorage.getItem("availablePositions"));
        options.forEach(position => {
            if (available_options.includes(position) === false) {
                const position_option = document.createElement('option');
                position_option.value = `${position}`;
                position_option.innerHTML = `${position}`;
                select_tag.appendChild(position_option);
            }
        })
    }

    displayPositionOptions();
}


function generatePlayersByTeam(id){
    const select_tag = document.querySelector(`#${id}`);

    // to prevent repeated creation of displayTeamOptions
    var current_options = select_tag.children;
    var array_current_options = Array.from(current_options);
    var available_options = [];
    array_current_options.forEach(e => {
        if (e.value !== "") {
            available_options.push(e.value)
        }
    })

    const displayTeamOptions = async () => {
        const teams = JSON.parse(localStorage.getItem("availablePlayersByTeam"))
        Object.keys(teams).forEach(team => {
            if (available_options.includes(team) === false) {
                const team_option = document.createElement('option');
                team_option.value = `${team}`;
                team_option.innerHTML = `${team.replace('-', ' ')}`;
                select_tag.appendChild(team_option);
            }
        })
    }

    displayTeamOptions();
}


function displayPlayersByTeam(teamname, team) {
    const team_database = JSON.parse(localStorage.getItem("availablePlayersByTeam"));
    const players = team_database[teamname];

    // load players by choosen team
    Object.keys(players).forEach(player => {
        var id = `${team}-${player}`;
        document.getElementById(id).innerHTML = `
        <option value="${players[player]}">${players[player]}</option>
        `;
    })
    
}


function generatePositionsByFormation(id){
    const select_tag = document.querySelector(`#${id}`);

    // to prevent repeated creation of displayFormationOptions
    var current_options = select_tag.children;
    var array_current_options = Array.from(current_options);
    var available_options = [];
    array_current_options.forEach(e => {
        if (e.value !== "") {
            available_options.push(e.value)
        }
    })

    const displayFormationOptions = async () => {
        const formations = JSON.parse(localStorage.getItem("availablePositionsByFormation"))
        Object.keys(formations).forEach(formation => {
            if (available_options.includes(formation) === false) {
                const formation_option = document.createElement('option');
                formation_option.value = `${formation}`;
                formation_option.innerHTML = `${formation}`;
                select_tag.appendChild(formation_option);
            }
        })
    }

    displayFormationOptions();
}


function displayPositionsByFormation(formation, team) {
    const formations = JSON.parse(localStorage.getItem("availablePositionsByFormation"));
    const positions = formations[formation];

    // load positions by choosen formation
    Object.keys(positions).forEach(player => {
        var id = `${team}-${player}-position`;
        // suggestion: maybe for each id, generate every available positions but if the pos matched with 
        // the current pos in the looping, then add 'selected' inside the option tag

        document.getElementById(id).innerHTML = `
        <option value="${positions[player]}">${positions[player]}</option>
        `;
    })
    
}

