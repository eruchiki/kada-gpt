import React from "react";
import { List, Link, ListItem,  ListItemButton, ListItemIcon } from "@mui/material";
import ThreadPopup from "./Thread/ThreadPopUp"
import PDFPopUp from "./PDF/PDFPopUp"
import PopUpFunction from "../../app/api/PopUpAPI"

type SideMenuPropsType = {
  userid: number;
  threadlist: Array<any>;
  PopUpData: { GroupId: number; CollectionList: any } | null;
};

const SideMenuList = (props: SideMenuPropsType) => {
  return (
    <>
      <List>
        {props.PopUpData && (
          <ListItem key="threadcreate" disablePadding>
            {/* <ListItemButton onClick={}> */}
            <ListItemButton>
              <ThreadPopup
                userid={props.userid}
                collectionlist={props.PopUpData.CollectionList}
                groupid={props.PopUpData.GroupId}
              />
            </ListItemButton>
            <ListItemButton>
              <PDFPopUp
                userid={props.userid}
                collectionlist={props.PopUpData.CollectionList}
              />
            </ListItemButton>
          </ListItem>
        )}
        {props.threadlist.map((thread) => (
          <ListItem key={thread.name} disablePadding>
            <ListItemButton>
              <Link
                href={`${process.env.NEXTAUTH_URL}/thread/${thread.id}`}
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
