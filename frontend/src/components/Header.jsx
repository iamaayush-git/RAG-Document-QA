import React from 'react'

const Header = () => {
  return (
    <div className=''>
      <h3 className='md:text-2xl text-xl md:font-bold font-semibold text-green-600 text-center'>DOCUMENT-QA</h3>
      <p className='text-green-700 md:font-md font-light md:text-center text-left md:mt-5 mt-3 '>Upload your TXT, PDF or MD files and instantly ask questions across all your documents. Powered by LangChain, FAISS vector search, and local AI — fast, private, and efficient.</p>
    </div>
  )
}

export default Header