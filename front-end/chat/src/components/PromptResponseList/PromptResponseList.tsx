"use client";

import React, { FC, useEffect, useRef } from "react";
import ChatGptImg from "../../img/chatgpt.png";
import MyImg from "../../img/me.png";
import ReactMarkdown from "react-markdown";
import Image from "next/image";
import MessagePropsType from "../../types/ChatHistoryTypes";
import hljs from "highlight.js";
import DocPropsType from "../../types/DocProps";
import "./PromptResponseList.css";
import axios from "axios";

const PDFDownLoad = async (Props: DocPropsType) => {
  const url = `api/pdf`;
  const response = await axios
    .post(url, Props, {
      responseType: "blob",
    })
    .then((response) => {
      // const blob = new Blob([response.data], { type: "application/pdf" });

      // const downloadUrl = (window.URL || window.webkitURL).createObjectURL(
      //   blob
      // );
      // const a = document.createElement("a");
      // a.href = downloadUrl;
      // a.download = "test.pdf";
      // document.body.appendChild(a);
      // a.click();
      // document.body.removeChild(a);
      const blob = new Blob([response.data], { type: "application/pdf" });
      const blobUrl = URL.createObjectURL(blob);

      // 新しいウィンドウを開く
      const newWindow = window.open();
      if (newWindow) {
        // 新しいウィンドウ内にPDFを表示する
        newWindow.document.write(
          '<iframe width="100%" height="100%" src="' + blobUrl + '"></iframe>'
        );
      } else {
        // 新しいウィンドウを開けなかった場合のエラーハンドリング
        console.error("Failed to open new window.");
      }
    })
    .catch((error) => {
      // 失敗時の処理etc
      return error;
    });
};

const PromptResponseList: FC<{
  responseList: MessagePropsType[];
  collectionId: number;
}> = ({ responseList, collectionId }) => {
  const responseListRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    hljs.highlightAll();
  });

  useEffect(() => {
    hljs.highlightAll();
  }, [responseList]);
  console.log(responseList, collectionId);
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
              {responseData.references &&
                responseData.references.length > 0 &&
                responseData.references.map((references) => (
                  <button
                    key={references.document_id}
                    onClick={() =>
                      PDFDownLoad({
                        CollectionId: collectionId,
                        DocumentId: references.document_id,
                      })
                    }
                  >
                    {references.number}
                  </button>
                ))}
            </div>
          </div>
        </>
      ))}
    </div>
  );
};

export default PromptResponseList;
