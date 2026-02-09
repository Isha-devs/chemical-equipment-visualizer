import React, { useEffect, useState } from "react";
import API from "../api/axios";

const History = () => {
    const [history, setHistory] = useState([]);

    useEffect(() => {
        API.get("history/")
        .then((res) => setHistory(res.data))
        .catch((err) => console.error(err));
    }, []);


    return (
        <div>
            <h2>Upload History (Last 5)</h2>

            <table border = "1" cellPadding="8">
                <thead>
                    <tr>
                        <th>Filename</th>
                        <th>Upload At</th>
                        <th>Total Equipment</th>
                    </tr>
                </thead>
                <tbody>
                    {history.map((item, index) => (
                        <tr key = {index}>
                            <td>{item.filename}</td>
                            <td>{new Date(item.uploaded_at).toLocaleString()}</td>
                            <td>{item.summary.total_equipment}</td>
                        </tr>
                    ))}
                </tbody>

            </table>
        </div>
    );
};

export default History;