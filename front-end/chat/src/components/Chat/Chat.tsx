"use client";

import { useState, useEffect } from "react";
import PromptInput from "../PromptInput/PromptInput";
import './Chat.css';
import GetThread from "@/app/api/GetThread";
import GetChatHisotry from '@/app/api/GetChatHistory';
import SendMessage from "@/app/api/SendMessage";
import ChatHisotryPropsType from '@/src/types/ChatHistoryTypes';
import ThreadInfoPropsType from "../../types/ThreadInfoProps";
import PromptResponseList from "../PromptResponseList/PromptResponseList";
import ChatPramasPropsType from "../../types/ChatParmsProps"


// const Chat: React.FC<{ ThreadData: ThreadInfoPropsType }> = ({
const Chat = (props:ChatPramasPropsType) => {
  // const [responseList, setResponseList] = useState<ChatHisotryPropsType[]>([]);
  const [prompt, setPrompt] = useState<string>("");
  const [ChatHistory, setChatHistory] = useState<ChatHisotryPropsType[]>([]);
  const [ThreadInfo, setThreadInfo] = useState<ThreadInfoPropsType>({
    id: -1,
    name: "",
    model_name: "",
    relate_num: 4,
    collections_id: -1,
    search_method: "",
    create_user_id: -1,
    group_id: 2,
  });
  // const [responseList, setResponseList] = useState<ChatHisotryPropsType[]>([]);

  useEffect(() => {
    const AxiosFunction = async () => {
      if (props.SessionUser) {
        const ThreadInfo = await GetThread(
          props.SessionUser.email,
          props.ThreadId
        );
        const chathisotry = await GetChatHisotry(
          props.SessionUser.email,
          ThreadInfo.id
        );
        setThreadInfo(ThreadInfo);
        setChatHistory(chathisotry);
      }
    };
    AxiosFunction();
  }, [props.SessionUser]);
  console.log(ChatHistory);
  const ChatFunction = async () => {
    await SendMessage({
      create_user_id: ThreadInfo.create_user_id,
      thread_id: ThreadInfo.id,
      collection_id: ThreadInfo.collections_id,
      relate_num: ThreadInfo.relate_num,
      search_method: ThreadInfo.search_method,
      model_name: ThreadInfo.model_name,
      message_text: prompt,
    });
    const chathisotry = await GetChatHisotry(
      props.SessionUser.email,
      ThreadInfo.id
    );
    setChatHistory(chathisotry);
  };
  console.log(ThreadInfo);
  // console.log(ThreadInfo)
  // const responseList: ChatHisotryPropsType[] = [
  //   {
  //     id: 1,
  //     message_text: "hello",
  //     response_text: "hello",
  //     referances: ["a", "b", "c"],
  //     created_at: "1",
  //     update_at: "1",
  //     relate_num: 4,
  //     search_method: "default",
  //     model_name: "gpt3",
  //   },
  //   {
  //     id: 1,
  //     message_text: "こんにちは",
  //     response_text: "元気です",
  //     referances: ["a", "b", "c"],
  //     created_at: "1",
  //     update_at: "1",
  //     relate_num: 4,
  //     search_method: "default",
  //     model_name: "gpt3",
  //   },
  // ];
  return (
    <div className="App">
      <div id="response-list">
        <PromptResponseList responseList={ChatHistory} key="response-list" />
      </div>
      {/* { uniqueIdToRetry &&
        (<div id="regenerate-button-container">
          <button id="regenerate-response-button" className={isLoading ? 'loading' : ''} onClick={() => regenerateResponse()}>
            Regenerate Response
          </button>
        </div>
        )
      } */}
      <div id="model-select-container">
        {/* <select id="model-select" value={modelValue} onChange={(event) => setModelValue(event.target.value as ModelValueType)}>
          <option value="gpt">GPT-3 (Understand and generate natural language )</option>
          <option value="codex">Codex (Understand and generate code, including translating natural language to code)
          </option>
          <option value="image">Create Image (Create AI image using DALL·E models)</option>
        </select> */}
      </div>
      <div id="input-container">
        <PromptInput
          prompt={prompt}
          onSubmit={() => ChatFunction()}
          key="prompt-input"
          updatePrompt={(prompt) => setPrompt(prompt)}
        />
        <button
          id="submit-button"
          // className={isLoading ? "loading" : ""}
          onClick={() => ChatFunction}
        ></button>
      </div>
    </div>
  );
};

export default Chat;
