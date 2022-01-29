const Pill = ({ children }) => {
  return (
    <div className="px-4 text-white font-semibold bg-gray-500  border border-gray-400 rounded-full text-sm whitespace-nowrap">
      {children}
    </div>
  )
}

export default Pill
