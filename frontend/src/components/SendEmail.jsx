import React, { useState } from "react";
import { useEmailProgress } from "../hooks/useEmailProgress";
import axios from "axios";
import axiosInstance from "../api/axiosInstance";

const SendEmail = () => {
  const [emailInput, setEmailInput] = useState("");
  const [serverResponse, setServerResponse] = useState(null);
  const { progress, connected } = useEmailProgress();

  const handleStartEmail = async () => {
    const emails = emailInput.split(",").map((email) => email.trim());

    try {
      const res = await axios.post('http://localhost:8000/api/start-sending-email/', { emails });
      setServerResponse(res.data);
    } catch (error) {
      console.error("Error starting email sending:", error);
      alert(error.response?.data?.error || "Something went wrong");
    }
  };

  return (
    <div style={{ padding: "2rem" }}>
      <h2>📬Email Sender</h2>

      <textarea
        placeholder="Enter emails separated by commas(,)"
        rows={4}
        style={{ width: "100%" }}
        value={emailInput}
        onChange={(e) => setEmailInput(e.target.value)}
      />

      <button onClick={handleStartEmail}>Send Emails</button>

      {serverResponse && (
        <div>
          <p>
            <strong>Task ID:</strong> {serverResponse.task_id}
          </p>
          <p>
            <strong>Valid Emails:</strong>{" "}
            {serverResponse.valid_emails.join(", ")}
          </p>
        </div>
      )}

      <hr />

      <h3>📊 Progress</h3>
      <p>WebSocket: {connected ? "Connected ✅" : "Disconnected ❌"}</p>
      <p>
        Sent: {progress?.emails_sent} / {progress?.total_emails}
      </p>
    </div>
  );
};

export default SendEmail;
