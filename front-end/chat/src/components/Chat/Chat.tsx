"use client";

import {useState} from 'react';
import axios from "axios";
import PromptInput from "../PromptInput/PromptInput";
import './Chat.css';
import GetChatHisotry from '@/app/api/GetChatHistory';
import SendMessage from "@/app/api/SendMessage";
import ThreadInfoPropsTypes from "../../types/ThreadInfoProps";
import PromptResponseList from "../PromptResponseList/PromptResponseList";
import { threadId } from 'worker_threads';


const Chat = (ThreadData: ThreadInfoPropsTypes) => {
  // const [responseList, setResponseList] = useState<ChatHisotryPropsType[]>([]);
  const [prompt, setPrompt] = useState<string>("");
  // const [promptToRetry, setPromptToRetry] = useState<string | null>(null);
  // const [uniqueIdToRetry, setUniqueIdToRetry] = useState<string | null>(null);
  // const [modelValue, setModelValue] = useState<ModelValueType>('gpt');
  // const [isLoading, setIsLoading] = useState(false);
  // let loadInterval: number | undefined;

  // const generateUniqueId = () => {
  //   const timestamp = Date.now();
  //   const randomNumber = Math.random();
  //   const hexadecimalString = randomNumber.toString(16);

  //   return `id-${timestamp}-${hexadecimalString}`;
  // }

  // const htmlToText = (html: string) => {
  //   const temp = document.createElement('div');
  //   temp.innerHTML = html;
  //   return temp.textContent;
  // }

  // const delay = (ms: number) => {
  //   return new Promise( resolve => setTimeout(resolve, ms) );
  // }

  // const addLoader = (uid: string) => {
  //   const element = document.getElementById(uid) as HTMLElement;
  //   element.textContent = ''

  //   // @ts-ignore
  //   loadInterval = setInterval(() => {
  //     // Update the text content of the loading indicator
  //     element.textContent += '.';

  //     // If the loading indicator has reached three dots, reset it
  //     if (element.textContent === '....') {
  //       element.textContent = '';
  //     }
  //   }, 300);
  // }

  // const addResponse = (selfFlag: boolean, response?: string) => {
  //   const uid = generateUniqueId()
  //   setResponseList(prevResponses => [
  //     ...prevResponses,
  //     {
  //       id: uid,
  //       response,
  //       selfFlag
  //     },
  //   ]);
  //   return uid;
  // }

  // const updateResponse = (uid: string, updatedObject: Record<string, unknown>) => {
  //   setResponseList(prevResponses => {
  //     const updatedList = [...prevResponses]
  //     const index = prevResponses.findIndex((response) => response.id === uid);
  //     if (index > -1) {
  //       updatedList[index] = {
  //         ...updatedList[index],
  //         ...updatedObject
  //       }
  //     }
  //     return updatedList;
  //   });
  // }

  // const regenerateResponse = async () => {
  //   await getGPTResult(promptToRetry, uniqueIdToRetry);
  // }

  // const getGPTResult = async (_promptToRetry?: string | null, _uniqueIdToRetry?: string | null) => {
  //   // Get the prompt input
  //   const _prompt = _promptToRetry ?? htmlToText(prompt);

  //   // If a response is already being generated or the prompt is empty, return
  //   if (isLoading || !_prompt) {
  //     return;
  //   }

  //   setIsLoading(true);

  //   // Clear the prompt input
  //   setPrompt('');

  //   let uniqueId: string;
  //   if (_uniqueIdToRetry) {
  //     uniqueId = _uniqueIdToRetry;
  //   } else {
  //     // Add the self prompt to the response list
  //     addResponse(true, _prompt);
  //     uniqueId = addResponse(false);
  //     await delay(50);
  //     addLoader(uniqueId);
  //   }

  //   // API部分
  //   try {
  //     // Send a POST request to the API with the prompt in the request body
  //     const response = await axios.post('get-prompt-result', {
  //       prompt: _prompt,
  //       model: modelValue
  //     });
  //       updateResponse(uniqueId, {
  //         response: response.data.trim(),
  //     });

  //     setPromptToRetry(null);
  //     setUniqueIdToRetry(null);
  //   } catch (err) {
  //     setPromptToRetry(_prompt);
  //     setUniqueIdToRetry(uniqueId);
  //     updateResponse(uniqueId, {
  //       // @ts-ignore
  //       response: `Error: ${err.message}`,
  //       error: true
  //     });
  //   } finally {
  //     // Clear the loader interval
  //     clearInterval(loadInterval);
  //     setIsLoading(false);
  //   }
  // }
  const responseList = GetChatHisotry(ThreadData.create_user_id,ThreadData.id);
  return (
    <div className="App">
      <div id="response-list">
        <PromptResponseList responseList={responseList} key="response-list" />
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
        <label htmlFor="model-select">Select model:</label>
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
          onSubmit={() =>
            SendMessage({
              create_user_id: ThreadData.create_user_id,
              thread_id: ThreadData.id,
              collection_id: ThreadData.collections_id,
              relate_num: ThreadData.relate_num,
              search_method: ThreadData.search_method,
              model_name: ThreadData.model_name,
              message_text: prompt,
            })
          }
          key="prompt-input"
          updatePrompt={(prompt) => setPrompt(prompt)}
        />
        <button
          id="submit-button"
          className={isLoading ? "loading" : ""}
          onClick={() =>
            SendMessage({
              create_user_id: ThreadData.create_user_id,
              thread_id: ThreadData.id,
              collection_id: ThreadData.collections_id,
              relate_num: ThreadData.relate_num,
              search_method: ThreadData.search_method,
              model_name: ThreadData.model_name,
              message_text: prompt,
            })
          }
        ></button>
      </div>
    </div>
  );
};

export default Chat;
