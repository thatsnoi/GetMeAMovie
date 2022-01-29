import React from 'react'
import { Card } from './Card'
import styled from '@emotion/styled'
import recommendations from '../../../../../state/Recommendations'
import { observer } from 'mobx-react-lite'

const Frame = styled.div`
  width: 100%;
  overflow: hidden;
  display: flex;
  justify-content: center;
  align-items: start;
  position: relative;
  height: calc(100% + 5rem);
`
export const Stack = observer(({ onVote, children, ...props }) => {
  const handleVote = (vote) => {
    onVote(recommendations.pop(), vote)
  }

  return (
    <Frame>
      {recommendations.movieStack.map((movie, index) => {
        let isTop = index === recommendations.movieStack.length - 1
        let i = recommendations.movieStack.length - index - 1
        return (
          <Card
            drag={isTop} // Only top card is draggable
            key={movie.id}
            onVote={(result) => handleVote(result)}
            movie={movie}
            index={i}
            data-value={movie.id}
            whileTap={{ scale: 1.15 }}
          />
        )
      })}
    </Frame>
  )
})
