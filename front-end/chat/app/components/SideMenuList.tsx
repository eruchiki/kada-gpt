import React from 'react';
import { List,ListItem,ListItemText } from '@mui/material';
import Link from 'next/link';
import ThreadsPropsType from '@/types/ThreadProps';

const SideMenuList = (threadlist: Array<ThreadsPropsType>) => {
  // const menulist = ["仕事","新規作成"]
  // const menupath = [`${process.env.NEXT_PUBLIC_ROOTPATH}/thread/1`,`${process.env.NEXT_PUBLIC_ROOTPATH}/thread/2`]
  return (
    <>
      <List>
        {threadlist.map((text, index) => (
          <Link href={`${process.env.NEXT_PUBLIC_ROOTPATH}/thread/${text.id}`}>
          <ListItem button key={text}>
            <ListItemText primary={text} />
          </ListItem>
          </Link>
        ))}
      </List>
    </>
  );
}
export default SideMenuList