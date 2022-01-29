const Pill = ({ children }) => {
  return (
    <div className="px-4 mb-2 mr-2 text-black font-semibold bg-blue-900 bg-opacity-30  border border-gray-600 rounded-full text-xs whitespace-nowrap">
      {children}
    </div>
  )
}

export default Pill
