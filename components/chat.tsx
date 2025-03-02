"use client";

import { useState, useEffect } from "react";
import { useChat } from "@ai-sdk/react";
import { callBackendClient } from "@/lib/callBackendClient";

export default function Chat() {
  const [healthData, setHealthData] = useState<any>(null);

  useEffect(() => {
    const fetchHealthCheck = async () => {
      try {
        const response = await callBackendClient("/auth-health-check");
        if (!response.ok) {
          const errorText = await response.text();
          throw new Error(errorText);
        }
        const data = await response.json();
        setHealthData(data);
      } catch (err: any) {
        console.error("Error fetching health check:", err);
      }
    };

    fetchHealthCheck();
  }, []);

  const { messages, input, handleInputChange, handleSubmit } = useChat();

  return (
    <div className="flex flex-col w-full max-w-md py-24 mx-auto stretch">
      <div className="py-10">
        <h2>Client call backend health check</h2>
        <p>{healthData?.message || "Loading..."}</p>
      </div>
      {messages.map((m) => (
        <div key={m.id} className="whitespace-pre-wrap">
          {m.role === "user" ? "User: " : "AI: "}
          {m.content}
        </div>
      ))}

      <form onSubmit={handleSubmit}>
        <input
          className="fixed dark:bg-zinc-900 bottom-0 w-full max-w-md p-2 mb-8 border border-zinc-300 dark:border-zinc-800 rounded shadow-xl"
          value={input}
          placeholder="Say something..."
          onChange={handleInputChange}
        />
      </form>
    </div>
  );
}
