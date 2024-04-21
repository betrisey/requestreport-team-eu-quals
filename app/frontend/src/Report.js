import axios from "axios";
import React, { useState } from "react";

function Report({ setSession }) {
  const formRef = React.useRef();
  const [url, setUrl] = useState("");
  const [result, setResult] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setResult("");
    try {
      const response = await axios.post(
        "/app/visit",
        `url=${url}`,
        {
          headers: { "Content-Type": "application/x-www-form-urlencoded" },
        }
      );
      if (response.data.success) {
        setResult("A bot has been dispatched to visit the URL");
      } else {
        setResult(response.data.error || "An error occurred");
      }
    } catch (err) {
      setResult(err.response?.data?.detail || "An error occurred");
    }
  };

  return (
    <div>
      <h2 className="text-3xl font-bold mb-4">report</h2>
      <div className="p-6 bg-white shadow-md rounded-lg">
        <form ref={formRef} onSubmit={handleSubmit} className="space-y-6">
          <input
            type="url"
            name="url"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            placeholder="https://example.com"
            required={true}
            className="input input-bordered w-full rounded-lg shadow-sm"
          />
          <button
            type="submit"
            className="btn btn-primary rounded-lg px-6 py-2 text-white bg-blue-600 hover:bg-blue-700 focus:ring-4 focus:ring-blue-300"
          >
            Submit
          </button>
          {result && <p>{result}</p>}
        </form>
      </div>
    </div>
  );
}

export default Report;
