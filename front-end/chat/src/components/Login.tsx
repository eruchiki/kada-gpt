"use client";

// import { getServerSession } from "next-auth";
import { signIn } from "next-auth/react";
import Button from "@mui/material/Button";
import { useState } from "react";
import PersonIcon from "@mui/icons-material/Person";
import IconButton from "@mui/material/IconButton";
import UserMenu from "./UserMenu";
import Tooltip from '@mui/material/Tooltip';

const LoginButton = (props: any) => {
  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null);
  const open = Boolean(anchorEl);
  const handleClick = (event: React.MouseEvent<HTMLButtonElement>) => {
    setAnchorEl(event.currentTarget);
  };
  const [showTooltip, setShowTooltip] = useState(false);
  const handleMouseEnter = () => {
    setShowTooltip(true);
  };

  const handleMouseLeave = () => {
    setShowTooltip(false);
  };
  return (
    <>
      {props.SessionUser && (
        <>
          <Tooltip
            title={props.SessionUser.name}
            placement="bottom"
            arrow={true}
          >
            <IconButton
              aria-controls={open ? "basic-menu" : undefined}
              aria-haspopup="true"
              aria-expanded={open ? "true" : undefined}
              onClick={handleClick}
              onMouseEnter={handleMouseEnter}
              onMouseLeave={handleMouseLeave}
            >
              <PersonIcon />
            </IconButton>
            <UserMenu
              open={open}
              setAnchorEl={setAnchorEl}
              anchorEl={anchorEl}
            />
          </Tooltip>
        </>
      )}
      {!props.SessionUser && (
        <Button color="inherit" onClick={() => signIn()}>
          Login
        </Button>
      )}
    </>
  );
};

export default LoginButton;
