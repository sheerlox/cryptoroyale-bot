socket.onAny(
  (event, data) => {
    if (['p'].includes(event)) console.log(event, data)
  }
)

console.log(game_state)

let buffer = [];
(function loop() {
  setTimeout(function () {
    buffer.push(game_state)
    loop()
  }, 1000)
}())

JSON.stringify(buffer)

console.table(game_state.loot)

// ---------------------
// ------ LOOPING ------
// ---------------------
function logPlayers() {
  console.table(Object.values(game_state.players).map((player) => {
    return {
      'username': player.username,
      'class': player.class,
      'HP': player.HP,
      'mode_int': player.mode_int,
      'place': player.place,
      'xPos': player.pos && player.pos.x,
      'xTo': player.to && player.to.x,
      'yPos': player.pos && player.pos.y,
      'yTo': player.to && player.to.y,
    }
  }))
}

function logLoots() {
  console.table(Object.values(game_state.loot).map((loot) => {
    return {
      'xPos': loot.pos.x,
      'yPos': loot.pos.x,
      't': loot.t, // P = blue | R = red | S = green
      'abouttodie': loot.abouttodie
    }
  }))
}

function tick () {
  setTimeout(function () {
    console.clear()
    console.log(game.input.x, game.input.y)
    logPlayers()
    logLoots()

    tick()
  }, 500)
}

tick()
