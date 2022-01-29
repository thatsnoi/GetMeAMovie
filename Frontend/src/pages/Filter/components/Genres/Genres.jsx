import Genre from './Genre'

const Genres = () => {
  return (
    <div className="relative">
      <h1 className="font-extrabold pb-2 text-2xl pl-5 md:pl-0 md:w-full md:text-center md:pb-4">
        Genre?
      </h1>
      <div
        className="space-x-3 space-y-3 flex flex-row overflow-x-auto overflow-y-hidden pr-10 md:grid md:grid-flow-row-dense md:grid-cols-6 "
        style={{ WebkitOverflowScrolling: 'touch' }}
      >
        <div className="absolute z-40 md:hidden right-0 top-0 bottom-0 w-10 bg-gradient-to-l from-white opacity-60"></div>
        <Genre icon="🤯" first>
          Action
        </Genre>
        <Genre icon="🐘">Adventure</Genre>
        <Genre icon="🤣">Comedy</Genre>
        <Genre icon="🌍" className="truncate">
          Documentary
        </Genre>
        <Genre icon="😢">Drama</Genre>
        <Genre icon="🐉">Fantasy</Genre>
        <Genre icon="😱">Horror</Genre>
        <Genre icon="😬">Mystery</Genre>
        <Genre icon="🥰">Romance</Genre>
        <Genre icon="👽">Sci-fi</Genre>
        <Genre icon="🚁">Thriller</Genre>
        <Genre icon="🤠">Western</Genre>
      </div>
    </div>
  )
}

export default Genres
