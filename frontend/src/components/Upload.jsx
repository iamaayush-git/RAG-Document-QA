import React, { useEffect, useRef, useState } from 'react'
import axios from "axios"
import { AiOutlineLoading3Quarters } from "react-icons/ai";
import { toast, ToastContainer } from 'react-toastify';

const Upload = () => {
  const [file, setFile] = useState(null)
  const fileInputRef = useRef(null)
  const [error, setError] = useState("")
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    if (file) {
      setError("")
    }
  }, [file])


  const submit = async (e) => {
    e.preventDefault()
    setLoading(true)
    try {
      if (!file) {
        setLoading(false)
        return setError("Please upload file")
      }
      const formData = new FormData();
      formData.append("file", file)

      const response = await axios.post("http://localhost:8000/ingest", formData, { headers: { "Content-Type": "multipart/form-data" } })
      if (response.data.success === true) {
        toast.success("File ingested successfully.")
      }

    } catch (err) {
      toast.error(err.response?.data?.detail[0].msg || "Internal server error");
    }
    setLoading(false)
  }


  return (
    <div>
      <form onSubmit={submit}>
        <input ref={fileInputRef} className='hidden' type="file" onChange={(e) => setFile(e.target.files[0])} />
        <div onClick={() => fileInputRef.current.click()} className='border md:h-20 md:w-20 md:p-2 p-1 h-15 w-15 rounded-md cursor-pointer mt-4 flex items-center justify-center' >
          <p
            className="text-black md:text-sm text-sm font-light text-left overflow-hidden whitespace-nowrap text-ellipsis max-w-full"
            title={file ? file.name : "Upload File"}
          >
            {file ? file.name : "Upload File"}
          </p>
        </div>
        <button disabled={loading} className={`${loading ? 'cursor-not-allowed opacity-50' : 'cursor-pointer'} flex items-center justify-center gap-3 px-3 py-2 bg-green-500 text-white rounded-md font-semibold mt-5 cursor-pointer`} type='submit'>Upload {loading && <AiOutlineLoading3Quarters className='animate-spin' />}  </button>
      </form>
      {error && <p className='font-semibold text-red-500 md:text-md text-sm'>Error: {error}</p>}
    </div>
  )
}

export default Upload