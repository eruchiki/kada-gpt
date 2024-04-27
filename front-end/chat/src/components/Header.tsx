"use client";

import { useSession } from "next-auth/react"
import * as React from 'react';
import AppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import Login from './Login';
import MenuButton from './MenuButton';
import ThreadsPropsType from '../types/ThreadProps';
import PersistentDrawerLeft from './PersistentDrawerLeft';
import GetThreadList from "@/app/api/GetThreadList";


const Header = () => {
  const [open, setOpen] = React.useState(false);
  const [ThreadList, setThreadList] = React.useState<ThreadsPropsType[]>([]);
  const { data: session, status } = useSession()

  React.useEffect(() => {
    if (session) {
      // const threadlist = [
      //   { id: 1, name: "test1" },
      //   { id: 2, name: "test2" },
      // ];
      const AxiosFunction = async () => {
        const threadlist = await GetThreadList(session?.user?.email);
        console.log(threadlist);
        setThreadList(threadlist);
      };
      AxiosFunction();
    }
  }, [session]);
  return (
    <div style={{ width: "100%" }}>
      <AppBar position="static">
        <Toolbar>
          <MenuButton open={open} setOpen={setOpen} />
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            Kada GPT
          </Typography>
          <Login />
        </Toolbar>
      </AppBar>
      <PersistentDrawerLeft
        open={open}
        setOpen={setOpen}
        threadlist={ThreadList}
      />
    </div>
  );
};

export default Header
