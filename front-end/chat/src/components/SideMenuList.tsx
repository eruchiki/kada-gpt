import React from "react";
import { List, Link, ListItem,  ListItemButton, ListItemIcon } from "@mui/material";
import ThreadPopup from "./Thread/ThreadPopUp"
import HomeButton from "./HomeButton"
import Tooltip from "@mui/material/Tooltip";

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
          <>
            <ListItem key="threadcreate" disablePadding>
              {/* <ListItemButton onClick={}> */}
              <Tooltip title="Thread作成" placement="bottom" arrow={true}>
                <ListItemButton>
                  <ThreadPopup
                    userid={props.userid}
                    collectionlist={props.PopUpData.CollectionList}
                    groupid={props.PopUpData.GroupId}
                  />
                </ListItemButton>
              </Tooltip>
              {/* <Tooltip
              title="PDFアップロード"
              placement="bottom"
              arrow={true}
            >
            <ListItemButton>
              <PDFPopUp
                userid={props.userid}
                collectionlist={props.PopUpData.CollectionList}
              />
            </ListItemButton>
            </Tooltip> */}
            </ListItem>
            <ListItem key="home" disablePadding>
              <ListItemButton>
                <HomeButton />
              </ListItemButton>
            </ListItem>
          </>
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
