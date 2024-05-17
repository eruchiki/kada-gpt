import React from "react";
import { List, Link, ListItem,  ListItemButton, ListItemIcon, ListItemText } from "@mui/material";
import ThreadPopup from "./Thread/ThreadPopUp";
import Tooltip from "@mui/material/Tooltip";
import HomeOutlinedIcon from "@mui/icons-material/HomeOutlined";

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
              <ListItemButton component="a" to="/">
                <HomeOutlinedIcon
                  color="primary"
                  sx={{ fontSize: 25, marginRight: 1 }}
                />
                <ListItemText
                  primary="ホーム"
                  primaryTypographyProps={{
                    color: "primary",
                    fontWeight: "medium",
                  }}
                />
              </ListItemButton>
            </ListItem>
          </>
        )}
        {props.threadlist.map((thread) => (
          <ListItem key={thread.name} disablePadding>
            <ListItemButton
              component="a"
              to={`/thread/${thread.id}`}
            >
              <ListItemText
                primary={thread.name}
                primaryTypographyProps={{
                  color: "primary",
                  fontWeight: "medium",
                }}
              />
            </ListItemButton>
          </ListItem>
        ))}
      </List>
    </>
  );
};
export default SideMenuList;
