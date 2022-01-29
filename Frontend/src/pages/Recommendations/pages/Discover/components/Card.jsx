import React, { useRef, useEffect, useState } from 'react'
import { motion, useMotionValue, useAnimation } from 'framer-motion'
import styled from '@emotion/styled'
import Pill from '../../../../../components/Pill'
import { timeConvert } from '../../../../../utils/utils'
import recommendations from '../../../../../state/Recommendations'
import { observer } from 'mobx-react-lite'
import { useKeyPress } from 'react-use'

const StyledCard = styled(motion.div)`
  position: fixed;
`

export const Card = observer(
  ({ movie, children, style, onVote, id, index, ...props }) => {
    // motion stuff
    const cardElem = useRef(null)

    const x = useMotionValue(0)
    const controls = useAnimation()

    const [constrained, setConstrained] = useState(true)

    const [direction, setDirection] = useState()

    const [velocity, setVelocity] = useState()

    const left = useKeyPress(37)
    const right = useKeyPress(39)

    const getVote = (childNode, parentNode) => {
      const childRect = childNode.getBoundingClientRect()
      const parentRect = parentNode.getBoundingClientRect()
      let result =
        parentRect.left >= childRect.right
          ? false
          : parentRect.right <= childRect.left
          ? true
          : undefined
      return result
    }

    // determine direction of swipe based on velocity
    const getDirection = () => {
      return velocity >= 1 ? 'right' : velocity <= -1 ? 'left' : undefined
    }

    const getTrajectory = () => {
      setVelocity(x.getVelocity())
      setDirection(getDirection())
    }

    const flyAway = (min) => {
      if (cardElem.current) {
        const flyAwayDistance = (direction) => {
          const parentWidth =
            cardElem.current.parentNode.getBoundingClientRect().width
          const childWidth = cardElem.current.getBoundingClientRect().width
          return direction === 'left'
            ? -parentWidth / 2 - childWidth / 2
            : parentWidth / 2 + childWidth / 2
        }
        if (direction && Math.abs(velocity) > min) {
          setConstrained(false)
          controls.start({
            x: flyAwayDistance(direction),
          })
        }
      }
    }

    useEffect(() => {
      const unsubscribeX = x.onChange(() => {
        if (cardElem.current) {
          const childNode = cardElem.current
          const parentNode = cardElem.current.parentNode
          const result = getVote(childNode, parentNode)
          result !== undefined && onVote(result)
        }
      })

      return () => unsubscribeX()
    })

    const flyAwayManual = (direction) => {
      const flyAwayDistance = (direction) => {
        const parentWidth =
          cardElem.current.parentNode.getBoundingClientRect().width
        const childWidth = cardElem.current.getBoundingClientRect().width
        return direction === 'left'
          ? -parentWidth / 2 - childWidth / 2
          : parentWidth / 2 + childWidth / 2
      }
      if (direction) {
        setConstrained(false)
        controls.start({
          x: flyAwayDistance(direction),
        })
      }
    }

    useEffect(() => {
      if (
        left[1]?.type === 'keyup' &&
        left[1]?.key === 'ArrowLeft' &&
        index === 0
      ) {
        flyAwayManual('left')
      }
      // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [left])

    useEffect(() => {
      if (
        right[1]?.type === 'keyup' &&
        right[1]?.key === 'ArrowRight' &&
        index === 0
      ) {
        flyAwayManual('right')
      }
      // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [right])

    let showDetails = recommendations.showMovieDetails === movie.id

    const toTop = async () => {
      controls.start({
        maxWidth: null,
      })
      await controls.start({
        top: 'calc(-100% + 17rem)',
        left: 0,
        right: 0,
        width: '100%',
        maxWidth: null,
      })
    }

    const toNormal = async () => {
      await controls.start({
        margin: 'auto',
        top: 'calc(0% + 5rem)',
        left: 0,
        right: 0,
        width: '90%',
        maxWidth: '400px',
      })
    }

    return (
      <StyledCard
        drag={!recommendations.showContent}
        animate={controls}
        dragConstraints={
          constrained && { left: 0, right: 0, top: 0, bottom: 0 }
        }
        dragElastic={1}
        ref={cardElem}
        onDrag={getTrajectory}
        onDragEnd={() => flyAway(100)}
        whileTap={{ scale: 1.1 }}
        style={{
          WebkitBackgroundSize: 'cover',
          MozBackgroundSize: 'cover',
          OBackgroundSize: 'cover',
          backgroundSize: 'cover',
          backgroundImage: `url("${movie.thumbnail}")`,
          height: 'calc(100% - 12rem)',
          width: '90%',
          maxWidth: '400px',
          margin: 'auto',
          top: 'calc(0% + 5rem)',
          left: 0,
          right: 0,
          x,
        }}
        onClick={async () => {
          if (direction && Math.abs(velocity) > 0) {
            return
          }

          // Special case if animation is ongoing
          if (
            !recommendations.showContent &&
            recommendations.showMovieDetails
          ) {
            recommendations.setShowMovieDetails(movie.id)
            recommendations.showContent = true
            await toTop()
            recommendations.setShowMovieDetails(movie.id)
            return
          }
          if (!showDetails) {
            toTop()
            recommendations.toggleShowContent()
            recommendations.setShowMovieDetails(movie.id)
          } else {
            recommendations.toggleShowContent()
            await toNormal()
            recommendations.setShowMovieDetails(undefined)
          }
        }}
        className={`relative rounded-2xl h-full z-50 cursor-pointer transition-shadow ${
          !!recommendations.showMovieDetails && !showDetails ? 'hidden' : ''
        } ${index === 0 || index === 1 ? 'shadow-2xl' : 'shadow-none'}`}
        {...props}
      >
        <div
          className={`absolute bottom-0 left-0 right-0 h-32 bg-gradient-to-t from-gray-900 rounded-b-2xl flex flex-col justify-end p-4 pr-0`}
        >
          <div>
            <p className="text-white text-2xl font-extrabold truncate">
              {movie.title + ' (' + movie.year + ')'}
            </p>
          </div>

          <div className="flex pt-1 space-x-2 overflow-hidden">
            <Pill>{movie.averageUserScore}</Pill>
            <Pill>{timeConvert(movie.duration)}</Pill>
            {movie.genres.map((genre, i) => {
              return <Pill key={i}>{genre}</Pill>
            })}
          </div>
        </div>
      </StyledCard>
    )
  }
)
