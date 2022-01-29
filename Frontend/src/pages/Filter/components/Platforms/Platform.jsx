import filter from '../../../../state/Filter'
import { observer } from 'mobx-react-lite'

const Platform = observer(
  ({ logo, color, platform, dark, first, ...props }) => {
    const _color = filter.platforms.includes(platform) ? color : 'gray'

    return (
      <div
        className={`relative p-1 rounded-2xl cursor-pointer w-40 md:w-32 lg:w-40 ${
          'bg-' + _color + (dark ? '-800' : '-200')
        } ${first ? 'ml-5' : ''} space-y-1`}
        style={{ flex: '0 0 auto' }}
      >
        <div
          className={`flex flex-col items-center justify-center h-12 ${
            filter.platforms.includes(platform) ? '' : 'filter grayscale'
          }`}
        >
          {props.children}
        </div>
        <div
          className={`absolute top-0 bottom-0 left-0 rounded-2xl right-0 z-50 bg-transparent cursor-pointer`}
          onClick={() => filter.togglePlatform(platform)}
        ></div>
      </div>
    )
  }
)

export default Platform
