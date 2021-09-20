// requires https://github.com/molnarg/js-schema
const Position = schema({
    'x': Number,
    'y': Number,
})

const NextGasArea = schema({
    'x': Number,
    'y': Number,
    'r': Number,
})

const GasArea = schema({
    'x': Number,
    'y': Number,
    'r': Number,
    'next': NextGasArea,
    'count': Number,
})

const Player = schema({
    '?pos': Position,
    'HP': Number,
    'class': ['P', 'R', 'S'], // P = blue | R = red | S = green
    'username': String,
    'mode_int': Number,
    'place': Number,
    '?inertia': Number,
    '?to': null
})

// 
const Loot = schema({
    'pos': Position,
    't': ['P', 'R', 'S'], // P = blue | R = red | S = green
    'abouttodie': Number,
})

console.table(game_state.loot)

// variable game_state
const GameState = schema({
    'cycle': schema({
        'stage': String, // ?? / ?? / 'post-game'
        'timer': Number,
    }),
    'gid': Number, // Game ID
    'gas_area': GasArea,
    'entry_cost': Number,
    'maximum_players': Number,
    'minimum_players': Number,
    'loot': schema({
        '9rxo': Loot,
    }),
    'players': schema({
        '[0-9]': Player,
    }),
    'rate': Number,
    'mode': String,
    'pregame_t': Number,
    'postgame_t': Number,
    'total_pot': Number,
    'winner': /0-9/,
    'crit_level': Number,
    'gas_damage': Number,
    'move_cost': Number,
    'gas_closes_in': Number,
    'move_speed': Number,
    'gas_speed': Number,
})

// Variable user_state
const UserState = schema({
    'loot': schema({
        '*': schema([
            String,
            Number,
            Number,
        ]),
    }),
    '?pid': Number,
    'playing': Boolean,
    'logged_in': Boolean,
    'spent': Number,
    'wallet': Number,
    'currency': String,
    'username': String,
    'discordid': String,
    'refund_address': String,
    'locked1': Number,
    'locked2': Number,
    'recovery_code': String,
    'ready': Boolean
})