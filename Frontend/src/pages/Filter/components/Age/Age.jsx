import Slider from 'rc-slider'
import 'rc-slider/assets/index.css'
import filter from '../../../../state/Filter'

const Range = Slider.Range;

const Age = () => {
  return (
    <div className="mx-5 md:w-full">
      <h1 className="font-extrabold pb-2 text-2xl md:w-full md:text-center">
        Age?
      </h1>
      <div className="px-2 pr-3 pt-3">
        <Range
          onChange={(value) => filter.setAge({min: value[0], max: value[1]})}
          step={null}
          min={0}
          max={18}
          defaultValue={[0, 18]}
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
          marks={{
            0: {
              label: '0',
              style: {
                color: 'black',
                fontWeight: 700,
                whiteSpace: 'nowrap',
                fontSize: '0.9rem',
              },
            },
            6: {
              label: '6',
              style: {
                color: 'black',
                fontWeight: 700,
                whiteSpace: 'nowrap',
                fontSize: '0.9rem',
              },
            },
            12: {
              label: '12',
              style: {
                color: 'black',
                fontWeight: 700,
                whiteSpace: 'nowrap',
                fontSize: '0.9rem',
              },
            },
            16: {
              label: '16',
              style: {
                color: 'black',
                fontWeight: 700,
                whiteSpace: 'nowrap',
                fontSize: '0.9rem',
              },
            },
            18: {
              label: '18',
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

export default Age
