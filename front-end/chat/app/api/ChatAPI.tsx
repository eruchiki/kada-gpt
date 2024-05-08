import SendMessage from "./SendMessage"
import GetChatHistory from "./GetChatHistory"
import ChatPropsType from "../../src/types/ChatProps";

const ChatFunction = async (props: ChatPropsType) => {
  await SendMessage({
    create_user_id: props.ThreadInfo.create_user_id,
    thread_id: props.ThreadInfo.id,
    collection_id: props.ThreadInfo.collections_id,
    relate_num: props.ThreadInfo.relate_num,
    search_method: props.ThreadInfo.search_method,
    model_name: props.ThreadInfo.model_name,
    message_text: props.prompt,
  });
  const chathisotry = await GetChatHistory(
    props.userid,
    props.ThreadInfo.id
  );
  props.setData(chathisotry);
};


export default ChatFunction;