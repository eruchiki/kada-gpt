"use client";

import React from "react";
import { Dialog, Button, DialogTitle, DialogActions, Box } from "@mui/material";
import TextForm from "../TextForm";
import SelectForm from "../SelectForm";
import AddIcon from "@mui/icons-material/Add";
import axios from "axios";
import { useRouter } from "next/navigation";

type ThreadPopUpPropsType = {
  userid: number;
  collectionlist: Array<any>;
  groupid: number;
};

const CreateThread = async (ThreadInfo: any, event: any) => {
  event.preventDefault();
  const url = `api/thread`;
  return await axios
    .post(url, ThreadInfo)
    .then((response) => {
      return response.data;
    })
    .catch((error) => {
      // 失敗時の処理etc
      return error;
    });
};

const ThreadPopUp = (props: ThreadPopUpPropsType) => {
  const router = useRouter();
  // console.log(typeof userid.userid);
  const [open, setOpen] = React.useState(false);
  const [ThreadName, setThreadName] = React.useState<string>("");
  const [LLMModel, setLLMModel] = React.useState<string>("gpt4");
  const [Collections, setCollections] = React.useState<number>(0);
  const [RelateNum, setRelateNum] = React.useState<number>(4);
  const [SearchMethod, setSearchMethod] = React.useState<string>("default");
  const handleClickOpen = () => {
    setOpen(true);
  };
  const handleClose =  (id:number) => {
      setThreadName(""),
      setCollections(0),
      setLLMModel("gpt4"),
      setRelateNum(4),
      setSearchMethod("default"),
      setOpen(false);
      router.push(`/`);
  };
  const handleCreate = async (ThreadInfo: any, event: any) => {
    await CreateThread(ThreadInfo, event).then((CreateData) => {
      handleClose(CreateData.id)
    }
    );
  }
  const LLMModelList = [
    { id: "gpt-3.5-turbo", name: "gpt3" },
    { id: "gpt-4-turbo", name: "gpt4" },
  ];
  const RelateNumList = [
    { id: 1, name: 1 },
    { id: 2, name: 2 },
    { id: 3, name: 3 },
    { id: 4, name: 4 },
    { id: 5, name: 5 },
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
            DataList={props.collectionlist}
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
            onClick={(e) => {handleCreate({
                  name: ThreadName,
                  model_name: LLMModel,
                  relate_num: RelateNum,
                  collections_id: Collections,
                  search_method: SearchMethod,
                  create_user_id: props.userid,
                  group_id: props.groupid,
                },
                e)
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
