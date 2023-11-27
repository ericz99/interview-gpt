import React from "react";

type CopilotBoxProps = {
  answers: string[];
};

export default function CopilotBox({ answers }: CopilotBoxProps) {
  return (
    <div className="flex-1 w-full relative bg-[#f8f9fa] h-full border-solid border-2 border-[#a4243b] rounded-md shadow-xl">
      <div className="bg-[#a4243b] p-4">
        <h1 className="text-lg text-white">Copilot</h1>
      </div>

      <div className="flex flex-col h-full p-4">
        {answers.map((a, idx) => (
          <div key={idx} className="bg-[#fefeff] p-2">
            <p className="text-sm">{a}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
