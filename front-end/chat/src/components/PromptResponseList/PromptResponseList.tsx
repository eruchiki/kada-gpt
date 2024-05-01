"use client";

import React, {FC, useEffect, useRef} from 'react';
import ChatGptImg from '../../img/chatgpt.png';
import MyImg from '../../img/me.png';
import ReactMarkdown from 'react-markdown';
import Image from "next/image";
import MessagePropsType from '../../types/ChatHistoryTypes'
import hljs from 'highlight.js';
import './PromptResponseList.css';


const PromptResponseList: FC<{ responseList: MessagePropsType[] }> = ({ responseList }) => {
  const responseListRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    hljs.highlightAll();
  })

  useEffect(() => {
    hljs.highlightAll();
  }, [responseList]);
  console.log(responseList)
  return (
    <div className="prompt-response-list" ref={responseListRef}>
      {responseList.map((responseData) => (
        <>
          <div className={"response-container " + "my-question"}>
            <Image className="avatar-image" src={MyImg} alt="avatar" />
            <div className="prompt-content" id={responseData.id}>
              {responseData.message_text && (
                <ReactMarkdown>{responseData.message_text}</ReactMarkdown>
              )}
            </div>
          </div>
          <div className={"response-container " + "chatgpt-response"}>
            <Image className="avatar-image" src={ChatGptImg} alt="avatar" />
            <div className="prompt-content" id={responseData.id}>
              {responseData.response_text && (
                <ReactMarkdown>{responseData.response_text}</ReactMarkdown>
              )}
            </div>
          </div>
        </>
      ))}
    </div>
  );
};

export default PromptResponseList;
