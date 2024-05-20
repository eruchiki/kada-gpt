"use client";

import { useState } from "react";
import PromptInput from "../PromptInput/PromptInput";
import "./Chat.css";
import ChatHisotryPropsType from "@/src/types/ChatHistoryTypes";
import PromptResponseList from "../PromptResponseList/PromptResponseList";
import ChatPramasPropsType from "../../types/ChatParmsProps";
import ChatPropsType from "@/src/types/ChatProps";
import axios from "axios";

const SendMessage = async (Props: ChatPropsType) => {
  const url = `api/chat`;
  Props.setDisable(true)
  const response =  await axios
    .post(url, {prompt:Props.prompt,ThreadInfo:Props.ThreadInfo,userid:Props.userid})
    .then((response) => {
      return response;
    })
    .catch((error) => {
      // 失敗時の処理etc
      return error;
    })
  Props.setData(response.data);
  Props.setPrompt("");
  Props.setDisable(false);
};

const Chat = (props: ChatPramasPropsType) => {
  const [prompt, setPrompt] = useState<string>("");
  const [ChatHistory, setChatHistory] = useState<ChatHisotryPropsType[]>(
    props.ChatHistory
  );
  const [Disabled, setDisabled] = useState<boolean>(false)
  return (
    <div className="App">
      <div id="response-list">
        <PromptResponseList
          responseList={ChatHistory}
          collectionId={props.ThreadInfo.collections_id}
          key="response-list"
        />
      </div>

      <div id="model-select-container"></div>
      <div id="input-container">
        <PromptInput
          prompt={prompt}
          onSubmit={() =>
            SendMessage({
              setData: setChatHistory,
              setPrompt: setPrompt,
              setDisable: setDisabled,
              prompt,
              ThreadInfo: props.ThreadInfo,
              userid: props.SessionUser.id,
            })
          }
          key="prompt-input"
          updatePrompt={(prompt) => setPrompt(prompt)}
          Disabled={Disabled}
        />
        <button
          id="submit-button"
          // className={isLoading ? "loading" : ""}
          onClick={() =>
            SendMessage({
              setData: setChatHistory,
              setPrompt: setPrompt,
              setDisable: setDisabled,
              prompt,
              ThreadInfo: props.ThreadInfo,
              userid: props.SessionUser.id,
            })
          }
        ></button>
      </div>
    </div>
  );
};

export default Chat;
