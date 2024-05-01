"use client";

import React, { useState } from "react";
import { Dialog, Button, DialogTitle, DialogActions, Box } from "@mui/material";
import PDFForm from "./PdfForm"
import SelectForm from "../SelectForm";
import AddIcon from "@mui/icons-material/Add";
import PDFPopupPropsType from "../../types/PDFPopupProps"
import axios from "axios";

type DocumentPropsType = {
  userid: number;
  Collections: number;
  PDFData: File[];
};

const DocumentAdd = async (props: DocumentPropsType, event: any) => {
  event.preventDefault();
  const url = `api/pdf`;
  return await axios
    .post(url, props)
    .then((response) => {
      return response.data;
    })
    .catch((error) => {
      // 失敗時の処理etc
      return error;
    });
};

const PDFPopUp = (props: PDFPopupPropsType) => {
  const [open, setOpen] = React.useState(false);
  const [PDFData, setPDFData] = React.useState<File[]>([]);
  const [Collections, setCollections] = React.useState<number>(0);
  const handleClickOpen = () => {
    setOpen(true);
  };
  const handleClose = () => {
    setOpen(false);
  };
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
            DataList={props.collectionlist}
            setData={setCollections}
          />
        </Box>
        <Box sx={{ p: 1 }}>
          <PDFForm setData={setPDFData} fileList={PDFData}></PDFForm>
        </Box>
        <DialogActions>
          <Button onClick={handleClose}>閉じる</Button>
          <Button
            onClick={(e) => {
              DocumentAdd(props.userid, Collections, PDFData, e);
              handleClose();
              // setPDFData([]);
              // setCollections(0);
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
