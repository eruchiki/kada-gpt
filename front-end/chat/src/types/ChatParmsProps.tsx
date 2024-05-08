import SessionPropsType from "./SessionProps";
import ThreadInfoPropsType from "./ThreadInfoProps";


type ChatParmsPropsType = {
  SessionUser: SessionPropsType;
  ThreadInfo: ThreadInfoPropsType;
  ChatHistory: any;
};
export default ChatParmsPropsType;
