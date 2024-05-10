import Menu from "@mui/material/Menu";
import { signOut } from "next-auth/react";
import { MenuItem } from "@mui/material";
import UserMenuPropsType from "../types/UserMenuProps";

const UserMenu = (props:UserMenuPropsType) => {
    const handleClose = () => {
        props.setAnchorEl(null);
    };
    return (
        <Menu
        anchorEl={props.anchorEl}
        open={props.open}
        onClose={handleClose}
        MenuListProps={{
            'aria-labelledby': 'basic-button',
          }}
      >
        <MenuItem onClick={() => signOut()}>Logout</MenuItem>
      </Menu>
    )
}
export default UserMenu