"use client";

import React, { useState } from "react";
import { Dialog, Button, DialogTitle, DialogActions, Box } from "@mui/material";
import CreateThread from "../../app/api/CreateThread";
import TextForm from "./TextForm";
import SelectForm from "./SelectForm";
import AddIcon from "@mui/icons-material/Add";

const ThreadPopUp = () => {
  const [open, setOpen] = React.useState(false);
  const [ThreadName, setThreadName] = React.useState<string>("");
  const [LLMModel, setLLMModel] = React.useState<string>("gpt4");
  const [Collections, setCollections] = React.useState<number>(0);
  const [RelateNum, setRelateNum] = React.useState<number>(4);
  const [SearchMethod, setSearchMethod] = React.useState<string>("default");
  const handleClickOpen = () => {
    setOpen(true);
  };
  const handleClose = () => {
    setOpen(false);
  };
  const LLMModelList = [
    { id: "gpt3", name: "gpt3" },
    { id: "gpt4", name: "gpt4" },
  ];
  const RelateNumList = [
    { id: 1, name: 1 },
    { id: 2, name: 2 },
    { id: 3, name: 3 },
    { id: 4, name: 4 },
    { id: 5, name: 5 },
  ];
  const CollectionList = [
    { id: 1, name: "test1" },
    { id: 2, name: "test2" },
  ];
  const SearchMethodList = [
    { id: "default", name: "default" },
    { id: "select", name: "select" },
  ];
  return (
    <div>
      <Button variant="outlined" onClick={handleClickOpen}>
        <AddIcon />
      </Button>
      <Dialog onClose={handleClose} open={open} fullWidth={true}>
        <DialogTitle sx={{ m: 0, p: 2 }}>スレッド作成</DialogTitle>
        <Box sx={{ p: 2 }}>
          <TextForm title="名前" data={ThreadName} setData={setThreadName} />
        </Box>
        <Box sx={{ p: 1 }}>
          <SelectForm
            label="LLMモデル"
            data={LLMModel}
            DataList={LLMModelList}
            setData={setLLMModel}
          />
        </Box>
        <Box sx={{ p: 5 }}>
          <SelectForm
            label="関連情報数"
            data={RelateNum}
            DataList={RelateNumList}
            setData={setRelateNum}
          />
        </Box>
        <Box sx={{ p: 1 }}>
          <SelectForm
            label="コレクション（ベクトルDB）"
            data={Collections}
            DataList={CollectionList}
            setData={setCollections}
          />
        </Box>
        <Box sx={{ p: 1 }}>
          <SelectForm
            label="手法"
            data={SearchMethod}
            DataList={SearchMethodList}
            setData={setSearchMethod}
          />
        </Box>
        <DialogActions>
          <Button onClick={handleClose}>閉じる</Button>
          <Button
            onClick={(e) => {
              // CreateThread(userid,threaddata,e);
              handleClose();
              setThreadName("")
              setCollections(0)
              setLLMModel("gpt4")
              setRelateNum(4)
              setSearchMethod("default")
            }}
          >
            作成
          </Button>
        </DialogActions>
      </Dialog>
    </div>
  );
};

export default ThreadPopUp;
