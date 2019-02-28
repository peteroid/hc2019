const fs = require('fs')

const inputPath = '../input/a_example.in'
// const inputPath = '../input/a_tiny.in'
// const inputPath = '../input/b_small.in'

let result = { count: 0, slices: [] }
function main () {
  // parse the input
  const input = fs.readFileSync(process.argv[2] || inputPath)
  const [config, ...lines] = String(input).split('\n')
  const [row, col, low, high] = config.split(' ').map(s => Number(s))
  const cells = lines.filter(Boolean).map(s => s.split(''))
  console.log(row, col, low, high)
  console.log(cells)

  // calculate
  timeStart('main')
  walk(cells, low, high, 0, 0, 1, 1, [])
  while (queue.length > 0) {
    const nextArgs = queue.pop()
    _walk(...nextArgs)

    // shortcut if we found the best answer
    // if (result.count === row * col) break
  }
  timeEnd('main')

  console.log(timeMarks)

  console.log(result)
  console.log(`walked: ${walkCount}`)
  console.log(`processed: ${processCount}`)

  console.log('Output:')
  console.log(result.slices.length)
  result.slices.forEach(([r, c, row, col]) => console.log(r, c, r + row - 1, c + col - 1))
}

const queue = []
let walkCount = 0
let processCount = 0
const walked = new Set()
const labels = new Map()

const timeMarks = {}
function timeStart (s = '') {
  timeMarks[s] = (timeMarks[s] || 0) - Date.now()
}
function timeEnd (s = '') {
  timeMarks[s] = (timeMarks[s] || 0) + Date.now()
}

function walk (pizza = [['']], low = 0, high = 0, r = 0, c = 0, row = 0, col = 0, slices = [[0]], cellCount = 0) {
  walkCount++
  if (r + row > pizza.length || c + col > pizza[0].length || row * col > high) {
    return
  }
  queue.push([pizza, low, high, r, c, row, col, slices, cellCount])
}

function _walk (pizza = [['']], low = 0, high = 0, r = 0, c = 0, row = 0, col = 0, slices = [[0]], cellCount = 0) {
  // console.log('work', r, c, row, col, result)

  timeStart('count')
  const counts = { T: 0, M: 0 }
  for (let i = 0; i < row; i++) {
    for (let j = 0; j < col; j++) {
      const cell = pizza[r + i][c + j]
      if (cell === 'T') {
        counts.T++
      } else if (cell === 'M') {
        counts.M++
      } else {
        // if slice contains taken cell, skip
        timeEnd('count')
        return
      }
    }
  }
  timeEnd('count')

  // console.log(counts, r, c, row, col)
  if (counts.T + counts.M > high) {
    // the slice has too much topping
    return
  }

  // skip for walked label
  timeStart('label')

  timeStart('plabel')
  // let label = ''
  // for (let i = 0; i < pizza.length; i++) {
  //   for (let j = 0; j < pizza[0].length; j++) {
  //     const cell = pizza[i][j]
  //     label += (cell === 'T' || cell === 'M') ? '.' : '-'
  //   }
  // }
  // label += ('_' + r)
  // label += ('_' + c)
  // label += ('_' + row)
  // label += ('_' + col)


  let pizzaLabel = labels.get(pizza)
  if (!pizzaLabel) {
    pizzaLabel = pizza.map(row => row.join('')).join('')
    labels.set(pizza, pizzaLabel)
  }

  // let pizzaLabel = pizza.map(row => row.join('')).join('')
  timeEnd('plabel')

  const label = [pizzaLabel, r, c, row, col].join('_')

  timeEnd('label')
  if (walked.has(label)) return
  walked.add(label)

  processCount++

  walk(pizza, low, high, r, c, row + 1, col, slices, cellCount)
  walk(pizza, low, high, r, c, row, col + 1, slices, cellCount)

  if (counts.T >= low && counts.M >= low) {
    // possible slice, try to expand from here too
    timeStart('pre-ok')
    const leftover = pizza.map(row => row.slice())

    for (let i = 0; i < row; i++) {
      for (let j = 0; j < col; j++) {
        // leftover[r + i][c + j] = '' + slices.length
        leftover[r + i][c + j] = 'O'
      }
    }

    const newSlices = [...slices, [r, c, row, col]]
    const newCellCount = cellCount + row * col
    if (newCellCount > result.count) {
      result.count = newCellCount
      result.slices = newSlices
      // console.log(result.count)
    }
    timeEnd('pre-ok')

    outer:
    for (let i = 0; i < pizza.length; i++) {
      for (let j = 0; j < pizza[0].length; j++) {
        const cell = leftover[i][j]
        if (cell === 'M' || cell === 'T') {
          walk(leftover, low, high, i, j, 1, 1, newSlices, newCellCount)
          break outer
        }
      }
    }

    // console.log(leftover)
  }
}

main()
