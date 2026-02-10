import { useState } from "react";
import api from "../api/axios";

function UploadCSV({summary,setSummary}) {
  const [file, setFile] = useState(null);

  const handleUpload = async () => {
    if (!file) return alert("Select a file");

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await api.post("upload/", formData);
      setSummary(res.data.summary);
    } catch (err) {
      alert("Upload failed");
    }
  };

  return (
    <div>
      <input type="file" onChange={(e) => setFile(e.target.files[0])} />
      <button onClick={handleUpload}>Upload CSV</button>

      {summary && (
        <div>
          <h3>Summary</h3>
          <pre>{JSON.stringify(summary, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}

export default UploadCSV;
