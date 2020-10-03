import Sequelize from 'sequelize'
const { DataTypes, Op, QueryTypes } = Sequelize

// The Sequelize documentation calls this object `sequelize` but the name `db` is used here
// to provide an analogy across various DAL examples.
const db = new Sequelize(process.env.DB_URL, {
  // This is done solely to line up the sample program output with other DAL examples.
  // In reality, having logging activated is pretty useful.
  logging: false
})

// Raw SQL-style implementation of a rating query.
const getRatingsByViewer = async (viewerId, limit = 100) => {
  return await db.query(
    `SELECT * FROM movie INNER JOIN rating ON movie.id = rating.movie_id
     WHERE viewer_id = ${viewerId}
     ORDER BY rating.date_rated, movie.title
     LIMIT ${limit}`,
    {
      type: QueryTypes.SELECT
    }
  )
}

// Raw SQL-style implementation of a movie inserter (Sequelize doesn’t have an in-between
// SQL-builder style option).
const insertMovie = async (title, year) => {
  // Watch for those apostrophes! —with raw SQL, we are responsible for proper encoding.
  const encodedTitle = title.replace(/'/g, "''")
  return (
    await db.query(
      `INSERT INTO movie (title, year) VALUES ('${encodedTitle}', ${year})
       RETURNING *`, // This is how we get the inserted row back.
      {
        type: QueryTypes.INSERT,
        plain: true
      }
    )
  )[0] // We know we are only inserting one item, and plain=true removes an additional array layer.
}

// ORM setup, Sequelize-style…
const Movie = db.define(
  'movie',
  {
    id: {
      type: DataTypes.INTEGER,
      primaryKey: true,
      autoIncrementIdentity: true
    },

    title: {
      type: DataTypes.STRING
    },

    year: {
      type: DataTypes.INTEGER
    }
  },
  {
    freezeTableName: true,
    timestamps: false
  }
)

// To stay within JavaScript naming conventions, we separate the model’s property name from
// its mapped table’s column/field name, where needed.
const Rating = db.define(
  'rating',
  {
    movieId: {
      type: DataTypes.INTEGER,
      field: 'movie_id',
      references: {
        model: Movie,
        key: 'id'
      }
    },

    viewerId: {
      type: DataTypes.INTEGER,
      field: 'viewer_id'
    },

    rating: {
      type: DataTypes.INTEGER
    },

    dateRated: {
      type: DataTypes.DATE,
      field: 'date_rated'
    }
  },
  {
    freezeTableName: true,
    timestampes: false
  }
)

// ORM-style implementation of a movie query.
const searchMoviesByTitle = async (title, limit = 100) => {
  return Movie.findAll({
    where: {
      title: {
        [Op.iLike]: `%${title}%`
      }
    },

    order: [['title', 'ASC']],
    limit
  })
}

// ORM-style implementation of an aggregate query.
const getAverageRatingOfMovie = async movieId =>
  // We know in advance that this will be a single row with a single column so we feel safe about hardcoding this.
  // A non-existent movie will yield `null` for this expression.
  await Rating.aggregate('rating', 'AVG', {
    where: {
      movieId
    },

    dataType: DataTypes.DECIMAL
  })

export { Movie, Rating, searchMoviesByTitle, getAverageRatingOfMovie, getRatingsByViewer, insertMovie }
