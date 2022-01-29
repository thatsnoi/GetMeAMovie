import Platform from './Platform'
import netflixLogo from './logos/Netflix.png'
import primevideoLogo from './logos/primevideo.png'
import hbomaxLogo from './logos/hbomax.svg'
import disneyLogo from './logos/disney.svg'
import movistarLogo from './logos/movistar.png'

const Platforms = () => {
  return (
    <div className="relative">
      <h1 className="font-extrabold pb-2 text-2xl pl-5 md:pl-0 md:w-full md:text-center md:pb-4">
        Platform?
      </h1>
      <div
        className="flex flex-row space-x-3 overflow-x-auto overflow-y-hidden flex-nowrap pr-10 md:pr-5"
        style={{ WebkitOverflowScrolling: 'touch' }}
      >
        <div className="absolute z-40 md:hidden right-0 top-0 bottom-0 w-10 bg-gradient-to-l from-white opacity-60"></div>
        <Platform platform="Netflix" color="red" first>
          <img
            src={netflixLogo}
            alt="Netflix"
            className="py-2 p-6"
            style={{ objectFit: 'contain', height: '100%' }}
          />
        </Platform>
        <Platform platform="Prime" color="blue">
          <img
            src={primevideoLogo}
            alt="Prime"
            className="py-2 p-6"
            style={{ objectFit: 'contain', height: '100%' }}
          />
        </Platform>
        <Platform platform="Disney" color="blue">
          <img
            src={disneyLogo}
            alt="Disney+"
            className="py-1 p-6"
            style={{ objectFit: 'contain', height: '100%' }}
          />
        </Platform>
        <Platform platform="Movistar Plus" color="blue">
          <img
            src={movistarLogo}
            alt="Movistar+"
            className="py-1 p-4"
            style={{ objectFit: 'contain', height: '100%' }}
          />
        </Platform>
        <Platform platform="HBO max" color="indigo">
          <img
            src={hbomaxLogo}
            alt="HBO Max"
            className="py-1 p-6"
            style={{ objectFit: 'contain', height: '100%' }}
          />
        </Platform>
      </div>
    </div>
  )
}

export default Platforms
