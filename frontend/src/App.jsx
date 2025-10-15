import React from 'react'
import Header from './components/Header'
import BodyComponent from './components/BodyComponent'
import { ToastContainer } from 'react-toastify'

const App = () => {
  return (
    <div className='h-screen w-screen flex items-center justify-center'>
      <div className='w-[80vw] h-[80vh] bg-slate-200 mx-auto p-10 overflow-hidden'>
        <Header />
        <BodyComponent />
      </div>
      <ToastContainer />
    </div>
  )
}

export default App