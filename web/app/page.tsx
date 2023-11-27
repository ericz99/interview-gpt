import React from "react";

import { Chat } from "@/components/chat";

export default function HomePage() {
  return (
    <div className=" w-full h-full relative flex flex-col container py-8 px-4">
      <Chat />
    </div>
  );
}
