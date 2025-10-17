import React from 'react'
import Upload from './Upload'
import Query from './Query'

const BodyComponent = () => {
  return (
    <div className='flex flex-col items-center justify-center'>
      <Upload />
      <Query />
    </div>
  )
}

export default BodyComponent