import { observer } from 'mobx-react-lite'
import { FiHeart } from 'react-icons/fi'
import { Link } from 'react-router-dom'
import recommendations from '../../../../../state/Recommendations'

const End = observer(() => {
  return (
    <>
      {recommendations.movieStack.length === 0 && (
        <div
          className={'w-full fixed overflow-hidden'}
          style={{ height: '100vh', top: '40%' }}
        >
          <div className="flex flex-col items-center justify-center space-y-2">
            <h3 className="font-extrabold text-2xl text-gray-900">
              That's all from us...
            </h3>
            <p className="font-medium text-md text-gray-600  -mt-2">
              Have a look at the movies you liked:
            </p>
            <Link
              className={`flex flex-col items-center text-gray-600 hover:text-red-600 transition-all`}
              to="/recommendations/liked"
            >
              <FiHeart size="2rem" />
            </Link>
          </div>
        </div>
      )}
    </>
  )
})

export default End
