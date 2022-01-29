import filter from '../../../../state/Filter'
import { observer } from 'mobx-react-lite'

const Genre = observer(({ icon, first, ...props }) => {
  return (
    <div
      className={`relative flex flex-col items-center justify-center py-4 px-1 rounded-2xl cursor-pointer ${
        filter.genres.includes(props.children) ? 'bg-blue-600' : 'bg-blue-900'
      } ${first ? 'ml-5' : ''} space-y-1`}
    >
      <span className="text-4xl">{icon}</span>
      <h4
        className={'text-white font-bold w-20 text-center ' + props.className}
      >
        {props.children}
      </h4>
      <div
        className="absolute top-0 bottom-0 left-0 right-0 z-50 bg-transparent cursor-pointer rounded-2xl"
        onClick={() => filter.toggleGenre(props.children)}
      ></div>
    </div>
  )
})

export default Genre
