import React from "react"
import { IconButton } from "@mui/material";
import MenuIcon from '@mui/icons-material/Menu';
import SideMenuPropsType from "../types/SideMenuProps";

const MenuButton = (props:SideMenuPropsType) => {
    const handleDrawerOpen = () => {
        props.setOpen(true);
    };
    return (
        <IconButton
            color="inherit"
            aria-label="open drawer"
            onClick={handleDrawerOpen}
            edge="start"  
            sx={{ mr: 2, ...(props.open && { display: 'none' }) }}
          >
            <MenuIcon />
          </IconButton>
    )
}

export default MenuButton