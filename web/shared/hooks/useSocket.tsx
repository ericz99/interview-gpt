import React, { useEffect, useContext } from "react";
import { io } from "socket.io-client";

import { SocketContext } from "@/shared/context";

type SocketEvent = {
  name: string;
  handler: (...args: any) => void;
};

export default function useSocket({ name, handler }: SocketEvent) {
  const { socket } = useContext(SocketContext);

  useEffect(() => {
    console.log("SocketIO: adding listener", name);
    socket?.on(name, handler);

    return () => {
      console.log("SocketIO: removing listener", name);
      socket?.off(name, handler);
    };
  }, [socket, name, handler]);
}
