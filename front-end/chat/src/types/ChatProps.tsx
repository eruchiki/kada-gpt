import * as React from "react";
import ThreadInfoPropsType from "./ThreadInfoProps"

type ChatPropsType = {
  setData: React.Dispatch<React.SetStateAction<any>>;
  setPrompt: React.Dispatch<React.SetStateAction<string>>;
  prompt: string;
  ThreadInfo: ThreadInfoPropsType;
  userid: number;
};

export default ChatPropsType;
