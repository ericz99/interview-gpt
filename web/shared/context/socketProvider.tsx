"use client";

import { useEffect, ReactNode } from "react";
import { io } from "socket.io-client";
import { SocketContext } from "./socketContext";

type SocketProviderProps = {
  children: ReactNode;
};

export default function SocketProvider({ children }: SocketProviderProps) {
  const socket = io("ws://localhost:8000/session", {
    reconnectionDelayMax: 10000,
    transports: ["websocket", "polling"],
    path: "/ws/socket.io/",
  });

  useEffect(() => {
    socket.on("connect", () => {
      console.log("SocketIO: Connected and authenticated");
      socket.emit("ping", "ping");
    });

    socket.on("error", (msg: string) => {
      console.error("SocketIO: Error", msg);
    });

    socket.on("disconnect", () => {
      console.log(`disconnect ${socket.id}`);
    });

    // Remove all the listeners and
    // close the socket when it unmounts
    return () => {
      socket.off();
    };
  }, [socket]);

  return (
    <SocketContext.Provider value={{ socket }}>
      {children}
    </SocketContext.Provider>
  );
}
