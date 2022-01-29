import ReactLoading from 'react-loading'

const Button = ({ onClick, className, children, loading }) => {
  return (
    <button
      onClick={onClick}
      className={
        'flex justify-center items-center rounded-2xl px-6 py-2 text-white font-bold text-xl w-36 h-12 ' +
        className
      }
    >
      {loading ? <ReactLoading type="spin" width={30} height={30} /> : children}
    </button>
  )
}

export default Button
