"use client";

import React, { useState } from "react";
import { Dialog, Button, DialogTitle, DialogActions, Box } from "@mui/material";
import CreateThread from "../../app/api/CreateThread";
import TextForm from "./TextForm";
import PDFForm from "./PdfForm"
import SelectForm from "./SelectForm";
import AddIcon from "@mui/icons-material/Add";

const PDFPopUp = () => {
  const [open, setOpen] = React.useState(false);
  const [PDFData, setPDFData] = React.useState<File[]>([]);
  const [Collections, setCollections] = React.useState<number>(0);
  const handleClickOpen = () => {
    setOpen(true);
  };
  const handleClose = () => {
    setOpen(false);
  };
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
        <DialogTitle sx={{ m: 0, p: 2 }}>関連文書登録</DialogTitle>
        <Box sx={{ p: 1 }}>
          <SelectForm
            label="コレクション（ベクトルDB）"
            data={Collections}
            DataList={CollectionList}
            setData={setCollections}
          />
        </Box>
        <Box sx={{ p: 1 }}>
          <PDFForm  setData={setPDFData} fileList={PDFData}></PDFForm>
        </Box>
        <DialogActions>
          <Button onClick={handleClose}>閉じる</Button>
          <Button
            onClick={(e) => {
              // CreateThread(userid,threaddata,e);
              handleClose();
              setPDFData([]);
              setCollections(0);
            }}
          >
            登録
          </Button>
        </DialogActions>
      </Dialog>
    </div>
  );
};

export default PDFPopUp;
