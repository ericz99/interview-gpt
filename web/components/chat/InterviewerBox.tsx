import React from "react";

type InterviewerBoxProps = {
  transcripts: string[];
};

export default function InterviewerBox({ transcripts }: InterviewerBoxProps) {
  return (
    <div className="w-full max-w-sm relative bg-[#f8f9fa] h-full rounded-md shadow-xl">
      <div className="bg-slate-400 p-4 rounded-t-md">
        <h1 className="text-lg">Interviewer</h1>
      </div>

      <div className="flex flex-col h-full p-4">
        {transcripts.map((t, idx) => (
          <div key={idx} className="bg-[#fefeff] p-2">
            <p className="text-sm">{t}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
