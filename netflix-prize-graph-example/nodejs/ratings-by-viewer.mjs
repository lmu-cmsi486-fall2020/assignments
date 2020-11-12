import { getRatingsByViewer } from './netflix-dal.mjs'

if (process.argv.length !== 3) {
  console.log('Usage: ratings-by-viewer <viewerId>')
  process.exit(1)
}

const viewerId = process.argv[2]
try {
  const result = await getRatingsByViewer(viewerId)

  if (result.length === 0) {
    console.log(`The viewer ${viewerId} does not have any ratings in the database.`)
    process.exit(0)
  }

  result.forEach(record => {
    const rating = record.get('rating').properties
    const movie = record.get('movie').properties

    // There’s more than meets the eye here: `console.log(record, rating, movie)` to see.
    console.log(`${rating.dateRated}: “${movie.title}” got a ${rating.rating}.`)
  })
} catch (error) {
  console.error(`Sorry, something went wrong. Please ensure that “${viewerId}” is a valid viewer ID.`)
}

// Explicitly exit sync since we are asynchronous at this point.
process.exit(0)
