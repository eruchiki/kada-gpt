"use client";

import { useState } from "react";
import PromptInput from "../PromptInput/PromptInput";
import "./Chat.css";
import ChatHisotryPropsType from "@/src/types/ChatHistoryTypes";
import PromptResponseList from "../PromptResponseList/PromptResponseList";
import ChatPramasPropsType from "../../types/ChatParmsProps";
import SendButton from "./SendButton";
import ChatFunction from "../../../app/api/ChatAPI";

const Chat = (props: ChatPramasPropsType) => {
  const [prompt, setPrompt] = useState<string>("");
  const [ChatHistory, setChatHistory] = useState<ChatHisotryPropsType[]>(
    props.ChatHistory
  );

  return (
    <div className="App">
      <div id="response-list">
        <PromptResponseList responseList={ChatHistory} key="response-list" />
      </div>

      <div id="model-select-container"></div>
      <div id="input-container">
        <PromptInput
          prompt={prompt}
          onSubmit={() =>
            ChatFunction({
              setData: setChatHistory,
              prompt,
              ThreadInfo: props.ThreadInfo,
              userid: props.SessionUser.id,
            })
          }
          key="prompt-input"
          updatePrompt={(prompt) => setPrompt(prompt)}
        />
        <SendButton
          setData={setChatHistory}
          prompt={prompt}
          ThreadInfo={props.ThreadInfo}
          userid={props.SessionUser.id}
        />
      </div>
    </div>
  );
};

export default Chat;
