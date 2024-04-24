"use client";

// import { getServerSession } from "next-auth";
import { useSession } from "next-auth/react"
import { signIn } from 'next-auth/react'
import Button from '@mui/material/Button'
import {useState} from 'react'
import PersonIcon from '@mui/icons-material/Person';
import IconButton from '@mui/material/IconButton';
import UserMenu from './UserMenu';


const LoginButton = () => {
  const { data: session, status } = useSession()
    const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null);
    const open = Boolean(anchorEl);
    const handleClick = (event: React.MouseEvent<HTMLButtonElement>) => {
        setAnchorEl(event.currentTarget);
    };
    console.log(session)
    return (
        <>
          {session && (
            <>
            <IconButton
            aria-controls={open ? 'basic-menu' : undefined}
            aria-haspopup="true"
            aria-expanded={open ? 'true' : undefined}
            onClick={handleClick}>
            <PersonIcon/>
            </IconButton>
            <UserMenu open={open} setAnchorEl={setAnchorEl} anchorEl={anchorEl}/> 
            </>
          )}
          {!session && (
            <Button color='inherit' onClick={() => signIn()}>Login</Button>
          )}
        </>
      )
}

export default LoginButton