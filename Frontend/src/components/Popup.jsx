const Popup = ({ children }) => {
  return (
    <div
      className="fixed flex justify-center items-end md:items-center left-0 right-0 top-0  blur-2xl h-full p-3"
      style={{
        zIndex: 100,
        backdropFilter: 'blur(2px)',
        marginTop: '-10px',
      }}
    >
      <div className="flex flex-col justify-evenly items-center h-auto w-full md:w-1/2 rounded-2xl bg-white shadow-2xl px-10 py-5 ring ring-blue-900">
        {children}
      </div>
    </div>
  )
}

export default Popup
