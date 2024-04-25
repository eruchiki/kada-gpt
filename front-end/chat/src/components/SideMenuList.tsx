import React from 'react';
import { List,ListItem,ListItemText } from '@mui/material';
import Link from 'next/link';
import ThreadsPropsType from '../types/ThreadProps';


const SideMenuList : React.FC<{threadlist:ThreadsPropsType[]}> = ({threadlist}) => {
  // const menulist = ["仕事","新規作成"]
  // const menupath = [`${process.env.NEXT_PUBLIC_ROOTPATH}/thread/1`,`${process.env.NEXT_PUBLIC_ROOTPATH}/thread/2`]
  return (
    <>
      <List>
        {threadlist.map(thread => (
          <Link href={`${process.env.NEXT_PUBLIC_ROOTPATH}/thread/${thread.id}`}>
          <ListItem button key={thread.name}>
            <ListItemText primary={thread.name} />
          </ListItem>
          </Link>
        ))}
      </List>
    </>
  );
}
export default SideMenuList