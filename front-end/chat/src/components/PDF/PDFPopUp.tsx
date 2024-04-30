"use client";

import React, { useState } from "react";
import { Dialog, Button, DialogTitle, DialogActions, Box } from "@mui/material";
import GetCollectionList from "../../../app/api/GetCollectionList";
import DocumentAdd from "../../../app/api/DocumentAdd";
import PDFForm from "./PdfForm"
import SelectForm from "../SelectForm";
import AddIcon from "@mui/icons-material/Add";

const PDFPopUp = (userid: string) => {
  const [CollectionList,setCollectionList] = React.useState([])
  const [open, setOpen] = React.useState(false);
  const [PDFData, setPDFData] = React.useState<File[]>([]);
  const [Collections, setCollections] = React.useState<number>(0);
  const handleClickOpen = () => {
    setOpen(true);
  };
  const handleClose = () => {
    setOpen(false);
  };
  console.log(PDFData)
 React.useEffect(() => {
      const AxiosFunction = async () => {
        const CollectionList = await GetCollectionList()
        console.log(CollectionList)
        setCollectionList(
          CollectionList.map((d) => {
            return {id:d.id,name:d.name};
          })
        );
      };
      AxiosFunction();
  }, []);
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
              DocumentAdd(userid.userid, Collections, PDFData, e);
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
