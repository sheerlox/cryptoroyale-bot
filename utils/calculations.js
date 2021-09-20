const calcDistance = (c1, c2) => {
  return Math.sqrt(Math.pow(c1.x - c2.x, 2) + Math.pow(c1.y - c2.y, 2))
}

const inGas = (p, size, game_state, RenderRes) => {
  if (!p) return false

  return calcDistance(p.pos, game_state.gas_area) + size / 3 > game_state.gas_area.r * 100 * (RenderRes || 1)
}

let insideGas = inGas(p, calcSize(p.HP), game_state)

const calcSize = (health) => {
  return Math.log2(Math.max(20, health)) * 7.5
}
