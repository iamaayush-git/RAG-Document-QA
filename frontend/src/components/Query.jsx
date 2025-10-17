import { useState } from "react";
import axios from "axios";
import { toast } from "react-toastify";
import { AiOutlineLoading3Quarters } from "react-icons/ai";

export default function Query() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);

  const handleQuery = async (e) => {
    e.preventDefault();
    if (!question.trim()) return;

    setLoading(true);
    setAnswer("");

    try {
      const res = await axios.post("http://localhost:8000/ask", {
        question: question,
        k: "2"
      });
      console.log(res);
      if (res.data.success === true) {
        setAnswer(res.data.answer);
      }
    } catch (err) {
      setAnswer("Error fetching answer.");
      toast.error(err.response.data.detail)
    }
    setLoading(false);
  };

  const formatted =
    typeof answer === "string"
      ? answer.replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>")
      : "";

  return (
    <div className="flex flex-col items-center mt-10 w-full  mx-auto">
      <h2 className="md:text-xl text-lg text-nowrap  font-semibold mb-4">Ask Your Documents</h2>

      <form onSubmit={handleQuery} className=" w-full flex md:flex-row flex-col items-center justify-center gap-2">
        <input
          type="text"
          className="md:w-[50%] w-[100%] border p-2 rounded"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="Type your question..."
        />
        <button disabled={loading || !question.trim()} className={`${loading || !question.trim() ? 'cursor-not-allowed opacity-50' : 'cursor-pointer'} flex items-center justify-center gap-3 px-3 py-2 bg-green-500 text-white rounded-md font-semibold cursor-pointer`} type='submit'>Ask {loading && <AiOutlineLoading3Quarters className='animate-spin' />}  </button>
      </form>

      {loading && <p className="mt-4">Thinking...</p>}
      {answer && (
        <div className="mt-4 bg-gray-100 p-3 rounded w-full">
          <p
            className="text-sm whitespace-pre-wrap"
            dangerouslySetInnerHTML={{ __html: formatted }}
          ></p>
        </div>
      )}
    </div>
  );
}
