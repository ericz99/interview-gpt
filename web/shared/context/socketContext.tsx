"use client";

import { createContext } from "react";
import { Socket } from "socket.io-client";

export const SocketContext = createContext<{ socket: Socket<any, any> | null }>(
  {
    socket: null,
  }
);
