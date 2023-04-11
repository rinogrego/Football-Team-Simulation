document.addEventListener("DOMContentLoaded", () => {

  
})


function generate_position_selection(id){
    // Thanks: https://stackoverflow.com/questions/68223406/how-to-create-select-dropdown-in-javascript-with-fetched-data-from-api
    
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

    const getPositions = async() => {
        const response = await fetch("api/database/positions");
        const data = response.json();
        return data
    }

    const displayPositionOptions = async () => {
        const options = await getPositions();
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


function generate_player_selection(id){
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

    const getPlayers = async() => {
        const response = await fetch("api/database/players");
        const data = response.json();
        return data
    }

    const displayPlayerOptions = async () => {
        const players = await getPlayers();
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


function generate_entries(team){
    
}