"use client";

import { useEffect, useRef, useCallback } from 'react';
import ContentEditable from 'react-contenteditable';
import './PromptInput.css';

interface PromptInputProps {
  prompt: string;
  onSubmit: () => void;
  updatePrompt: (prompt: string) => void;
}

const PromptInput: React.FC<PromptInputProps> = ({ prompt, onSubmit, updatePrompt }) => {
  const checkKeyPress = useCallback((e: KeyboardEvent) => {
     if (e.key === "Enter" && e.code !== "Enter") {
       // 日本語変換中のEnterキーが押されたときの処理
       e.preventDefault();
       // ここに日本語変換中のEnterキーが押されたときの処理を記述する
     } else if (e.key === "Enter" && e.code === "Enter") {
       // 通常のEnterキーが押されたときの処理
       e.preventDefault();
       if (e.ctrlKey || e.shiftKey) {
         document.execCommand("insertHTML", false, "<br/><br/>");
       } else {
         onSubmit();
       }
     }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [prompt]);

  const contentEditableRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    window.addEventListener("keydown", checkKeyPress);
    return () => {
      window.removeEventListener("keydown", checkKeyPress);
    };
  }, [checkKeyPress]);

  return (
    <ContentEditable
      innerRef={contentEditableRef}
      html={prompt}
      disabled={false}
      id="prompt-input"
      className="prompt-input"
      onChange={(event) => updatePrompt(event.target.value)}
    />
  );
};

export default PromptInput;
