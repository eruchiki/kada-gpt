"use client";


import * as React from 'react';
import AppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import LoginButton from './Login';
import MenuButton from './MenuButton';
import PersistentDrawerLeft from './PersistentDrawerLeft';
import HeaderPropsType from '../types/HeaderProps';


const Header = (props:  HeaderPropsType) => {
  const [open, setOpen] = React.useState(false); 
  return (
    <div style={{ width: "100%" }}>
      <AppBar position="sticky">
        <Toolbar>
          <MenuButton open={open} setOpen={setOpen} />
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            Kada GPT
          </Typography>
          <LoginButton SessionUser={props.SessionUser} />
        </Toolbar>
      </AppBar>
      {props.SessionUser && (
        <PersistentDrawerLeft
          open={open}
          setOpen={setOpen}
          threadlist={props.ThreadList}
          userid={props.SessionUser?.id}
          PopUpData={props.PopUpData}
        />
      )}
    </div>
  );
};

export default Header
