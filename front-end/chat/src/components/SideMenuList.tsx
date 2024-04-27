import React from "react";
import { List, Link, ListItem,  ListItemButton, ListItemIcon } from "@mui/material";
import ThreadsPropsType from "../types/ThreadProps";
import ThreadPopup from "./ThreadPopUp"
import PDFPopUp from "./PDFPopUp"


const SideMenuList: React.FC<{ threadlist: ThreadsPropsType[] }> = ({
  threadlist,
}) => {
  // const menulist = ["仕事","新規作成"]
  // const menupath = [`${process.env.NEXT_PUBLIC_ROOTPATH}/thread/1`,`${process.env.NEXT_PUBLIC_ROOTPATH}/thread/2`]
  return (
    <>
      <List>
        <ListItem key="threadcreate" disablePadding>
          {/* <ListItemButton onClick={}> */}
          <ListItemButton>
            <ThreadPopup />
          </ListItemButton>
          <ListItemButton>
            <PDFPopUp />
          </ListItemButton>
        </ListItem>
        {threadlist.map((thread) => (
          <ListItem key={thread.name} disablePadding>
            <ListItemButton>
              <Link
                href={`${process.env.NEXT_PUBLIC_ROOTPATH}/thread/${thread.id}`}
                key={thread.name}
                underline="none"
              >
                {thread.name}
              </Link>
            </ListItemButton>
          </ListItem>
        ))}
      </List>
    </>
  );
};
export default SideMenuList;
