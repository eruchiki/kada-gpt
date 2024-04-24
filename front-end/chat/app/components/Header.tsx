"use client";

import * as React from 'react';
import AppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import Login from './Login';
import MenuButton from './MenuButton';
import PersistentDrawerLeft from './PersistentDrawerLeft';


const Header = () => {
    const [open, setOpen] = React.useState(false);
  return (
    <div style = {{ width:"100%" }}>
      <AppBar position="static">
        <Toolbar>
         <MenuButton open={open} setOpen={setOpen} />
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            Kada GPT
          </Typography>
          <Login/>
        </Toolbar>
      </AppBar>
      <PersistentDrawerLeft open={open} setOpen={setOpen}/>
    </div>
  );
}

export default Header