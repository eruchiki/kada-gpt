"use client";

import React, { useState } from "react";
import FilePropsType from "../types/FileProps";
import { Button } from "@mui/material";
import { MuiFileInput } from "mui-file-input";

const PdfForm = (props: FilePropsType) => {
  // const [files, setFiles] = useState<File[]>([]);
  const handleDrop = (e: any) => {
    e.preventDefault();
    const mime_type = "application/pdf";
    const newFiles = [...e.dataTransfer.files];
    props.setData([...props.fileList,...newFiles]);
  };

  const handleFileChange = (newFiles: File) => {
    const mime_type = "application/pdf";
    props.setData([...props.fileList, newFiles]);
  };

  const handleCancel = (index: number) => {
    const updatedFiles = props.fileList.filter((_, i) => i !== index);
    props.setData(updatedFiles);
  };

  return (
    <div>
      <h1>PDF ファイルをアップロード</h1>
      <MuiFileInput
        onDrop={handleDrop}
        value={props.fileList}
        onChange={handleFileChange}
        helperText="PDFを選択して下さい"
      />
      {/* <form
        onSubmit={handleSubmit}
        onDrop={handleDrop}
        encType="multipart/form-data"
      >
        <input type="file" multiple accept=".pdf" onChange={handleFileChange} />
        <button type="submit">アップロード</button>
      </form> */}
      <ul>
        {props.fileList.map((file, index) => (
          <li key={index}>
            {file.name}
            <Button onClick={() => handleCancel(index)}>キャンセル</Button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default PdfForm;
