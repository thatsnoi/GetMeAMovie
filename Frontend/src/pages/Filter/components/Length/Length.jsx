import Slider from 'rc-slider'
import 'rc-slider/assets/index.css'
import filter from '../../../../state/Filter'
import { timeConvert } from './../../../../utils/utils'

const { createSliderWithTooltip } = Slider
const Range = createSliderWithTooltip(Slider.Range)

const Length = () => {
  return (
    <div className="mx-5 pb-5 md:w-full">
      <h1 className="font-extrabold pb-2 text-2xl md:w-full md:text-center">
        Length?
      </h1>
      <div className="px-2 pr-3 pt-3">
        <Range
          tipFormatter={(value) => `${timeConvert(value)}`}
          onChange={(value) =>
            filter.setLength({ min: value[0], max: value[1] })
          }
          min={5}
          max={300}
          defaultValue={[30, 140]}
          trackStyle={[{ backgroundColor: 'rgba(12, 74, 110)' }]}
          activeDotStyle={{
            backgroundColor: 'white',
            border: 'solid 2px rgba(12, 74, 110)',
          }}
          handleStyle={[
            {
              backgroundColor: 'white',
              border: 'solid 4px rgba(12, 74, 110)',
              boxShadow: '0 0 0 0px transparant',
            },
            {
              backgroundColor: 'white',
              border: 'solid 4px rgba(12, 74, 110)',
            },
          ]}
          //   railStyle={{ backgroundColor: 'black' }}
          marks={{
            5: {
              label: '5min',
              style: {
                color: 'black',
                fontWeight: 700,
                whiteSpace: 'nowrap',
                fontSize: '0.9rem',
              },
            },
            60: {
              label: '1h',
              style: {
                color: 'black',
                fontWeight: 700,
                whiteSpace: 'nowrap',
                fontSize: '0.9rem',
              },
            },
            120: {
              label: '2h',
              style: {
                color: 'black',
                fontWeight: 700,
                whiteSpace: 'nowrap',
                fontSize: '0.9rem',
              },
            },
            180: {
              label: '3h',
              style: {
                color: 'black',
                fontWeight: 700,
                whiteSpace: 'nowrap',
                fontSize: '0.9rem',
              },
            },
            240: {
              label: '4h',
              style: {
                color: 'black',
                fontWeight: 700,
                whiteSpace: 'nowrap',
                fontSize: '0.9rem',
              },
            },
            300: {
              label: '5h',
              style: {
                color: 'black',
                fontWeight: 700,
                whiteSpace: 'nowrap',
                fontSize: '0.9rem',
              },
            },
          }}
        />
      </div>
    </div>
  )
}

export default Length
