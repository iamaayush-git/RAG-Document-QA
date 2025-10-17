import React from 'react'
import Header from './components/Header'
import BodyComponent from './components/BodyComponent'
import { ToastContainer } from 'react-toastify'

const App = () => {
  return (
    <div className='h-screen w-screen flex items-center justify-center overflow-scroll'>
      <div className='w-[80vw] h-screen overflow-auto bg-slate-200 mx-auto md:p-10 p-5'>
        <Header />
        <BodyComponent />
      </div>
      <ToastContainer />
    </div>
  )
}

export default App