"use client";

import { useState } from "react";
import { useSocket } from "@/shared/hooks";
import { CopilotBox, InterviewerBox } from "@/components/chat";
import { Button } from "@/components/ui/button";

type IncomingData = {
  transcript: string;
  answer: string;
};

export default function Chat() {
  const [transcripts, setTranscripts] = useState<string[]>([]);
  const [answers, setAnswers] = useState<string[]>([]);

  const incomingDataHandler = (data: IncomingData) => {
    const { transcript, answer } = data;
    setTranscripts((prev) => [...prev, transcript]);
    setAnswers((prev) => [...prev, answer]);
  };

  useSocket({
    name: "incoming data",
    handler: incomingDataHandler,
  });

  return (
    <div className="flex flex-col relative w-full h-full justify-between gap-8 my-12">
      <div className="flex flex-1 gap-8">
        <InterviewerBox transcripts={transcripts} />
        <CopilotBox answers={answers} />
      </div>
    </div>
  );
}
