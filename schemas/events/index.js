// requires https://github.com/molnarg/js-schema

// var Duck = schema({
//   swim: Function,
//   quack: Function,
//   age: Number.min(0).max(5),
//   color: ['yellow', 'brown']
// })

const Tip = schema({
  name: String, // name of the sender
  amount: Number, // amount of the tip
  count: Number, // number of tips since start of session
})
