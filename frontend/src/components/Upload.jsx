import React, { useRef, useState } from 'react'
import axios from "axios"
import { AiOutlineLoading3Quarters } from "react-icons/ai";
import { toast, ToastContainer } from 'react-toastify';
import ConfirmModal from './ConfirmModel.jsx';

const Upload = () => {
  const [file, setFile] = useState(null)
  const fileInputRef = useRef(null)
  const [error, setError] = useState("")
  const [loading, setLoading] = useState(false)
  const [clearContextLoading, setClearContextLoading] = useState(false)
  const [open, setOpen] = useState(false)


  const submit = async (e) => {
    e.preventDefault()
    setLoading(true)
    try {
      if (!file) {
        setLoading(false)
        return setError("Please select file.")
      }
      const formData = new FormData();
      formData.append("file", file)

      const response = await axios.post("http://localhost:8000/ingest", formData, {
        headers:
          { "Content-Type": "multipart/form-data" }
      })
      console.log(response)
      if (response.data.success === true) {
        toast.success("File ingested successfully.")
      }

    } catch (err) {
      toast.error(err.response?.data?.detail[0].msg || "Internal server error");
    }
    setLoading(false)
  }

  const clear_context = async () => {
    try {
      setClearContextLoading(true);
      const respnse = await axios.post("http://localhost:8000/reset");
      if (respnse.data.success === true) {
        toast.success("Context cleared successfully!");
      }
      setOpen(false);
    } catch {
      toast.error("Error clearing context");
    } finally {
      setClearContextLoading(false);
    }
  }


  return (
    <div className=''>
      <form className='flex items-center justify-center flex-col'>
        <input ref={fileInputRef} className='hidden' type="file" onChange={(e) => setFile(e.target.files[0])} />
        <div onClick={() => fileInputRef.current.click()} className='border md:h-20 md:w-20 md:p-2 p-1 h-15 w-15 rounded-md cursor-pointer mt-4 flex items-center justify-center' >
          <p
            className="text-black md:text-sm text-sm font-light text-left overflow-hidden whitespace-nowrap text-ellipsis max-w-full"
            title={file ? file.name : "Upload File"}
          >
            {file ? file.name : "Upload File"}
          </p>
        </div>
        <div className='flex items-center justify-center gap-5'>
          <button disabled={loading} className={`${loading ? 'cursor-not-allowed opacity-50' : 'cursor-pointer'} flex items-center justify-center gap-3 px-3 py-2 bg-green-500 text-white rounded-md font-semibold mt-5 cursor-pointer`} onClick={submit}>Upload {loading && <AiOutlineLoading3Quarters className='animate-spin' />}  </button>

          <button disabled={clearContextLoading} className={`${clearContextLoading ? 'cursor-not-allowed opacity-50' : 'cursor-pointer'} flex items-center justify-center gap-3 px-3 py-2 bg-red-500 text-white rounded-md font-semibold mt-5 cursor-pointer`} onClick={(e) => { e.preventDefault(); setOpen(true) }} >Clear Context {clearContextLoading && <AiOutlineLoading3Quarters className='animate-spin' />}  </button>



        </div>
      </form>
      {error && <p className='font-semibold text-red-500 md:text-md text-sm'>Error: {error}</p>}
      <ConfirmModal
        open={open}
        setOpen={setOpen}
        title="Confirm Action"
        message="Are you sure want to clear all context?"
        onConfirm={clear_context}
        loading={clearContextLoading}
      />
    </div>
  )
}

export default Upload